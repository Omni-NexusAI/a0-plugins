from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from types import SimpleNamespace

from usr.plugins.browser_session_sync.helpers import session_sync


class FakePage:
    def __init__(self, url: str = "about:blank", title: str = ""):
        self.url = url
        self._title = title
        self.listeners = {}
        self.goto_calls = []

    def on(self, event: str, callback):
        self.listeners[event] = callback

    async def title(self):
        return self._title

    async def goto(self, url: str, **kwargs):
        self.url = url
        self.goto_calls.append((url, kwargs))


class FakeContext:
    def __init__(self):
        self.listeners = {}
        self.pages = []
        self.cookies = []
        self.origins = []
        self.added_cookies = []
        self.init_scripts = []

    def on(self, event: str, callback):
        self.listeners[event] = callback

    async def storage_state(self):
        return {"cookies": list(self.cookies), "origins": list(self.origins)}

    async def add_cookies(self, cookies):
        self.added_cookies.extend(cookies)
        self.cookies.extend(cookies)

    async def add_init_script(self, **kwargs):
        self.init_scripts.append(kwargs)

    async def new_page(self):
        page = FakePage()
        self.pages.append(page)
        if "page" in self.listeners:
            self.listeners["page"](page)
        return page


class FakeCore:
    def __init__(self, context_id: str = "ctx"):
        self.context_id = context_id
        self.context = FakeContext()
        self.pages = {}
        self.last_interacted_browser_id = None
        self.next_id = 1
        self.started = False

    def _max_open_tabs(self):
        return 8

    def _ensure_can_open_page(self):
        if len(self.pages) >= self._max_open_tabs():
            raise RuntimeError("too many tabs")

    async def _register_page(self, page):
        item = SimpleNamespace(id=self.next_id, page=page)
        self.pages[self.next_id] = item
        self.next_id += 1
        return item

    async def _goto(self, page, url):
        await page.goto(url)

    async def ensure_started(self):
        self.started = True


def write_snapshot(path: Path, payload: dict):
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_context_id_from_extension_data_accepts_context_object():
    data = {"args": (SimpleNamespace(id="abc123"),)}

    assert session_sync.context_id_from_extension_data(data) == "abc123"
    assert session_sync.context_id_from_extension_data({"args": ("raw-id",)}) == "raw-id"


def test_select_best_snapshot_prefers_exact_tab_snapshot(tmp_path, monkeypatch):
    monkeypatch.setattr(session_sync, "SAVE_DIR", tmp_path)
    write_snapshot(tmp_path / "ctx_older.json", {"cookies": [{"domain": "example.com"}], "origins": []})
    write_snapshot(
        tmp_path / "other_newer.json",
        {"context_state": {"cookies": [], "origins": []}, "tabs": [{"url": "https://other.test"}]},
    )
    write_snapshot(
        tmp_path / "ctx_newer.json",
        {"context_state": {"cookies": [], "origins": []}, "tabs": [{"url": "https://ctx.test"}]},
    )

    selected = session_sync.select_best_snapshot("ctx")

    assert selected is not None
    path, snapshot = selected
    assert path.name == "ctx_newer.json"
    assert snapshot["tabs"][0]["url"] == "https://ctx.test"


def test_select_best_snapshot_prefers_newest_current_state_over_more_tabs(tmp_path, monkeypatch):
    monkeypatch.setattr(session_sync, "SAVE_DIR", tmp_path)
    older = tmp_path / "ctx_older_many_tabs.json"
    newer = tmp_path / "ctx_newer_one_tab.json"
    write_snapshot(
        older,
        {
            "context_state": {"cookies": [], "origins": []},
            "tabs": [
                {"url": "https://one.test"},
                {"url": "https://two.test"},
                {"url": "https://three.test"},
            ],
        },
    )
    write_snapshot(
        newer,
        {"context_state": {"cookies": [], "origins": []}, "tabs": [{"url": "https://kept.test"}]},
    )
    os.utime(older, (1000, 1000))
    os.utime(newer, (2000, 2000))
    session_sync.update_manifest(
        "ctx",
        newer,
        session_sync.load_snapshot(newer),
        '["https://kept.test"]',
    )

    selected = session_sync.select_best_snapshot("ctx")

    assert selected is not None
    path, snapshot = selected
    assert path.name == newer.name
    assert [tab["url"] for tab in snapshot["tabs"]] == ["https://kept.test"]


def test_zero_tab_current_state_beats_older_tab_snapshot(tmp_path, monkeypatch):
    monkeypatch.setattr(session_sync, "SAVE_DIR", tmp_path)
    older = tmp_path / "ctx_older_many_tabs.json"
    current = tmp_path / "ctx_current_empty.json"
    write_snapshot(
        older,
        {"context_state": {"cookies": [], "origins": []}, "tabs": [{"url": "https://old.test"}]},
    )
    write_snapshot(current, {"context_state": {"cookies": [], "origins": []}, "tabs": [], "tab_count": 0})
    session_sync.update_manifest("ctx", current, session_sync.load_snapshot(current), "[]")

    selected = session_sync.select_best_snapshot("ctx")

    assert selected is not None
    path, snapshot = selected
    assert path.name == current.name
    assert snapshot["tabs"] == []


def test_legacy_snapshot_normalizes_to_context_state(tmp_path, monkeypatch):
    monkeypatch.setattr(session_sync, "SAVE_DIR", tmp_path)
    write_snapshot(tmp_path / "legacy.json", {"cookies": [{"domain": "example.com"}], "origins": []})

    snapshot = session_sync.load_snapshot(tmp_path / "legacy.json")

    assert snapshot["context_state"]["cookies"][0]["domain"] == "example.com"
    assert snapshot["tabs"] == []


def test_register_auto_save_adds_context_and_page_listeners():
    core = FakeCore()
    page = FakePage("https://example.com")
    core.pages[1] = SimpleNamespace(id=1, page=page)

    session_sync.register_auto_save(core)

    assert "page" in core.context.listeners
    assert "load" in page.listeners
    assert "close" in page.listeners
    assert "framenavigated" not in page.listeners


def test_restore_core_session_is_idempotent_and_opens_saved_tabs(tmp_path, monkeypatch):
    monkeypatch.setattr(session_sync, "SAVE_DIR", tmp_path)
    monkeypatch.setattr(session_sync, "schedule_save", lambda *args, **kwargs: None)
    write_snapshot(
        tmp_path / "ctx_20260606_210539.json",
        {
            "context_state": {"cookies": [{"name": "sid", "value": "1", "domain": ".example.com", "path": "/"}], "origins": []},
            "tabs": [{"url": "https://example.com"}, {"url": "https://github.com"}],
        },
    )
    core = FakeCore("ctx")

    first = asyncio.run(session_sync.restore_core_session(core))
    second = asyncio.run(session_sync.restore_core_session(core))

    assert "Restored 2 tabs" in first
    assert "already ran" in second
    assert len(core.pages) == 2
    assert len(core.context.added_cookies) == 1


def test_schedule_save_coalesces_rapid_events(monkeypatch):
    calls = []
    core = FakeCore("ctx")

    async def fake_save_core_snapshot(core, *, suffix=None, force=False):
        calls.append(force)
        return Path("saved.json")

    monkeypatch.setattr(session_sync, "save_core_snapshot", fake_save_core_snapshot)

    async def run():
        session_sync.schedule_save(core, delay=0.01, reason="load")
        session_sync.schedule_save(core, delay=0.01, reason="load")
        await asyncio.sleep(0.05)

    asyncio.run(run())

    assert calls == [False]


def test_save_core_snapshot_updates_manifest_and_skips_unchanged(tmp_path, monkeypatch):
    monkeypatch.setattr(session_sync, "SAVE_DIR", tmp_path)
    core = FakeCore("ctx")
    page = FakePage("https://example.com", "Example")
    core.pages[1] = SimpleNamespace(id=1, page=page)

    saved = asyncio.run(session_sync.save_core_snapshot(core, force=True))
    manifest = session_sync.load_manifest()

    assert saved.exists()
    assert manifest["contexts"]["ctx"]["filename"] == saved.name
    try:
        asyncio.run(session_sync.save_core_snapshot(core))
    except session_sync.NoSnapshotChange:
        pass
    else:
        raise AssertionError("unchanged snapshot should have been skipped")


def test_auto_restore_consumed_once_per_boot(tmp_path, monkeypatch):
    monkeypatch.setattr(session_sync, "SAVE_DIR", tmp_path)
    monkeypatch.setattr(session_sync, "boot_id", lambda: "boot-1")
    monkeypatch.setattr(session_sync, "load_config", lambda: {"enabled": True, "auto_restore": True, "auto_save": True})

    calls = []

    async def fake_run(context_id, callback, *, create=False, ensure_started=False):
        calls.append((context_id, create, ensure_started))
        return "Restored 1 tabs from ctx_current.json."

    monkeypatch.setattr(session_sync, "_run_with_core_started", fake_run)

    first = asyncio.run(session_sync.auto_restore_runtime_session_for_context("ctx"))
    second = asyncio.run(session_sync.auto_restore_runtime_session_for_context("ctx"))

    assert "Restored 1 tabs" in first
    assert "already ran" in second
    assert calls == [("ctx", True, True)]


def test_disabled_config_blocks_auto_restore_and_auto_save(tmp_path, monkeypatch):
    monkeypatch.setattr(session_sync, "SAVE_DIR", tmp_path)
    monkeypatch.setattr(session_sync, "load_config", lambda: {"enabled": False, "auto_restore": True, "auto_save": True})
    core = FakeCore("ctx")

    assert asyncio.run(session_sync.auto_restore_runtime_session_for_context("ctx")) == "Browser session auto-restore is disabled."
    session_sync.schedule_save(core, delay=0.01)

    assert not getattr(core, session_sync.SAVE_HANDLE_ATTR, None)
