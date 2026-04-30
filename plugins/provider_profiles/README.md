# Provider Profiles

Portable Agent Zero plugin that adds provider-aware model memory to the model configurator.

## What it does

- **Remembers your last model per provider** — when you switch from OpenAI to Ollama and back, your previously selected OpenAI model is automatically restored.
- **Auto-fills local provider API bases** — LM Studio and Ollama endpoints are populated automatically when you select those providers.
- **Clears stale model names** — switching to a provider with no saved selection blanks the model field so you start fresh.

## Compatibility

- Agent Zero runtime with the v1.7+ plugin loader and `_model_config` UI store.
- Gracefully degrades on unsupported hosts: the plugin waits for `$store.modelConfig` and exits silently if it is unavailable.
- No dependency on external modules or identity systems.

## Installation

1. Copy the `provider_profiles` folder into your Agent Zero `plugins_custom/` directory.
2. Restart Agent Zero (or reload plugins from the UI).
3. The provider select dropdowns in the model configurator will now persist and restore model selections automatically.

## Configuration

Defaults can be overridden via `default_config.yaml`:

| Key | Default | Description |
|---|---|---|
| `history_storage_key` | `modelConfig_providerHistory` | localStorage key for provider history |
| `local_provider_defaults.lm_studio` | `http://host.docker.internal:1234/v1` | Auto-filled API base for LM Studio |
| `local_provider_defaults.ollama` | `http://host.docker.internal:11434` | Auto-filled API base for Ollama |
| `clear_stale_model_on_new_provider` | `true` | Clear model name when switching to a provider with no saved selection |

## License

MIT
