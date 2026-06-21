from __future__ import annotations

import copy
import json
import re
from contextlib import nullcontext
from typing import Any

from helpers import dirty_json
from helpers.mcp_handler import (
    MCPConfig,
    MCPServerLocal,
    MCPServerRemote,
)
from helpers.settings import set_settings_delta


def _normalize_name(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")


def _is_server(value: Any) -> bool:
    return isinstance(value, dict) and any(
        key in value for key in ("command", "args", "url", "serverUrl")
    )


def _walk_servers(value: Any, key: str = ""):
    if isinstance(value, list):
        for item in value:
            yield from _walk_servers(item)
    elif isinstance(value, dict):
        if _is_server(value):
            yield key, value
        for child_key, child in value.items():
            yield from _walk_servers(child, str(child_key))


def _parse_config(raw: str) -> Any:
    parsed = dirty_json.try_parse(raw or "{}")
    if not isinstance(parsed, (dict, list)):
        raise ValueError("MCP config must be a JSON object or array.")
    return parsed


def _find_server(parsed: Any, server_name: str) -> tuple[str, dict[str, Any]]:
    target = _normalize_name(server_name)
    for key, entry in _walk_servers(parsed):
        candidates = (
            key,
            entry.get("name"),
            entry.get("displayName"),
            entry.get("id"),
        )
        if target in {_normalize_name(candidate) for candidate in candidates if candidate}:
            return key, entry
    raise ValueError(f'MCP server "{server_name}" was not found.')


def _runtime_name(server: Any) -> str:
    return _normalize_name(getattr(server, "name", ""))


def _disconnected_name(item: dict[str, Any]) -> str:
    config = item.get("config") if isinstance(item.get("config"), dict) else {}
    return _normalize_name(item.get("name") or config.get("name"))


def _instance_lock():
    lock = getattr(MCPConfig, "_MCPConfig__lock", None)
    return lock if lock is not None else nullcontext()


async def toggle_server(raw_config: str, server_name: str, disabled: bool) -> dict[str, Any]:
    parsed = _parse_config(raw_config)
    key, entry = _find_server(parsed, server_name)
    entry["disabled"] = bool(disabled)
    formatted = json.dumps(parsed, indent=2)

    # Persist without invoking settings' global MCP reload. Runtime state below is
    # changed for only the selected server.
    set_settings_delta({"mcp_servers": formatted}, apply=False)

    target = _normalize_name(server_name)
    runtime_config = copy.deepcopy(entry)
    runtime_config["name"] = runtime_config.get("name") or key or server_name
    target = _normalize_name(runtime_config["name"]) or target
    instance = MCPConfig.get_instance()

    if disabled:
        with _instance_lock():
            instance.servers = [server for server in instance.servers if _runtime_name(server) != target]
            instance.disconnected_servers = [
                item for item in instance.disconnected_servers if _disconnected_name(item) != target
            ]
            instance.disconnected_servers.append(
                {"config": runtime_config, "error": "Disabled in config", "name": target}
            )
    else:
        runtime_config.pop("disabled", None)
        server_type = MCPServerRemote if runtime_config.get("url") or runtime_config.get("serverUrl") else MCPServerLocal
        server = server_type(runtime_config)
        error = ""
        try:
            await server.initialize()
        except Exception as exc:
            error = str(exc)

        with _instance_lock():
            instance.servers = [existing for existing in instance.servers if _runtime_name(existing) != target]
            instance.disconnected_servers = [
                item for item in instance.disconnected_servers if _disconnected_name(item) != target
            ]
            if error:
                instance.disconnected_servers.append(
                    {"config": runtime_config, "error": error, "name": target}
                )
            else:
                instance.servers.append(server)

    status = next(
        (item for item in instance.get_servers_status() if _normalize_name(item.get("name")) == target),
        {"name": target, "connected": False, "error": "Status unavailable", "tool_count": 0, "has_log": False},
    )
    status["disabled"] = bool(disabled)
    return {
        "ok": not bool(status.get("error")) or bool(disabled),
        "disabled": bool(disabled),
        "config": formatted,
        "status": status,
    }
