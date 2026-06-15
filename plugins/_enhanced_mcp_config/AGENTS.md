# Enhanced MCP Config DOX

## Purpose

`_enhanced_mcp_config` is the built-in Agentspine MCP configuration enhancement plugin synced from the GPU-pre container. The container behavior lives in core API/helper/WebUI files, so this plugin vendors those files under `overrides/a0` and applies them at startup.

## Ownership

- `plugin.yaml` owns plugin identity, version `0.9.9`, always-enabled behavior, and `mcp` settings-section placement.
- `README.md` owns the intended MCP configuration behavior: per-server enable/disable controls, refined status handling, and safer apply/toggle flow.
- `extensions/python/agent_init/_10_enhanced_mcp_config.py` owns startup application of the override payload.
- `helpers/overlay.py` owns copying changed override files into the runtime root.
- `overrides/a0/api/` owns MCP status/apply/toggle/log/detail API handlers copied from the container.
- `overrides/a0/helpers/` owns container MCP handler and settings helper copies required by the behavior.
- `overrides/a0/webui/components/settings/mcp/` owns the enhanced MCP settings UI copied from the container.
- `webui/thumbnail.svg` owns the plugin thumbnail asset.

## Local Contracts

- Treat `overrides/a0` as the container-synced behavior payload.
- Keep the manifest name `_enhanced_mcp_config` aligned with the installed directory name.
- Any future implementation must preserve unknown MCP server fields and existing server definitions.
- Do not edit copied override files without checking the matching container/source behavior or intentionally upgrading the plugin.

## Work Guidance

- Future MCP settings code should prefer guarded config transforms over direct destructive rewrites.
- Toggle/apply flows should preserve disabled state and unsupported server fields.
- If WebUI controls are added, document selectors, store assumptions, and degradation behavior here.

## Verification

- Parse touched Python files, including override API/helper files.
- For future behavior changes, test missing/empty MCP config, enabled and disabled servers, unknown keys, and unsupported host pages.

## Child DOX Index

This plugin has no child DOX files.
