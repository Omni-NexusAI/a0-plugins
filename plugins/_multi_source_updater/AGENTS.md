# Multi Source Updater DOX

## Purpose

`_multi_source_updater` is the built-in Agentspine updater enhancement plugin synced from the GPU-pre container. In this container state it is primarily a manifest/documentation package with an agent-init extension stub.

## Ownership

- `plugin.yaml` owns plugin identity, version `0.9.9`, always-enabled behavior, and `backup` settings-section placement.
- `README.md` owns the intended updater behavior: selectable update source, persisted source, and Agentspine compatibility display behavior.
- `extensions/python/agent_init/_10_multi_source_updater.py` owns the current runtime hook; it intentionally returns without patching in this snapshot.
- `webui/thumbnail.svg` owns the plugin thumbnail asset.

## Local Contracts

- Treat the current no-op runtime hook as the container-synced behavior until implementing a deliberate upgrade.
- Keep the manifest name `_multi_source_updater` aligned with the installed directory name.
- Future updater behavior must preserve existing settings and avoid forcing a source switch without explicit user intent.
- Do not claim active source-switching implementation in docs until the behavior exists in source.

## Work Guidance

- Future updater code should separate source selection, persistence, display labels, and update execution.
- Source metadata should stay explicit enough that agents can tell whether Omni-NexusAI or agent0ai is active.
- Keep updater changes plugin-local unless the user explicitly requests host-runtime edits.

## Verification

- Parse touched Python files.
- For future behavior changes, verify source selection persistence, display labels, fallback behavior, and unsupported host behavior.

## Child DOX Index

This plugin has no child DOX files.
