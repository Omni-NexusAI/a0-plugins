from __future__ import annotations

import importlib.util
from pathlib import Path

from helpers.api import ApiHandler, Request, Response


def _load_toggle_helper():
    helper_path = Path(__file__).resolve().parents[1] / "helpers" / "server_toggle.py"
    spec = importlib.util.spec_from_file_location("agentspine_enhanced_mcp_server_toggle", helper_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load MCP toggle helper from {helper_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ToggleServer(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        server_name = str(input.get("server_name") or "").strip()
        if not server_name:
            return {"ok": False, "error": "server_name is required"}
        try:
            return await _load_toggle_helper().toggle_server(
                str(input.get("mcp_servers") or ""),
                server_name,
                bool(input.get("disabled")),
            )
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
