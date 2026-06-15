# Enhanced MCP Config DOX

## Purpose

`enhanced_mcp_config` owns portable MCP server configuration improvements for compatible Agent Zero runtimes.

## Ownership

- `README.md` owns user-facing behavior and compatibility.
- `default_config.yaml` owns normalization/toggle settings such as `normalize_disabled_flags`, `reflect_toggle_status`, and `apply_delay_ms`.
- WebUI/runtime extension files own Alpine `mcpServersStore` patching when available.

## Local Contracts

- Preserve unknown MCP server config keys.
- Normalize missing `disabled` flags without changing unrelated server configuration.
- Keep toggle persistence explicit and reversible.
- Degrade safely when the target MCP store is absent.

## Work Guidance

- Keep MCP config transformations small and data-preserving.
- Document any new config key in README and `default_config.yaml`.
- Avoid mixing MCP config behavior with bridge routing, model config, or updater behavior.

## Verification

- Test missing `disabled` flags and existing `disabled` flags.
- Toggle a server and confirm only the intended flag changes.
- Load on an unsupported host and confirm no unhandled WebUI errors.

## Child DOX Index

This plugin has no child DOX files.
