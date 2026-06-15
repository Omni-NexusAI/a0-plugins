from __future__ import annotations

import importlib.util
from pathlib import Path

from helpers.extension import Extension


def _load_overlay_helper():
    plugin_root = Path(__file__).resolve().parents[3]
    helper_path = plugin_root / "helpers" / "overlay.py"
    spec = importlib.util.spec_from_file_location("agentspine_enhanced_mcp_overlay", helper_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load enhanced MCP overlay helper from {helper_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EnhancedMcpConfigInit(Extension):
    def execute(self, **kwargs):
        changed = _load_overlay_helper().apply_overrides()
        if getattr(self, "agent", None):
            self.agent.set_data(
                "enhanced_mcp_config_plugin",
                {"loaded": True, "overrides_changed": changed},
            )
