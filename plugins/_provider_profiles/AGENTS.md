# Provider Profiles DOX

## Purpose

`_provider_profiles` owns provider-specific model-slot restoration for the Agentspine v1.20 model configurator.

## Contracts

- Built-in source is `/a0/plugins/_provider_profiles`; durable mirror state is `_provider_profiles/config.json`.
- Bind through `modelConfig.installSettingsHooks(context)` and visible model-section ownership; never depend on Alpine `_x_dataStack`.
- Preserve every non-private model field and unknown profile keys.
- Schema version 2 accepts both legacy colon keys and underscore keys.
- LM Studio and Ollama defaults must not leak into non-local providers.
- Canonical local URLs are store-owned defaults applied on provider change, model search, and settings hydration: LM Studio `http://host.docker.internal:1234/v1`; Ollama `http://host.docker.internal:11434`.
- Core `_model_config` Save completes before the profile mirror is scheduled; concurrent Save submissions must collapse into one operation.

## Compatibility And Verification

- Target A0 `M v1.20`, Agentspine `v0.9.9-standard-pre`.
- Switch each model slot away and back, save/reopen, and restart; verify provider, model, API base, context, and kwargs restore.
- Explicitly test LM Studio and Ollama defaults and a non-local provider after each.
