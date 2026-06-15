# A0 Plugins DOX

This repository uses DOX: a hierarchy of `AGENTS.md` files that agents must read before editing and keep current after meaningful changes.

## Purpose

This repo is the upstream A0 plugin monorepo for portable Agent Zero plugins maintained under Omni-NexusAI. It is separate from any local Agentspine runtime checkout or baked container tree.

## Ownership

- `plugins/` contains portable plugin source packages.
- Each plugin is designed to be copied into an Agent Zero `plugins_custom/` or compatible plugin directory.
- This monorepo can sync individual plugin folders into per-plugin repositories.
- Runtime state, installed plugin config, logs, bytecode caches, and container snapshots are not source contracts.

## Local Contracts

- Read this file first, then read every child `AGENTS.md` on the path to files you will edit.
- The closest `AGENTS.md` controls local details; parent docs still control broader workflow and safety rules.
- Keep plugins portable across compatible Agent Zero runtimes unless a plugin doc explicitly scopes support narrower.
- Preserve graceful degradation: unsupported hosts should fail quietly or report a clear compatibility issue, not break the runtime.
- Keep manifests, README files, DOX files, and implementation behavior aligned.
- Update the nearest owning `AGENTS.md` when behavior, structure, config contracts, UI contracts, or verification requirements change.

## Work Guidance

- Prefer plugin-local code over host-runtime edits.
- Keep runtime patches idempotent and guarded.
- Preserve unknown config keys when reading/writing host or plugin settings.
- Avoid committing generated files such as `.pyc`, `__pycache__`, build output, logs, or local secrets.
- When comparing to Agentspine or a baked A0 runtime, clearly state which tree is the source of truth.

## Verification

- For Python changes, parse or compile touched Python files when practical.
- For WebUI changes, inspect the affected DOM/CSS behavior and verify the plugin degrades safely when the target store/page is absent.
- For config migrations, test missing keys, existing keys, and unknown keys.

## Child DOX Index

- `plugins/AGENTS.md`: shared plugin packaging, portability, and per-plugin guidance.
