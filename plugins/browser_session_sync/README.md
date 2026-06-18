# Browser Session Sync

Work-in-progress Agent Zero plugin that preserves native Browser tabs, cookies,
and localStorage across hard container restarts.

## Behavior

- Restores the latest current-state snapshot once per runtime boot.
- Tracks tab loads and closes with debounced, atomic snapshots.
- Treats an empty tab set as authoritative, so closed tabs stay closed.
- Keeps timestamped snapshots for explicit manual recovery.
- Provides manual `browser_session_save` and `browser_session_restore` tools.
- Stays plugin-owned and does not patch updater-managed Agent Zero files.

## Configuration

The plugin is enabled by default and can be toggled from its plugin settings.

```yaml
enabled: true
auto_restore: true
auto_save: true
```

## Install

Install this repository as the `browser_session_sync` Agent Zero plugin, or copy
its contents to `/a0/usr/plugins/browser_session_sync`. Restart Agent Zero after
installation so lifecycle extensions are loaded.

Saved browser state is written under `/a0/usr/browser_sessions` and is not part
of the plugin repository.

## Status

This is a WIP release. Keep production snapshots backed up while testing browser
runtime and WebUI compatibility across Agent Zero updates.

## Tests

Run from an Agent Zero environment where the `helpers` and `usr` packages are
available:

```bash
python -m pytest tests
```
