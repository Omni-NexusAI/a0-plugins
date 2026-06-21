# _multi_source_updater

Agentspine built-in multi-source self-updater overlay for Agent Zero v1.20.

## Purpose

This plugin lets the updater choose between upstream Agent Zero and Agentspine
sources while preserving truthful runtime health metadata.

## Built-In Source And Config

- Built-in source: `/a0/plugins/_multi_source_updater`
- User config/state: `/a0/usr/plugins/_multi_source_updater/config.json`
- Pending update payload: Agent Zero self-update request file managed by
  `helpers.self_update`

The plugin is an underscore built-in overlay. Do not enable a duplicate custom
updater plugin beside it.

## Runtime Hooks

- `agent_init` patches `helpers.self_update` branch/tag lookup, update info, and
  scheduling behavior.
- Page-head UI patch adds the update-source selector and refreshes branch/tag
  choices for the selected source.
- Scheduled payloads include `update_source`, `remote_url`, selected branch,
  selected tag, and diagnostic source version fields.

## Behavior

- Upstream `agent0ai` source uses real upstream tags and real current version.
- Agentspine `omni-nexusai` source treats this standard-pre build as effective
  current/latest `v0.9.9-standard-pre`.
- Legacy `v0.9.8-custom` may appear as old history but must not be offered as a
  backward latest target for this build.
- Spoofing is source-scoped and must not alter `/api/health`.

## Compatibility Notes

- Target runtime: Agent Zero `M v1.20` with Agentspine
  `v0.9.9-standard-pre`.
- Agentspine tags use `standard`, `standard-pre`, `gpu`, and `gpu-pre`; the
  retired `custom` suffix is legacy-only.

## Test Checklist

- Compile plugin Python files.
- Confirm `/api/health` still reports actual Agent Zero `M v1.20`.
- Switch updater source to Agentspine and confirm current/latest displays
  `v0.9.9-standard-pre`.
- Switch updater source to upstream and confirm upstream tags remain available.
- Dry-run schedule and confirm payload includes selected source, remote URL, and
  `agentspine_effective_current_tag: v0.9.9-standard-pre`.
