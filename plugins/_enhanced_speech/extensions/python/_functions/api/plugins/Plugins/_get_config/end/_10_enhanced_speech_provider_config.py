from __future__ import annotations

import importlib.util
from pathlib import Path

from helpers.extension import Extension


def _load_config_helper():
    plugin_root = Path(__file__).resolve().parents[8]
    helper_path = plugin_root / "helpers" / "config.py"
    spec = importlib.util.spec_from_file_location("agentspine_enhanced_speech_config", helper_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load enhanced speech config helper from {helper_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EnhancedSpeechGetConfig(Extension):
    def execute(self, data=None, **kwargs):
        if not isinstance(data, dict):
            return
        args = data.get("args") or ()
        if len(args) < 2 or not isinstance(args[1], dict):
            return
        payload = args[1]
        plugin_name = payload.get("plugin_name", "")
        if plugin_name not in {"_enhanced_speech", "enhanced_speech", "_kokoro_tts", "_whisper_stt"}:
            return
        result = data.get("result")
        if not isinstance(result, dict) or not result.get("ok"):
            return
        settings = result.get("data") if isinstance(result.get("data"), dict) else {}
        enhanced = _load_config_helper().provider_config_for(plugin_name, settings)
        if enhanced is not None:
            result["data"] = enhanced
