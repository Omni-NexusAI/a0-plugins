# Provider Profiles DOX

## Purpose

`provider_profiles` owns provider-aware model memory for compatible Agent Zero model configuration UIs.

## Ownership

- `README.md` owns user-facing behavior and compatibility.
- `default_config.yaml` owns storage keys, local-provider defaults, and stale-model clearing behavior.
- WebUI/runtime extension files own patching of `_model_config` / `modelConfig` behavior when available.

## Local Contracts

- Preserve model selections per provider.
- Preserve local-provider API base defaults for LM Studio and Ollama unless config changes them.
- Clear stale model names only when the plugin config says to do so.
- Degrade safely when the target model config store is absent.

## Work Guidance

- Keep provider history storage key configurable.
- Preserve unknown model/provider fields when saving history.
- Keep local-provider defaults in config and docs aligned.

## Verification

- Switch from one provider to another and back; verify prior model selection restores.
- Select LM Studio or Ollama and verify API base defaults are populated.
- Switch to a provider with no saved selection and verify stale model clearing follows config.
- Load on an unsupported host and confirm no unhandled WebUI errors.

## Child DOX Index

This plugin has no child DOX files.
