from helpers.extension import Extension


class EnhancedSpeechInit(Extension):
    def execute(self, **kwargs):
        if self.agent:
            self.agent.set_data("enhanced_speech_plugin", {"loaded": True})