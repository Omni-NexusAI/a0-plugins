# Multi Source Updater DOX

## Purpose

`_multi_source_updater` is the built-in Agentspine updater enhancement plugin synced from the GPU-pre container. The container behavior lives in core helper/settings/WebUI files, so this plugin vendors those files under `overrides/a0` and applies them at startup.

## Ownership

- `plugin.yaml` owns plugin identity, version `0.9.9`, always-enabled behavior, and `backup` settings-section placement.
- `README.md` owns the intended updater behavior: selectable update source, persisted source, and Agentspine compatibility display behavior.
- `extensions/python/agent_init/_10_multi_source_updater.py` owns startup application of the override payload.
- `helpers/overlay.py` owns copying changed override files into the runtime root.
- `overrides/a0/helpers/self_update.py` owns source-aware updater behavior copied from the container.
- `overrides/a0/helpers/settings.py` owns the `self_update_source` setting and updater cache invalidation copied from the container.
- `overrides/a0/webui/components/settings/external/` owns the update-source UI copied from the container.
- `webui/thumbnail.svg` owns the plugin thumbnail asset.

## Local Contracts

- Treat `overrides/a0` as the container-synced behavior payload.
- Keep the manifest name `_multi_source_updater` aligned with the installed directory name.
- Future updater behavior must preserve existing settings and avoid forcing a source switch without explicit user intent.
- Do not edit copied override files without checking the matching container/source behavior or intentionally upgrading the plugin.

## Work Guidance

- Future updater code should separate source selection, persistence, display labels, and update execution.
- Source metadata should stay explicit enough that agents can tell whether Omni-NexusAI or agent0ai is active.
- Keep updater changes plugin-local unless the user explicitly requests host-runtime edits.

## Verification

- Parse touched Python files, including override helper files.
- For future behavior changes, verify source selection persistence, display labels, fallback behavior, and unsupported host behavior.

## Child DOX Index

This plugin has no child DOX files.
