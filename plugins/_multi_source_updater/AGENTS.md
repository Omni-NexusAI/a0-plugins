# Multi Source Updater DOX

## Purpose

`_multi_source_updater` is the built-in source-aware updater compatibility layer for A0 v1.20 and Agentspine v0.9.9-standard-pre.

## Ownership

- `plugin.yaml` owns plugin identity, version `0.9.9`, always-enabled behavior, and `backup` settings-section placement.
- `README.md` owns the intended updater behavior: selectable update source, persisted source, and Agentspine compatibility display behavior.
- `helpers/source.py` owns source selection, source-keyed branch/tag caches, Agentspine effective-version behavior, and pending update payloads.
- `api/source.py` owns reading and persisting the selected update source.
- `extensions/python/agent_init/_10_multi_source_updater.py` owns runtime updater patch installation.
- `extensions/python/startup_migration/_10_multi_source_updater.py` owns config migration.
- `extensions/webui/page-head/_10_multi_source_updater.html` owns the source selector and source-aware refresh behavior.

## Local Contracts

- Keep the manifest name `_multi_source_updater` aligned with the installed directory name.
- Keep upstream health/version metadata truthful; the `v0.9.9-standard-pre` effective version applies only to the Agentspine source.
- Scheduled update payloads must preserve source, remote URL, branch, tag, build flavor, and effective Agentspine version.
- Source changes must invalidate only the matching source caches and must not force a source switch without explicit user intent.

## Work Guidance

- Future updater code should separate source selection, persistence, display labels, and update execution.
- Source metadata should stay explicit enough that agents can tell whether Omni-NexusAI or agent0ai is active.
- Keep updater changes plugin-local unless the user explicitly requests host-runtime edits.

## Verification

- Parse plugin Python and page-head JavaScript.
- Verify Agentspine and upstream source switching, source-keyed branches/tags, source persistence, and dry-run payload metadata.
- Confirm Agentspine reports `v0.9.9-standard-pre` as effective current/latest while `/api/health` remains truthful `M v1.20`.

## Child DOX Index

This plugin has no child DOX files.
