# Agentspine Built-In Plugin Sync

## Current Compatibility

- Validated container: `agentspine-standard-pre`
- Agent Zero runtime: `M v1.20`
- Agentspine release line: `v0.9.9-standard-pre`
- Validation date: `2026-06-20`
- Baked source path: `/a0/plugins`
- Live hotfix path: `/a0/usr/plugins`

## Synced Plugin Directories

The Agentspine distribution owns these five underscore-prefixed built-ins:

- `plugins/_agentspine_identity`
- `plugins/_enhanced_mcp_config`
- `plugins/_enhanced_speech`
- `plugins/_multi_source_updater`
- `plugins/_provider_profiles`

Each package has its own README and `AGENTS.md` covering hooks, configuration, compatibility, failure behavior, and tests.

## Packaging Contract

- The repaired `_enhanced_speech`, `_enhanced_mcp_config`, `_provider_profiles`, `_agentspine_identity`, and `_multi_source_updater` packages use their v1.20 built-in layouts. Do not restore the old speech, MCP, or updater `overrides/a0` payload trees.
- Use `/a0/usr/plugins/<id>` only for reversible live validation. After acceptance, mirror the same package into the Agentspine repository's `plugins/<id>` directory and this monorepo.
- Keep underscore IDs aligned across directory names, manifests, imports, documentation, and deployment paths.
- Runtime configuration belongs in the live plugin config files and must not be copied back into source packages.

## Maintenance Rules

- Treat the five underscore-prefixed plugin directories as the maintained Agentspine built-in overlay set.
- Keep underscore directory names unless all manifest names, imports, deployment paths, and docs are updated together.
- Do not commit container-generated `__pycache__` or `.pyc` files.
- Validate changes against both truthful upstream health metadata and the source-scoped Agentspine compatibility version.
