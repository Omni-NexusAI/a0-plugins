# Multi Source Updater

Built-in Agentspine self-update enhancement plugin.

This directory is copied from the `agentspine-gpu-pre` container state synced on
2026-06-15. The manifest version is `0.9.9` and the installed plugin name is
`_multi_source_updater`.

## Purpose

The plugin represents the Agentspine updater enhancement boundary. The manifest
places it in the `backup` settings section and describes the intended feature
set:

- selecting update source between Omni-NexusAI and agent0ai;
- preserving the selected update source in persisted settings;
- providing Agentspine v0.9.9-pre compatibility display behavior.

## Design

In this container state, the implementation is intentionally minimal:

- `plugin.yaml` declares the always-enabled plugin and backup/settings
  placement.
- `extensions/python/agent_init/_10_multi_source_updater.py` defines the runtime
  extension class and returns without modifying the host.
- `webui/thumbnail.svg` provides the plugin asset.

This makes the plugin a durable placeholder and documentation boundary for
updater behavior that may be implemented in the runtime or added to the plugin
later.

## Function

At startup, Agent Zero's plugin framework can load `MultiSourceUpdaterInit`, but
the extension does not patch updater routes, settings, source selection, or UI
state in this snapshot.

Future implementation should keep source selection, persistence, display
labels, and update execution separate so agents can reason about each behavior
without surprise side effects.

## Current Limits

The manifest and README describe the intended updater enhancement surface, but
the current copied code is a no-op. Do not assume active source switching exists
until source code is added.

## Verification

- Parse the Python extension after edits.
- For future behavior, verify source selection persistence, display labels,
  fallback behavior, and unsupported host behavior.
