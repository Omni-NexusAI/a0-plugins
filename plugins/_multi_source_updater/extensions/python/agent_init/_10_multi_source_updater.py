from helpers.extension import Extension


class MultiSourceUpdaterInit(Extension):
    def execute(self, **kwargs):
        try:
            from plugins._multi_source_updater.helpers import source
        except Exception:
            from usr.plugins._multi_source_updater.helpers import source

        source.patch_self_update()
        if getattr(self, "agent", None):
            self.agent.set_data("agentspine_update_source", source.get_active_source_key())
