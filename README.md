# a0-plugins

Polished plugin collection for [Agent Zero](https://github.com/frdel/agent-zero) runtimes.

## Plugins

| Plugin | Description |
|--------|-------------|
| [enhanced_mcp_config](plugins/enhanced_mcp_config/) | Normalizes `disabled` flags in MCP server entries and preserves toggle state in JSON-backed MCP configuration. |
| [enhanced_speech](plugins/enhanced_speech/) | Kokoro TTS enhancements with dual-voice blending, speed control, and remote worker support. |
| [provider_profiles](plugins/provider_profiles/) | Remembers last-used model per provider, auto-fills local-provider API bases (LM Studio, Ollama), and restores provider-specific selections when switching providers. |

## Installation

Drop a plugin folder into your Agent Zero `plugins/` directory (or `usr/plugins/` for user-space plugins):

```bash
cp -r plugins/<plugin-name> /path/to/agent-zero/plugins/<plugin-name>
```

Restart Agent Zero to activate the plugin.

## Monorepo + Per-Plugin Repos

This repo is a monorepo that syncs to individual per-plugin GitHub repos:

```bash
# Sync each plugin to its own repo under Omni-NexusAI
./sync-to-repos.sh
```

## License

[MIT](LICENSE)
