# Enhanced MCP Configurator

Built-in Agentspine MCP configuration enhancement plugin.

This directory is synced from the `agentspine-gpu-pre` container state on
2026-06-15. The manifest version is `0.9.9` and the installed plugin name is
`_enhanced_mcp_config`.

## Purpose

The plugin provides the Agentspine MCP settings enhancement boundary:

- per-server enable/disable toggle controls;
- refined MCP server status handling in settings;
- safer apply/toggle update flow for MCP server configuration.

## Design

In the live GPU container, this behavior is baked into core API, helper, and
WebUI files. The monorepo plugin vendors those files under `overrides/a0` and
applies them on agent startup.

- `extensions/python/agent_init/_10_enhanced_mcp_config.py` applies the override
  payload and records changed files on the agent.
- `helpers/overlay.py` copies changed files from `overrides/a0` into the runtime
  root.
- `overrides/a0/api/` contains the MCP status, apply, toggle, log, and detail
  API handlers.
- `overrides/a0/helpers/mcp_handler.py` contains the container MCP handler with
  `disabled` server support.
- `overrides/a0/helpers/settings.py` contains the container settings schema and
  MCP reload behavior.
- `overrides/a0/webui/components/settings/mcp/` contains the enhanced MCP
  settings modal, status list, toggle UI, examples, log view, and detail view.

## Function

After startup applies the payload, the MCP modal behaves like the GPU container:

- every discovered server entry receives a `disabled` field if one is missing;
- toggling a server updates the JSON editor immediately;
- the status row reflects the disabled state immediately and marks disabled
  servers disconnected;
- the toggle is disabled while an apply operation is running;
- toggles are applied through `mcp_servers_toggle`;
- full config applies are normalized and sent through `mcp_servers_apply`;
- status polling pauses during apply and restarts afterward.

## Current Limits

The override payload intentionally matches the GPU container. It is more
invasive than a pure WebUI extension because the behavior currently depends on
core API handlers and helper files.

## Verification

- Parse the Python extension, helper, API handlers, and override Python files.
- Test empty config, existing enabled servers, existing disabled servers,
  unknown server keys, and unsupported host settings pages.
