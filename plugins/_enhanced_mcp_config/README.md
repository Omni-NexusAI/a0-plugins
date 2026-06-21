# _enhanced_mcp_config

Agentspine built-in MCP configuration overlay for Agent Zero v1.20.

## Purpose

This plugin restores Agentspine MCP quality-of-life controls on top of the
v1.20 `mcpServersStore`: reliable enable/disable toggles and safe JSON
normalization for server entries.

## Built-In Source And Config

- Built-in source: `/a0/plugins/_enhanced_mcp_config`
- User config/state: `/a0/usr/plugins/_enhanced_mcp_config/config.json`
- MCP data target: the active Agent Zero MCP settings JSON managed by
  `mcpServersStore`

The plugin is an underscore built-in overlay. Do not enable a duplicate
non-underscore `enhanced_mcp_config` custom plugin beside it.

## Runtime Hooks

- Page-head UI patch waits for `mcpServersStore`, patches store methods once,
  and injects per-server toggles into MCP server rows.
- Store patch normalizes every server entry to include an explicit boolean
  `disabled` value before formatting or applying JSON.

## Behavior

- Toggle controls call the plugin-local `toggle_server` API. It persists with
  `apply=False` and mutates only the selected `MCPConfig` server.
- Enabling initializes only the selected server; disabling removes only that
  server from the active runtime list. Full JSON Apply remains the explicit
  all-server reload operation.
- Invalid JSON reports a parse error and leaves the existing configuration
  intact.
- Missing `disabled` fields are persisted as `false`; existing values are
  coerced to booleans.
- Server rows use the Agentspine green/gray switch treatment and keep log/tool
  controls aligned in a dedicated action group.
- Status refreshes re-read disabled state from the editor, so backend polling
  cannot visually undo an unapplied or newly applied toggle.

## Compatibility Notes

- Target runtime: Agent Zero `M v1.20` with Agentspine
  `v0.9.9-standard-pre`.
- The page-head patch is guarded globally, patches the store once, and throttles
  DOM work to one animation frame so Settings can open repeatedly without
  accumulating status loops or duplicate controls.

## Test Checklist

- Compile plugin Python files.
- Open Settings and MCP configuration without UI freeze.
- Toggle at least one server off and on; confirm JSON updates and persists.
- Confirm sibling server rows and backend connections do not reload during a
  single-server toggle.
- Enter invalid JSON and confirm the error is surfaced without losing config.
- Reload Settings and confirm `disabled` values remain explicit booleans.
