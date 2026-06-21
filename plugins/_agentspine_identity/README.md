# _agentspine_identity

Agentspine built-in identity overlay for Agent Zero v1.20.

## Purpose

This plugin applies visible Agentspine branding and links while preserving the
truthful upstream Agent Zero runtime identity exposed by health metadata.

## Built-In Source And Config

- Built-in source: `/a0/plugins/_agentspine_identity`
- User config/state: `/a0/usr/plugins/_agentspine_identity/config.json`

The plugin is an underscore built-in overlay. Do not enable a duplicate custom
identity plugin beside it.

## Runtime Hooks

- Page-head and banner hooks patch visible UI labels and links.
- Agent initialization hook exposes identity defaults to Agentspine-specific UI
  surfaces.
- Helper code keeps branding defaults such as release tag, repo URL, and banner
  prefix separate from `/api/health`.

## Behavior

- Shows Agentspine branding and Omni-NexusAI links where the overlay owns the UI.
- Uses `v0.9.9-standard-pre` as the default standard-pre release tag.
- Does not falsify upstream commit, tag, branch, or health version metadata.

## Compatibility Notes

- Target runtime: Agent Zero `M v1.20` with Agentspine
  `v0.9.9-standard-pre`.
- Pre-release standard builds should identify as Agentspine standard-pre in UI
  surfaces without rewriting Agent Zero health responses.

## Test Checklist

- Compile plugin Python files.
- Confirm `/api/health` still reports actual Agent Zero `M v1.20`.
- Confirm visible Agentspine branding and links appear in the shell/header.
- Confirm no console errors from identity page-head hooks.
