from __future__ import annotations

from typing import Any

from helpers.extension import Extension
from usr.plugins.browser_session_sync.helpers.session_sync import (
    auto_restore_runtime_session_for_context,
)


class BrowserSessionViewerFallback(Extension):
    """Plugin-owned, boot-gated restore bootstrap for Browser viewer opens."""

    async def execute(
        self,
        event_type: str = "",
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        if event_type != "browser_viewer_subscribe" or not data:
            return
        context_id = str(data.get("context_id") or data.get("contextId") or "").strip()
        if not context_id:
            return
        try:
            message = await auto_restore_runtime_session_for_context(context_id)
            print(f"[browser_session_sync] viewer bootstrap: {message}")
        except Exception as exc:
            print(f"[browser_session_sync] viewer bootstrap restore failed for {context_id}: {exc}")
