from __future__ import annotations

import importlib.util
import importlib
from pathlib import Path

from helpers.extension import Extension


def _load_remote_tts_helper():
    for module_name in (
        "usr.plugins._enhanced_speech.helpers.remote_tts",
        "plugins._enhanced_speech.helpers.remote_tts",
    ):
        try:
            return importlib.import_module(module_name)
        except Exception:
            pass
    try:
        return importlib.import_module("usr.plugins._enhanced_speech.helpers.remote_tts")
    except Exception:
        pass
    plugin_root = Path(__file__).resolve().parents[3]
    helper_path = plugin_root / "helpers" / "remote_tts.py"
    spec = importlib.util.spec_from_file_location("usr.plugins._enhanced_speech.helpers.remote_tts", helper_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load enhanced speech helper from {helper_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EnhancedSpeechInit(Extension):
    def execute(self, **kwargs):
        _load_remote_tts_helper().patch_runtime()
        if getattr(self, "agent", None):
            self.agent.set_data("enhanced_speech_loaded", True)
            self.agent.set_data("enhanced_speech_backends", ["kokoro_tts", "whisper_stt"])
