import json
import os
from pathlib import Path
from helpers import files
from helpers.api import ApiHandler, Request, Response
from usr.plugins.browser_session_sync.helpers.session_sync import (
    MANIFEST_FILE_NAME,
    load_config,
    save_config,
)

SAVE_DIR = Path(files.get_abs_path("usr", "browser_sessions"))


class SessionsList(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        action = input.get("action", "list")
        
        if action == "list":
            return self._list_sessions()
        elif action == "delete":
            filename = input.get("filename", "")
            return self._delete_session(filename)
        elif action == "delete_all":
            return self._delete_all()
        elif action == "stats":
            return self._get_stats()
        elif action == "prune":
            keep_count = int(input.get("keep_count", 10))
            return self._prune_oldest(keep_count)
        elif action == "set_max_size":
            max_mb = float(input.get("max_mb", 50))
            return self._enforce_max_size(max_mb)
        elif action == "get_config":
            return {"ok": True, "config": load_config()}
        elif action == "save_config":
            return {"ok": True, "config": save_config(input.get("config") or input)}
        
        return {"ok": False, "error": f"Unknown action: {action}"}
    
    def _list_sessions(self) -> dict:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        sessions = []
        for f in sorted(self._session_files(), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                sessions.append(self._session_info(f, data))
            except Exception:
                sessions.append(self._session_info(f, None))
        stats = self._compute_stats(sessions)
        return {"ok": True, "sessions": sessions, "stats": stats}
    
    def _session_info(self, f: Path, data: dict | None) -> dict:
        size = f.stat().st_size
        info = {
            "name": f.name,
            "size": size,
            "size_str": self._format_size(size),
            "cookies": 0,
            "origins": 0,
            "domains": [],
            "tabs": [],
            "tab_count": 0,
            "date": f.stat().st_mtime,
            "date_str": self._format_date(f.stat().st_mtime),
        }
        if data:
            # Support both new (with context_state + tabs) and legacy (just storage_state) formats
            if "context_state" in data:
                context_state = data.get("context_state", {})
                tabs = data.get("tabs", [])
                info["tabs"] = tabs
                info["tab_count"] = len(tabs)
            else:
                context_state = data
            cookies = context_state.get("cookies", [])
            origins = context_state.get("origins", [])
            info["cookies"] = len(cookies)
            info["origins"] = len(origins)
            domains = sorted(set(c.get("domain", "") for c in cookies if c.get("domain")))
            info["domains"] = domains[:20]
            if len(domains) > 20:
                info["domains"].append(f"... and {len(domains)-20} more")
        return info
    
    def _compute_stats(self, sessions: list) -> dict:
        total_size = sum(s["size"] for s in sessions)
        total_cookies = sum(s["cookies"] for s in sessions)
        total_origins = sum(s["origins"] for s in sessions)
        total_tabs = sum(s.get("tab_count", 0) for s in sessions)
        all_domains = set()
        for s in sessions:
            for d in s.get("domains", []):
                if not d.startswith("..."):
                    all_domains.add(d)
        return {
            "total_files": len(sessions),
            "total_size": total_size,
            "total_size_str": self._format_size(total_size),
            "total_cookies": total_cookies,
            "total_origins": total_origins,
            "total_tabs": total_tabs,
            "unique_domains": len(all_domains),
        }
    
    def _get_stats(self) -> dict:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        sessions = []
        for f in self._session_files():
            sessions.append(self._session_info(f, None))
        return {"ok": True, "stats": self._compute_stats(sessions)}
    
    def _delete_session(self, filename: str) -> dict:
        if not filename or ".." in filename or "/" in filename or "\\" in filename:
            return {"ok": False, "error": "Invalid filename"}
        fpath = SAVE_DIR / filename
        if fpath.exists():
            fpath.unlink()
            return {"ok": True}
        return {"ok": False, "error": "File not found"}
    
    def _delete_all(self) -> dict:
        count = 0
        for f in self._session_files():
            f.unlink()
            count += 1
        return {"ok": True, "deleted": count}
    
    def _prune_oldest(self, keep_count: int) -> dict:
        files_sorted = sorted(self._session_files(),
                             key=lambda p: p.stat().st_mtime, reverse=True)
        if len(files_sorted) <= keep_count:
            return {"ok": True, "deleted": 0, "message": f"Already at or below limit ({len(files_sorted)} <= {keep_count})"}
        to_delete = files_sorted[keep_count:]
        for f in to_delete:
            f.unlink()
        return {"ok": True, "deleted": len(to_delete), "kept": keep_count}
    
    def _enforce_max_size(self, max_mb: float) -> dict:
        max_bytes = int(max_mb * 1024 * 1024)
        files_sorted = sorted(self._session_files(),
                             key=lambda p: p.stat().st_mtime, reverse=True)
        total_size = sum(f.stat().st_size for f in files_sorted)
        if total_size <= max_bytes:
            return {"ok": True, "deleted": 0, "message": f"Cache size OK ({self._format_size(total_size)} <= {max_mb} MB)"}
        deleted = 0
        saved_bytes = 0
        for f in files_sorted[::-1]:
            if total_size - saved_bytes <= max_bytes:
                break
            saved_bytes += f.stat().st_size
            f.unlink()
            deleted += 1
        return {"ok": True, "deleted": deleted, "freed": self._format_size(saved_bytes)}
    
    def _format_size(self, bytes_val: int) -> str:
        if bytes_val < 1024:
            return f"{bytes_val} B"
        elif bytes_val < 1024 * 1024:
            return f"{bytes_val / 1024:.1f} KB"
        else:
            return f"{bytes_val / (1024 * 1024):.2f} MB"
    
    def _format_date(self, ts: float) -> str:
        import datetime
        return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    def _session_files(self) -> list[Path]:
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
        return [
            path
            for path in SAVE_DIR.glob("*.json")
            if path.name != MANIFEST_FILE_NAME
        ]
