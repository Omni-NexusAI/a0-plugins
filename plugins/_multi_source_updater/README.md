# Multi Source Updater

Built-in Agentspine self-update enhancement plugin.

This directory is synced from the `agentspine-gpu-pre` container state on
2026-06-15. The manifest version is `0.9.9` and the installed plugin name is
`_multi_source_updater`.

## Purpose

The plugin provides the Agentspine updater enhancement boundary:

- selecting update source between Omni-NexusAI and agent0ai;
- preserving the selected update source in persisted settings;
- providing Agentspine v0.9.9-pre compatibility display behavior.

## Design

In the live GPU container, updater behavior is baked into core helper, settings,
and WebUI files. The monorepo plugin vendors those files under `overrides/a0`
and applies them on agent startup.

- `extensions/python/agent_init/_10_multi_source_updater.py` applies the
  override payload and records changed files on the agent.
- `helpers/overlay.py` copies changed files from `overrides/a0` into the runtime
  root.
- `overrides/a0/helpers/self_update.py` contains update-source selection logic.
- `overrides/a0/helpers/settings.py` contains the `self_update_source` setting
  and updater cache invalidation behavior.
- `overrides/a0/webui/components/settings/external/` contains the self-update
  store and modal with the update-source selector.

## Function

After startup applies the payload, the self-update flow behaves like the GPU
container:

- update sources are `omni-nexusai` and `agent0ai`;
- default source is `omni-nexusai`;
- `self_update_source` is persisted in settings;
- remote URL selection follows the active source;
- release/tag listing follows the active source;
- Omni-NexusAI source uses Agentspine preview display behavior;
- self-update caches are invalidated when the source changes.

## Current Limits

The override payload intentionally matches the GPU container. It is more
invasive than a pure extension because self-update behavior currently depends on
core helper and settings files.

## Verification

- Parse the Python extension, helper, and override Python files.
- Verify source selection persistence, display labels, fallback behavior, and
  unsupported host behavior.
