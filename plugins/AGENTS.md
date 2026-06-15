# Plugins DOX

## Purpose

`plugins/` contains portable Agent Zero plugin packages. Each child plugin folder should be understandable and installable on its own.

## Ownership

- `README.md` explains user-facing purpose, compatibility, installation, and configuration.
- `default_config.yaml` owns plugin defaults where present.
- `plugin.yaml` or equivalent manifests own plugin identity where present.
- `extensions/` owns runtime hooks loaded by the Agent Zero plugin framework.
- `helpers/`, `api/`, and `webui/` own plugin-local backend, route, and UI assets where present.

## Local Contracts

- Read this file and the target plugin's `AGENTS.md` before editing a plugin.
- Keep each plugin self-contained enough to sync into its own repository.
- Keep runtime patches idempotent; WebUI hooks may run after Alpine init, DOMContentLoaded, and later DOM mutations.
- Do not introduce dependencies on Agentspine-only paths unless the plugin doc explicitly calls that out.
- Document compatibility gaps instead of silently relying on a specific local runtime.

## Work Guidance

- Put host-store patches in WebUI extension files with clear guards.
- Put reusable backend behavior in helpers rather than embedding it in route handlers.
- Prefer explicit defaults and migration helpers over implicit UI-only defaults.
- Keep UI classes and label formats documented when other agents need to reproduce a design.

## Verification

- Confirm plugin files can be copied independently.
- Verify unsupported hosts do not throw unhandled errors during startup or page load.
- Check that README, DOX, and default config agree after changes.

## Child DOX Index

- `enhanced_mcp_config/AGENTS.md`: MCP server disabled-flag normalization and toggle preservation.
- `enhanced_speech/AGENTS.md`: Kokoro TTS settings, dual-voice blending, remote worker support, and voice selector UI contract.
- `provider_profiles/AGENTS.md`: provider-aware model selection memory and local-provider defaults.
