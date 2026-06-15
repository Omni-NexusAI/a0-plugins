# A0 Plugins DOX

This repository uses DOX: a hierarchy of `AGENTS.md` files that agents must read before editing and keep current after meaningful changes.

## Purpose

This repo is the upstream Omni-NexusAI A0 plugin monorepo for portable Agent Zero plugins and Agentspine plugin overlays. It is separate from a local runtime checkout, but some plugin folders may be copied directly from an installed container state.

## Ownership

- `plugins/` contains plugin source packages.
- `CONTAINER_SYNC.md` records the current container snapshot source and the plugin directories matched to it.
- Each plugin owns its manifest, README, extension hooks, helper code, assets, and nearest `AGENTS.md`.
- Runtime logs, installed settings, bytecode caches, and container filesystem snapshots are not source artifacts.

## Local Contracts

- Read this file first, then read every child `AGENTS.md` on the path to files you will edit.
- The closest `AGENTS.md` controls local details; parent docs still control broader workflow and safety rules.
- Keep manifests, README files, DOX files, and implementation behavior aligned.
- Preserve installed plugin directory names when they are used in manifests or Python import paths.
- When comparing to Agentspine or a baked A0 runtime, clearly state which container, image, branch, or commit is the source of truth.
- Update the nearest owning `AGENTS.md` when behavior, structure, config contracts, UI contracts, verification requirements, or sync status change.

## Work Guidance

- Prefer plugin-local code over host-runtime edits.
- Keep runtime patches idempotent and guarded.
- Preserve unknown config keys when reading or writing host/plugin settings.
- Avoid generated files such as `.pyc`, `__pycache__`, build output, logs, or local secrets.
- Keep container-synced plugins faithful to their declared snapshot unless intentionally upgrading them.

## Verification

- For Python changes, parse or compile touched Python files when practical.
- For WebUI changes, inspect the affected DOM/CSS behavior and verify safe degradation when the target store/page is absent.
- For sync work, compare plugin manifests and source files against the declared runtime snapshot.

## Child DOX Index

- `plugins/AGENTS.md`: shared plugin packaging, portability, container sync, and per-plugin guidance.
