from __future__ import annotations
from typing import Any
from helpers.extension import Extension


class BrowserSessionSyncPrompt(Extension):
    """Adds system prompt section explaining browser session persistence is GLOBAL:
    - ALL tabs (user-opened or agent-opened) are automatically saved on every navigation
    - Auto-restore on fresh contexts
    - No init script pollution (fixed bug where all tabs were tagged)
    """
    async def execute(
        self,
        system_prompt: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        if system_prompt is None:
            return
        section = (
            "## Browser Session Persistence (GLOBAL)\n\n"
            "Browser sessions (cookies + localStorage) are persisted GLOBALLY across the entire browser context.\n\n"
            "**Key behaviors:**\n"
            "- ALL tabs — whether opened by you or by the user — are auto-saved on every page load/close\n"
            "- The current browser context's tabs are visible via the `browser` tool and the WebUI browser viewer\n"
            "- When a new conversation starts (fresh context), the most recent saved session is auto-restored into the new context\n"
            "- No init scripts are injected (this was a previous bug that polluted all tabs)\n\n"
            "**To save explicitly:** Use tool `browser_session_sync.save` to snapshot the current context's state immediately.\n\n"
            "**To restore explicitly:** Use tool `browser_session_sync.restore` with `--list` to see available sessions, or `--filename` to load a specific one.\n\n"
            "**To use the user's pre-existing tabs:** Just use the `browser` tool with their tab's context_id. Do NOT open new tabs if the user already has them open — you can navigate to their tabs directly.\n"
        )
        system_prompt.append(section)
