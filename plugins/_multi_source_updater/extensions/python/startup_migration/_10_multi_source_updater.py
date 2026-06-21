from helpers.extension import Extension


class MultiSourceUpdaterStartup(Extension):
    def execute(self, **kwargs):
        try:
            from plugins._multi_source_updater.helpers import source
        except Exception:
            from usr.plugins._multi_source_updater.helpers import source

        source.patch_self_update()
