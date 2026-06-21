from helpers.extension import Extension

try:
    from plugins._agentspine_identity.helpers.identity import get_identity_config
except Exception:
    from usr.plugins._agentspine_identity.helpers.identity import get_identity_config


class AgentspineIdentityBanners(Extension):
    async def execute(self, banners: list = [], frontend_context: dict = {}, **kwargs):
        cfg = get_identity_config()
        banners.append(
            {
                "id": "agentspine-identity",
                "type": "info",
                "priority": 1,
                "title": str(cfg.get("product_name") or "Agentspine"),
                "html": "Agentspine overlay plugins are active on this Agent Zero-compatible runtime.",
                "dismissible": True,
                "source": "backend",
            }
        )
