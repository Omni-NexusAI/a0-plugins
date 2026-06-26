from __future__ import annotations

from typing import Any

from helpers.extension import Extension


class BrowserSessionRestoreOnRuntimeStart(Extension):
    """Disabled: native browser_runtime_started is updater-managed.

    Browser Session Sync must remain plugin-only, so auto-restore is bootstrapped
    from plugin-owned WebUI/WebSocket/API paths instead of relying on this
    native _browser hook.
    """

    async def execute(
        self,
        runtime: Any = None,
        context_id: str = "",
        **kwargs: Any,
    ) -> None:
        return
