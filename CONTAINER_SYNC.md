# Container Sync State

## Source

- Container name: `agentspine-gpu-pre`
- Container ID: `ea634265aca0b0e2567383caf1bc3e8380272566ae59fe08b745adda4ed48c17`
- Container image ID: `sha256:1697f0cfb1f4114e8e554d02c84c3a86d6ab8c570b7d02c60a260f8dd7580e9a`
- Sync date: `2026-06-15`
- Source path: `/a0/plugins`

## Synced Plugin Directories

These directories were copied from the container and cleaned of bytecode caches:

- `plugins/_agentspine_identity`
- `plugins/_enhanced_mcp_config`
- `plugins/_enhanced_speech`
- `plugins/_multi_source_updater`

Each synced manifest reports version `0.9.9`.

## Behavior Payloads

Some feature behavior in the GPU-pre container is baked into core runtime files
rather than the plugin directories themselves. The monorepo plugin packages now
include those copied files under `overrides/a0` and apply them at startup:

- `_enhanced_speech`: `helpers/settings.py`, `helpers/build_type.py`,
  `helpers/kokoro_tts.py`, and speech settings UI.
- `_enhanced_mcp_config`: MCP API handlers, `helpers/mcp_handler.py`,
  `helpers/settings.py`, and MCP settings UI.
- `_multi_source_updater`: `helpers/self_update.py`, `helpers/settings.py`,
  and self-update UI/store files.

## Not Present In This Container

- `_provider_profiles` was not present under `/a0/plugins`, `/a0/usr/plugins`, or `/a0/usr/plugins_disabled` in this container state.
- `plugins/provider_profiles` remains in this monorepo as portable plugin source. Its behavior mirrors the provider-history logic found in the container's built-in `_model_config` plugin.

## Maintenance Rules

- Treat the four underscore-prefixed plugin directories as the installed Agentspine GPU-pre state until a newer container sync or deliberate upgrade replaces them.
- Keep underscore directory names unless all manifest names, imports, deployment paths, and docs are updated together.
- Do not commit container-generated `__pycache__` or `.pyc` files.
