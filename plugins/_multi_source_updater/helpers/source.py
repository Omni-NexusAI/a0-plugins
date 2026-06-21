from __future__ import annotations

import re
import os
import subprocess
import time
from pathlib import Path
from typing import Any

from helpers import plugins


PLUGIN_NAME = "_multi_source_updater"
AGENTSPINE_PUBLIC_LATEST_TAG = "v0.9.9-standard-pre"
AGENTSPINE_EFFECTIVE_LABEL = f"{AGENTSPINE_PUBLIC_LATEST_TAG} (current Agentspine build)"

UPDATE_SOURCES: dict[str, dict[str, str]] = {
    "omni-nexusai": {
        "label": "Agentspine (Omni-NexusAI)",
        "author": "Omni-NexusAI",
        "name": "agent-zero",
    },
    "agent0ai": {
        "label": "Agent Zero upstream (agent0ai)",
        "author": "agent0ai",
        "name": "agent-zero",
    },
}

_branch_cache: dict[str, tuple[float, list[str]]] = {}
_tag_cache: dict[str, tuple[float, list[str]]] = {}
_CACHE_TTL_SECONDS = 60.0


def normalize_source(value: str | None) -> str:
    key = (value or "").strip().lower()
    return key if key in UPDATE_SOURCES else "omni-nexusai"


def get_active_source_key() -> str:
    try:
        config = plugins.get_plugin_config(PLUGIN_NAME) or {}
    except Exception:
        config = {}
    if not isinstance(config, dict):
        config = {}
    return normalize_source(config.get("update_source"))


def set_active_source_key(value: str | None) -> str:
    key = normalize_source(value)
    plugins.save_plugin_config(PLUGIN_NAME, "", "", {"update_source": key})
    clear_caches()
    return key


def get_active_source() -> dict[str, str]:
    return UPDATE_SOURCES[get_active_source_key()]


def source_options() -> list[dict[str, str]]:
    return [{"value": key, "label": value["label"]} for key, value in UPDATE_SOURCES.items()]


def remote_url(source_key: str | None = None) -> str:
    source = UPDATE_SOURCES[normalize_source(source_key or get_active_source_key())]
    return f"https://github.com/{source['author']}/{source['name']}.git"


def clear_caches() -> None:
    _branch_cache.clear()
    _tag_cache.clear()
    try:
        from helpers import self_update

        if hasattr(self_update, "_remote_branch_tag_cache"):
            self_update._remote_branch_tag_cache.clear()
        if hasattr(self_update, "_remote_branch_head_cache"):
            self_update._remote_branch_head_cache.clear()
        if hasattr(self_update, "_remote_branch_list_cache"):
            self_update._remote_branch_list_cache = None
    except Exception:
        pass


def _run_git_raw(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        capture_output=True,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        timeout=20,
    )
    return completed.stdout.strip()


def _sort_branches(branches: list[str]) -> list[str]:
    priority = {"main": 0, "development": 1, "ready": 2, "testing": 3}
    return sorted(dict.fromkeys(branches), key=lambda value: (priority.get(value, 100), value))


def get_available_branch_values() -> list[str]:
    key = get_active_source_key()
    cached = _branch_cache.get(key)
    now = time.monotonic()
    if cached and now - cached[0] <= _CACHE_TTL_SECONDS:
        return list(cached[1])

    branches: list[str] = []
    try:
        output = _run_git_raw("ls-remote", "--heads", remote_url(key))
        prefix = "refs/heads/"
        for line in output.splitlines():
            parts = line.strip().split()
            if len(parts) == 2 and parts[1].startswith(prefix):
                branches.append(parts[1][len(prefix):])
    except Exception:
        branches = []

    if not branches:
        branches = ["main", "development", "ready", "testing"]
    branches = _sort_branches(branches)
    _branch_cache[key] = (now, branches)
    return list(branches)


def _is_upstream_tag(tag: str) -> bool:
    return re.fullmatch(r"v\d+\.\d+", tag.strip()) is not None


def _is_agentspine_tag(tag: str) -> bool:
    return re.fullmatch(r"v\d+\.\d+\.\d+-(?:(?:standard|gpu)(?:-pre)?|custom)", tag.strip()) is not None


def _tag_sort_key(tag: str) -> tuple[int, int, int, int, str]:
    match = re.match(r"v(\d+)\.(\d+)(?:\.(\d+))?", tag)
    major = int(match.group(1)) if match else -1
    minor = int(match.group(2)) if match else -1
    patch = int(match.group(3)) if match and match.group(3) else -1
    stable = 1 if "-pre" not in tag else 0
    return (major, minor, patch, stable, tag)


def get_available_tags(branch: str | None = None, query: str = "") -> tuple[list[str], str]:
    key = get_active_source_key()
    cached = _tag_cache.get(key)
    now = time.monotonic()
    if cached and now - cached[0] <= _CACHE_TTL_SECONDS:
        tags = list(cached[1])
    else:
        try:
            output = _run_git_raw("ls-remote", "--tags", "--refs", remote_url(key))
            prefix = "refs/tags/"
            tags = []
            for line in output.splitlines():
                parts = line.strip().split()
                if len(parts) == 2 and parts[1].startswith(prefix):
                    tag = parts[1][len(prefix):]
                    if key == "omni-nexusai" and _is_agentspine_tag(tag):
                        tags.append(tag)
                    elif key == "agent0ai" and _is_upstream_tag(tag):
                        tags.append(tag)
            tags = sorted(dict.fromkeys(tags), key=_tag_sort_key, reverse=True)
            _tag_cache[key] = (now, tags)
        except Exception as exc:
            return [], str(exc)

    normalized_query = query.strip().lower()
    if normalized_query:
        tags = [tag for tag in tags if normalized_query in tag.lower()]
    return tags, ""


def _agentspine_release_info(base: dict[str, Any], branch: str = "main") -> dict[str, Any]:
    info = dict(base or {})
    info["branch"] = branch or info.get("branch", "main")
    info["describe"] = AGENTSPINE_PUBLIC_LATEST_TAG
    info["short_tag"] = AGENTSPINE_PUBLIC_LATEST_TAG
    info["display_version"] = AGENTSPINE_EFFECTIVE_LABEL
    info["agentspine_effective_latest"] = True
    info["actual_upstream_version"] = base.get("short_tag", "")
    info["actual_upstream_describe"] = base.get("describe", "")
    return info


def is_agentspine_source() -> bool:
    return get_active_source_key() == "omni-nexusai"


def get_selector_tag_options(
    branch: str | None = None,
    *,
    repo_dir: str | Path | None = None,
    current_version: str | None = None,
) -> tuple[list[dict[str, str]], list[int], str]:
    tags, error = get_available_tags(branch)
    if error:
        return [], [], error
    options = []
    if get_active_source_key() == "agent0ai":
        options.append({"value": "latest", "label": "latest"})
    elif AGENTSPINE_PUBLIC_LATEST_TAG not in tags:
        tags.insert(0, AGENTSPINE_PUBLIC_LATEST_TAG)
    options.extend({"value": tag, "label": tag} for tag in tags)
    return options, [], ""


def apply_to_self_update_module(module: Any) -> None:
    source = get_active_source()
    module.OFFICIAL_REPO_AUTHOR = source["author"]
    module.OFFICIAL_REPO_NAME = source["name"]


def _write_pending_update(module: Any, payload: dict[str, Any]) -> None:
    writer = getattr(module, "_write_yaml", None)
    path_getter = getattr(module, "get_update_file_path", None)
    if callable(writer) and callable(path_getter):
        writer(path_getter(), payload)


def _schedule_update(module: Any, **kwargs) -> dict[str, Any]:
    repository = module.get_repo_dir(kwargs.get("repo_dir"))
    version_info = module.get_repo_version_info(repository)
    branch = str(kwargs.get("branch", "")).strip().lower()
    tag = str(kwargs.get("tag", "")).strip() or "latest"
    branches = set(get_available_branch_values())
    if branch not in branches:
        raise ValueError("Branch must be one of the available remote branches.")
    tag_options, _, tag_error = get_selector_tag_options(branch, repo_dir=repository, current_version=version_info["short_tag"])
    if tag_error:
        raise RuntimeError(tag_error)
    if tag not in {option["value"] for option in tag_options}:
        raise ValueError(f"Version {tag} does not exist on branch {branch}.")

    policy = str(kwargs.get("backup_conflict_policy", "rename")).strip().lower()
    if policy not in module.BACKUP_CONFLICT_POLICIES:
        raise ValueError("Backup conflict policy must be one of: rename, overwrite, fail.")

    backup_path = module._resolve_backup_path(str(kwargs.get("backup_path", "")), repository)
    backup_name = module._sanitize_filename(
        str(kwargs.get("backup_name", "")),
        module.build_default_backup_name(version_info["short_tag"], tag),
    )
    active_key = get_active_source_key()
    payload = {
        "branch": branch,
        "tag": tag,
        "source_version": version_info["short_tag"],
        "source_describe": version_info["describe"],
        "source_commit": version_info["commit"],
        "requested_at": module._now_iso(),
        "backup_usr": bool(kwargs.get("backup_usr")),
        "backup_path": str(backup_path),
        "backup_name": backup_name,
        "backup_conflict_policy": policy,
        "update_source": active_key,
        "remote_url": remote_url(active_key),
    }
    if active_key == "omni-nexusai":
        payload["agentspine_effective_current_tag"] = AGENTSPINE_PUBLIC_LATEST_TAG
        payload["actual_upstream_version"] = version_info["short_tag"]
    _write_pending_update(module, payload)
    ensure_manager_remote_url_support()
    return payload


def ensure_manager_remote_url_support() -> None:
    manager_path = Path("/exe/self_update_manager.py")
    try:
        text = manager_path.read_text(encoding="utf-8")
    except Exception:
        return
    marker = "# Agentspine multi-source updater: request remote support"
    if marker in text:
        return
    target = "def execute_pending_update(\n    request_data: dict[str, Any],\n    *,\n    logger: AttemptLogger,\n) -> subprocess.Popen[bytes]:\n"
    replacement = target + f"    {marker}\n    global OFFICIAL_REPO_URL\n    requested_remote_url = str(request_data.get(\"remote_url\", \"\")).strip()\n    if requested_remote_url:\n        OFFICIAL_REPO_URL = requested_remote_url\n        logger.log(f\"Using update remote {{OFFICIAL_REPO_URL}}\")\n"
    if target not in text:
        return
    manager_path.write_text(text.replace(target, replacement, 1), encoding="utf-8")


def patch_self_update() -> None:
    from helpers import self_update

    ensure_manager_remote_url_support()
    if getattr(self_update, "_agentspine_multi_source_patched", False):
        apply_to_self_update_module(self_update)
        return

    originals: dict[str, Any] = {}

    def store_original(name: str) -> Any:
        original = getattr(self_update, name, None)
        if callable(original):
            originals[name] = original
        return original

    store_original("get_available_branch_values")
    self_update.get_available_branch_values = lambda repo_dir=None: get_available_branch_values()

    store_original("get_available_branches")
    self_update.get_available_branches = lambda repo_dir=None: [
        {"value": branch, "label": branch} for branch in get_available_branch_values()
    ]

    store_original("get_available_tags")
    self_update.get_available_tags = lambda branch=None, repo_dir=None, query="": get_available_tags(branch, query=query)

    store_original("get_selector_tag_options")
    self_update.get_selector_tag_options = get_selector_tag_options

    store_original("schedule_update")
    self_update.schedule_update = lambda **kwargs: _schedule_update(self_update, **kwargs)

    original_remote_url = store_original("_get_official_remote_url")
    if callable(original_remote_url):
        self_update._get_official_remote_url = lambda: remote_url()

    original_info = store_original("get_update_info")
    if callable(original_info):
        def get_update_info(*args, **kwargs):
            apply_to_self_update_module(self_update)
            info = original_info(*args, **kwargs)
            if isinstance(info, dict):
                active_key = get_active_source_key()
                info["update_sources"] = source_options()
                info["active_update_source"] = active_key
                info["active_update_remote_url"] = remote_url(active_key)
                info["available_branches"] = [
                    {"value": branch, "label": branch} for branch in get_available_branch_values()
                ]
                default_branch = info.get("default_branch") or (get_available_branch_values()[0] if get_available_branch_values() else "main")
                tag_options, higher_major_versions, tags_error = get_selector_tag_options(default_branch)
                info["tag_options"] = tag_options
                info["higher_major_versions"] = higher_major_versions
                info["tags_error"] = tags_error
                info["branches"] = [{"value": branch, "label": branch} for branch in get_available_branch_values()]
                info["available_tag_options"] = tag_options
                info["available_tags"] = [option["value"] for option in tag_options]
                info["available_higher_major_versions"] = higher_major_versions
                info["available_tags_error"] = tags_error
                defaults = dict(info.get("defaults") or {})
                defaults["branch"] = default_branch
                if active_key == "omni-nexusai":
                    actual_current = dict(info.get("current") or {})
                    current = _agentspine_release_info(actual_current, info.get("current", {}).get("branch", default_branch))
                    latest = _agentspine_release_info(actual_current, "main")
                    info["current"] = current
                    info["main_branch_latest"] = latest
                    info["current_branch_latest"] = _agentspine_release_info(actual_current, default_branch)
                    info["major_upgrade_versions"] = []
                    defaults["tag"] = AGENTSPINE_PUBLIC_LATEST_TAG
                    defaults["backup_name"] = self_update.build_default_backup_name(
                        AGENTSPINE_PUBLIC_LATEST_TAG,
                        AGENTSPINE_PUBLIC_LATEST_TAG,
                    )
                    info["agentspine_version_spoof"] = {
                        "enabled": True,
                        "effective_latest": AGENTSPINE_PUBLIC_LATEST_TAG,
                        "reason": "Agentspine standard-pre latest is v0.9.9-standard-pre; this build is treated as current for the Agentspine source.",
                        "actual_upstream_version": actual_current.get("short_tag", ""),
                    }
                else:
                    info["agentspine_version_spoof"] = {"enabled": False}
                    defaults.setdefault("tag", info.get("current", {}).get("short_tag", ""))
                info["defaults"] = defaults
            return info

        self_update.get_update_info = get_update_info

    self_update._agentspine_multi_source_originals = originals
    self_update._agentspine_multi_source_patched = True
    apply_to_self_update_module(self_update)
