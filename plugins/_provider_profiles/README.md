# _provider_profiles

Agentspine built-in provider-profile overlay for Agent Zero v1.20.

## Purpose

This plugin preserves model settings per provider and model slot so switching
providers does not lose the previous provider's model, API base, or context
settings.

## Built-In Source And Config

- Built-in source: `/a0/plugins/_provider_profiles`
- User config/state: `/a0/usr/plugins/_provider_profiles/config.json`
- UI target: `_model_config` and the v1.20 `modelConfig` Alpine store

The plugin is an underscore built-in overlay for this repaired standard-pre
runtime. Do not enable a duplicate non-underscore `provider_profiles` custom
plugin beside it.

## Runtime Hooks

- The overlay wraps v1.20 `modelConfig.installSettingsHooks(context)` to retain
  the active plugin settings context. A capture-phase provider change hook maps
  the visible model section to its public config slot, snapshots before the
  native `@change="model.api_base = ''"` handler, then restores in a microtask.
- Local storage is the synchronous UI source of truth; plugin config mirrors the
  same profiles for durable recovery.
- Model search patch supplies local-provider API base defaults when needed.

## Behavior

- Profiles are saved per model slot and provider.
- Legacy `slot:provider` and `slot_provider` keys migrate to schema version 2
  canonical keys without discarding unknown profile fields.
- Saved values include provider, model name, API base, context length/history,
  vision flag, rate limits, and provider kwargs.
- LM Studio defaults to `http://host.docker.internal:1234/v1`.
- Ollama defaults to `http://host.docker.internal:11434`.
- The defaults are exposed through `modelConfig.providerApiBaseDefaults` and
  applied during manual switching, model search, and settings hydration, while
  preserving any non-empty user URL.
- Stale local API bases are cleared when switching to a non-local provider with
  no saved profile.
- Save is single-flight. The core model configuration is persisted first, then
  the profile mirror is debounced, preventing competing `/plugins` writes and
  duplicate modal-close behavior.

## Compatibility Notes

- Target runtime: Agent Zero `M v1.20` with Agentspine
  `v0.9.9-standard-pre`.
- Provider IDs are `lm_studio` and `ollama` in v1.20 `_model_config`.
- The provider hook uses event delegation and the settings context rather than
  Alpine's private `_x_dataStack`, so reopened settings and dynamically
  rendered model slots do not accumulate handlers.

## Test Checklist

- Compile plugin Python files.
- Open Model Configuration without UI freeze.
- Set LM Studio or Ollama API base/model, switch away, then switch back and
  confirm values restore.
- Confirm outgoing provider values are saved before switching.
- Confirm local provider defaults are not accidentally cleared.
