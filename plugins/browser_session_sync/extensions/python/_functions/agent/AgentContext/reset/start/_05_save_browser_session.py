from __future__ import annotations

from helpers.extension import Extension
from usr.plugins.browser_session_sync.helpers.session_sync import (
    context_id_from_extension_data,
    save_runtime_snapshot_for_context,
)


class SaveBrowserSession(Extension):
    async def execute(self, data: dict = {}, **kwargs):
        context_id = context_id_from_extension_data(data)
        if not context_id:
            return
        try:
            await save_runtime_snapshot_for_context(context_id)
        except Exception:
            pass
