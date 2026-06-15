# Agentspine Identity Module

Built-in identity overlay for Agentspine.

This directory is copied from the `agentspine-gpu-pre` container state synced on
2026-06-15. The manifest version is `0.9.9` and the installed plugin name is
`_agentspine_identity`.

## Purpose

`_agentspine_identity` keeps the core application close to upstream Agent Zero
while applying Agentspine product identity at runtime. It is always enabled in
Agentspine builds and is not intended as a marketplace plugin.

The overlay affects:

- first-run assistant greeting text;
- banners returned through the banner extension point;
- served index HTML title and version bootstrap data;
- browser-side document title, sidebar version label, visible text nodes, and
  selected accessibility/title attributes.

## Design

The Python helper `helpers/identity.py` is the shared identity engine. It owns:

- default product and release metadata;
- lightweight YAML loading from `default_config.yaml`;
- release-tag normalization;
- timestamp formatting;
- display-version formatting;
- protected phrase handling;
- Agent Zero to Agentspine text replacement.

Runtime hooks use that helper in separate surfaces:

- `extensions/python/agent_init/_10_initial_message.py` rewrites the initial
  prompt message for the main agent when the conversation log is empty.
- `extensions/python/banners/_95_agentspine_identity.py` rewrites banner title,
  HTML, and message strings.
- `extensions/python/_functions/helpers/ui_server/UiRouteHandlers/serve_index/end/_10_agentspine_index_identity.py`
  rewrites served HTML title and `globalThis.gitinfo` version bootstrap data.
- `extensions/webui/page-head/_10_agentspine_identity.html` applies browser-side
  replacement after page load and later DOM mutations.

## Function

The default release banner is based on `default_config.yaml`:

- standard pre-release: `v0.9.9-standard-pre`
- GPU pre-release: `v0.9.9-gpu-pre`
- default banner prefix: `D`

The server-side index hook uses `BUILD_VARIANT=fullgpu` or `BUILD_VARIANT=gpu`
to select the GPU pre-release tag; otherwise it uses the standard pre-release
tag. Existing labels that already start with `D `, `M `, or `AS ` are preserved.

The browser-side hook repeats identity replacement in the DOM, patches the
Alpine sidebar version store when available, updates `globalThis.gitinfo`, and
observes later DOM mutations so delayed UI content is also rewritten.

## Guardrails

The phrase `Agent Zero Venice` is protected and restored after replacement.
Browser-side replacement skips `SCRIPT`, `STYLE`, `CODE`, `PRE`, `TEXTAREA`, and
`INPUT` elements.

## Verification

- Parse the Python files after backend changes.
- Verify the first-run greeting is branded only for agent `0` and only when the
  context log is empty.
- Verify document title, sidebar version, banners, and visible text are branded.
- Verify protected phrases remain unchanged.
