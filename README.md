# a0-plugins

Polished plugin collection for Agent Zero and Agentspine-compatible runtimes.

This monorepo currently includes a container-synced Agentspine GPU-pre plugin
set copied from container
`ea634265aca0b0e2567383caf1bc3e8380272566ae59fe08b745adda4ed48c17`.

## Container-Synced Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| [`_agentspine_identity`](plugins/_agentspine_identity/) | `0.9.9` | Agentspine identity overlay for product naming, first-run greeting text, banners, page title, version display, and runtime text replacement. |
| [`_enhanced_mcp_config`](plugins/_enhanced_mcp_config/) | `0.9.9` | Built-in MCP configuration enhancement placeholder for the Agentspine MCP settings surface. |
| [`_enhanced_speech`](plugins/_enhanced_speech/) | `0.9.9` | Enhanced speech support with remote Kokoro worker detection/defaults and a WebUI STT recorder patch. |
| [`_multi_source_updater`](plugins/_multi_source_updater/) | `0.9.9` | Built-in updater enhancement placeholder for multi-source update behavior in Agentspine builds. |

## Additional Plugin Sources

| Plugin | Status |
|--------|--------|
| [`provider_profiles`](plugins/provider_profiles/) | Existing upstream portable plugin. `_provider_profiles` was not present in the synced GPU-pre container, so this directory should not be treated as container-matched until it is deployed and re-synced. |

## Installation

Drop a plugin folder into an Agent Zero-compatible plugin directory:

```bash
cp -r plugins/<plugin-name> /path/to/agent-zero/plugins/<plugin-name>
```

The underscore-prefixed Agentspine plugins are copied with their installed
runtime names. Keep those directory names unless the manifest and import paths
are updated together.

## Maintenance

- `CONTAINER_SYNC.md` records the container snapshot used for this sync.
- `AGENTS.md` files implement DOX guidance for the repo, `plugins/`, and each
  plugin boundary.
- Do not commit runtime bytecode caches, logs, secrets, or local settings.

## Monorepo + Per-Plugin Repos

This repo can sync individual plugin folders into per-plugin GitHub repos:

```bash
./sync-to-repos.sh
```

## License

[MIT](LICENSE)
