from helpers.api import ApiHandler, Request, Response

try:
    from plugins._multi_source_updater.helpers import source
except Exception:
    from usr.plugins._multi_source_updater.helpers import source


class Source(ApiHandler):
    @classmethod
    def get_methods(cls) -> list[str]:
        return ["GET", "POST"]

    async def process(self, input: dict, request: Request) -> dict | Response:
        if "update_source" in input:
            selected = source.set_active_source_key(str(input.get("update_source") or ""))
        else:
            selected = source.get_active_source_key()
        return {
            "success": True,
            "active_update_source": selected,
            "update_sources": source.source_options(),
        }
