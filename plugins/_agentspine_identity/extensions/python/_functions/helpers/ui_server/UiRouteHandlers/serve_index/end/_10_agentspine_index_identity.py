from helpers.extension import Extension
from usr.plugins._agentspine_identity.helpers.identity import apply_identity_text


class AgentspineIndexIdentity(Extension):
    def execute(self, data=None, **kwargs):
        if not isinstance(data, dict):
            return
        result = data.get("result")
        if isinstance(result, str):
            data["result"] = apply_identity_text(result)
