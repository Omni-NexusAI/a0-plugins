# Enhanced MCP Configurator

A portable Agent Zero plugin that normalizes `disabled` flags in MCP server entries and preserves toggle state in JSON-backed MCP server configuration.

## Features

- **Disabled-flag normalization** – Ensures every MCP server entry has an explicit `disabled` field, eliminating silent defaults and making configuration state unambiguous.
- **Toggle preservation** – Toggles the `disabled` flag on named servers while keeping the rest of the configuration intact.
- **Runtime patching** – Hooks into the Alpine.js `mcpServersStore` at runtime when available; silently does nothing on hosts without that store.

## Compatibility

- Agent Zero runtimes with the v1.7+ plugin loader and MCP settings store.
- Safe on unsupported hosts: the plugin only patches when `$store.mcpServersStore` is present.

## Installation

1. Copy this directory into your Agent Zero `plugins_custom/` folder.
2. Restart the Agent Zero runtime.
3. The plugin activates automatically on the next agent initialization.

## Configuration

Settings are stored in `default_config.yaml`:

| Key | Default | Description |
|-----|---------|-------------|
| `normalize_disabled_flags` | `true` | Normalize missing `disabled` flags in server entries |
| `reflect_toggle_status` | `true` | Persist toggle state changes back to the config |
| `apply_delay_ms` | `120` | Delay in ms before applying store patches |

## License

MIT
