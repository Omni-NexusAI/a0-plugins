# Agentspine Identity DOX

## Purpose

`_agentspine_identity` is the built-in Agentspine branding and identity overlay. It keeps the host runtime close to upstream Agent Zero while applying Agentspine product naming, greeting text, banners, document title, and version labels at runtime.

## Ownership

- `plugin.yaml` owns the installed plugin identity and `0.9.9` version.
- `default_config.yaml` owns product names, release prefixes, compatibility label, and release-tag defaults.
- `helpers/identity.py` owns Python-side text replacement, release-tag normalization, timestamp formatting, and display-version formatting.
- `extensions/python/agent_init/_10_initial_message.py` owns the branded first message for agent `0` when the context log is empty.
- `extensions/python/banners/_95_agentspine_identity.py` owns banner text replacement.
- `extensions/python/_functions/helpers/ui_server/UiRouteHandlers/serve_index/end/_10_agentspine_index_identity.py` owns server-side index HTML/title/version rewriting.
- `extensions/webui/page-head/_10_agentspine_identity.html` owns browser-side DOM, title, sidebar version, and attribute text replacement.

## Local Contracts

- Built-in source is `/a0/plugins/_agentspine_identity`; runtime configuration is `/a0/usr/plugins/_agentspine_identity/config.json`.
- Target compatibility is A0 `M v1.20` with Agentspine `v0.9.9-standard-pre`; never rewrite `/api/health` metadata.
- Preserve protected phrases such as `Agent Zero Venice`.
- Keep Python and WebUI replacement tables aligned when adding or changing identity strings.
- Keep release-tag behavior aligned between `default_config.yaml`, `helpers/identity.py`, and the index/page-head hooks.
- The default development banner prefix is `D`; do not change it without updating docs and config together.
- Imports depend on the installed directory name `plugins._agentspine_identity`; do not rename the folder without updating imports.

## Work Guidance

- Text replacement must be idempotent and safe when hooks run repeatedly.
- DOM replacement must skip script/style/code/pre/textarea/input content.
- Server-side index rewriting should preserve existing explicit `D`, `M`, or `AS` display labels.
- Branding should be broad enough for runtime surfaces but narrow enough to avoid corrupting protected product names.

## Verification

- Parse touched Python files.
- Load the WebUI and verify document title, sidebar version, first-run message, banners, and visible Agent Zero strings are rewritten as expected.
- Verify protected phrases remain unchanged.

## Child DOX Index

This plugin has no child DOX files.
