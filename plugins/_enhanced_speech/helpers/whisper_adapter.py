from __future__ import annotations

from typing import Any

from . import config as speech_config


def patch_runtime() -> None:
    from plugins._whisper_stt.helpers import runtime

    if getattr(runtime, "_agentspine_enhanced_speech_patched", False):
        return

    runtime._agentspine_original_normalize_config = getattr(runtime, "normalize_config", None)
    runtime._agentspine_original_get_config = getattr(runtime, "get_config", None)
    original_normalize_config = runtime._agentspine_original_normalize_config
    original_get_config = runtime._agentspine_original_get_config

    def normalize_config(config: dict[str, Any] | None = None) -> dict[str, Any]:
        base = original_normalize_config(config) if callable(original_normalize_config) else (config or {})
        return speech_config.normalize_whisper_config(base)

    def get_config() -> dict[str, Any]:
        base = original_get_config() if callable(original_get_config) else {}
        return speech_config.normalize_whisper_config(base)

    if hasattr(runtime, "normalize_config"):
        runtime.normalize_config = normalize_config
    runtime.get_config = get_config
    runtime._agentspine_enhanced_speech_patched = True
