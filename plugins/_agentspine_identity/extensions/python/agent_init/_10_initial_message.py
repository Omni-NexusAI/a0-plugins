from helpers.extension import Extension

try:
    from plugins._agentspine_identity.helpers.identity import get_identity_config
except Exception:
    from usr.plugins._agentspine_identity.helpers.identity import get_identity_config


class InitialMessage(Extension):
    def execute(self, **kwargs):
        if getattr(self, "agent", None):
            self.agent.set_data("agentspine_identity", get_identity_config())
