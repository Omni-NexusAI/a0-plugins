# Enhanced MCP Configurator

Built-in Agentspine MCP configuration enhancement plugin.

This directory is copied from the `agentspine-gpu-pre` container state synced on
2026-06-15. The manifest version is `0.9.9` and the installed plugin name is
`_enhanced_mcp_config`.

## Purpose

The plugin represents the Agentspine MCP settings enhancement boundary. The
manifest places it in the `mcp` settings section and describes the intended
feature set:

- per-server enable/disable toggle controls;
- refined MCP server status handling in settings;
- safer apply/toggle update flow for MCP server configuration.

## Design

In this container state, the implementation is intentionally minimal:

- `plugin.yaml` declares the always-enabled plugin and MCP settings placement.
- `extensions/python/agent_init/_10_enhanced_mcp_config.py` defines the runtime
  extension class and returns without modifying the host.
- `webui/thumbnail.svg` provides the plugin asset.

This makes the plugin a durable placeholder and documentation boundary for the
MCP configuration work that exists in or around the current Agentspine runtime.

## Function

At startup, Agent Zero's plugin framework can load `EnhancedMcpConfigInit`, but
the extension does not patch settings, files, routes, or WebUI state in this
snapshot.

Future implementation should preserve unknown MCP server keys, avoid destructive
config rewrites, and make server disabled/enabled state explicit in persisted
configuration.

## Current Limits

The manifest and README describe the intended MCP enhancement surface, but the
current copied code is a no-op. Do not assume active toggle UI or config
mutation exists until source code is added.

## Verification

- Parse the Python extension after edits.
- For future behavior, test empty config, existing enabled servers, existing
  disabled servers, unknown server keys, and unsupported host settings pages.
