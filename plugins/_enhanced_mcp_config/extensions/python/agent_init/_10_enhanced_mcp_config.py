from helpers.extension import Extension


class EnhancedMcpConfigInit(Extension):
    def execute(self, **kwargs):
        if self.agent:
            self.agent.set_data("_enhanced_mcp_config_plugin", {"loaded": True})
