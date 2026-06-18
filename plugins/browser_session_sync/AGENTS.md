# Browser Session Sync DOX

## Purpose

This plugin persists native Agent Zero Browser tabs, cookies, and localStorage across runtime restarts.

## Contracts

- Keep all behavior plugin-owned; do not require patches to updater-managed `_browser` files.
- Automatic restore is boot-gated and one-shot. Save events must never reopen tabs.
- The current-state manifest is authoritative, including snapshots containing zero tabs.
- Preserve legacy storage-only snapshots and timestamped snapshots for manual recovery.
- Keep save listeners idempotent and saves debounced to avoid duplicate input bindings or browser slowdown.
- `enabled`, `auto_restore`, and `auto_save` remain independently configurable.

## Verification

- Run `python -m pytest tests` in an Agent Zero-compatible Python environment.
- Verify a hard restart restores tabs when the Browser panel subscribes.
- Close a restored tab, restart again, and confirm it stays closed.
- Confirm typing emits one character per keypress and routine browsing produces sparse saves.
