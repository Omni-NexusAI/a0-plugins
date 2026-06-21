# Enhanced MCP Config DOX

## Purpose

`_enhanced_mcp_config` owns Agentspine's v1.20 MCP JSON safety and per-server runtime toggles.

## Contracts

- Built-in source is `/a0/plugins/_enhanced_mcp_config`; `/a0/usr/plugins/_enhanced_mcp_config` is hotfix/config staging only.
- `api/toggle_server.py` and `helpers/server_toggle.py` persist with `apply=False` and mutate only the selected `MCPConfig` entry.
- Full JSON Apply intentionally remains the only all-server reload path.
- Preserve unknown server keys and normalize `disabled` to a boolean.
- The page-head observer must remain scoped and idempotent.

## Compatibility And Verification

- Target A0 `M v1.20`, Agentspine `v0.9.9-standard-pre`.
- Compile Python, syntax-check page-head JavaScript, toggle one server off/on, and confirm sibling rows and connections do not refresh.
- Test malformed JSON and verify the last valid editor value survives.
