# Provider Profiles

Portable Agent Zero plugin that adds provider-aware model memory to the model
configurator.

## What It Does

- Remembers the last model per provider, so switching away from a provider and
  back restores the provider-specific model.
- Saves and restores `api_base` beside the model name.
- Saves and restores `ctx_length` beside the model name.
- Auto-fills local provider API bases for LM Studio and Ollama.
- Clears stale model names when switching to a provider with no saved selection.

Saved provider history entries use this shape:

```json
{
  "name": "model-name",
  "api_base": "http://host.docker.internal:1234/v1",
  "ctx_length": 128000
}
```

## Compatibility

- Agent Zero runtime with the v1.7+ plugin loader and `_model_config` UI store.
- Gracefully degrades on unsupported hosts: the plugin waits for
  `$store.modelConfig` and exits silently if it is unavailable.
- No dependency on external modules or identity systems.

## Installation

1. Copy the `provider_profiles` folder into your Agent Zero `plugins_custom/`
   directory.
2. Restart Agent Zero or reload plugins from the UI.
3. Provider dropdowns in the model configurator will persist and restore model,
   API base, and context length selections automatically.

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
