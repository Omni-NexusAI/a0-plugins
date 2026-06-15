# Enhanced MCP Config DOX

## Purpose

`_enhanced_mcp_config` is the built-in Agentspine MCP configuration enhancement plugin synced from the GPU-pre container. In this container state it is primarily a manifest/documentation package with an agent-init extension stub.

## Ownership

- `plugin.yaml` owns plugin identity, version `0.9.9`, always-enabled behavior, and `mcp` settings-section placement.
- `README.md` owns the intended MCP configuration behavior: per-server enable/disable controls, refined status handling, and safer apply/toggle flow.
- `extensions/python/agent_init/_10_enhanced_mcp_config.py` owns the current runtime hook; it intentionally returns without patching in this snapshot.
- `webui/thumbnail.svg` owns the plugin thumbnail asset.

## Local Contracts

- Treat the current no-op runtime hook as the container-synced behavior until implementing a deliberate upgrade.
- Keep the manifest name `_enhanced_mcp_config` aligned with the installed directory name.
- Any future implementation must preserve unknown MCP server fields and existing server definitions.
- Do not claim active UI behavior in docs until the behavior exists in source.

## Work Guidance

- Future MCP settings code should prefer guarded config transforms over direct destructive rewrites.
- Toggle/apply flows should preserve disabled state and unsupported server fields.
- If WebUI controls are added, document selectors, store assumptions, and degradation behavior here.

## Verification

- Parse touched Python files.
- For future behavior changes, test missing/empty MCP config, enabled and disabled servers, unknown keys, and unsupported host pages.

## Child DOX Index

This plugin has no child DOX files.
