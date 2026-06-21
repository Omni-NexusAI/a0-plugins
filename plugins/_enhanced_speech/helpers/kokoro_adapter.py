from __future__ import annotations

import base64
import io
from typing import Any

import soundfile as sf

from . import config as speech_config
from . import remote_worker


def _notify(kind: str, message: str, *, group: str, detail: str = "") -> None:
    try:
        from helpers.notification import NotificationManager, NotificationPriority, NotificationType

        notification_type = {
            "info": NotificationType.INFO,
            "success": NotificationType.SUCCESS,
            "error": NotificationType.ERROR,
        }[kind]
        NotificationManager.send_notification(
            type=notification_type,
            priority=NotificationPriority.HIGH if kind == "error" else NotificationPriority.NORMAL,
            message=message,
            detail=detail,
            title="Kokoro TTS",
            display_time=5 if kind == "error" else 3,
            group=group,
        )
    except Exception:
        pass


def _notify_remote_state(runtime: Any, success: bool, remote_url: str, error: str = "") -> None:
    state = (success, remote_url, error if not success else "")
    if getattr(runtime, "_agentspine_remote_notification_state", None) == state:
        return
    runtime._agentspine_remote_notification_state = state
    if success:
        _notify("success", f"Remote Kokoro worker ready at {remote_url}", group="kokoro-remote")
    else:
        _notify("error", "Remote Kokoro worker is unavailable.", group="kokoro-remote", detail=error)


def _resolve_local_device(policy: str) -> tuple[str, str]:
    requested = (policy or "auto").strip().lower()
    if requested == "remote":
        return "remote", "Remote worker"
    if requested == "cpu":
        return "cpu", "CPU"
    try:
        import torch

        if requested in {"cuda", "gpu"}:
            return ("cuda", "GPU") if torch.cuda.is_available() else ("cpu", "CPU")
        if torch.cuda.is_available():
            return "cuda", "GPU"
    except Exception:
        pass
    return "cpu", "CPU"


def patch_runtime() -> None:
    from plugins._kokoro_tts.helpers import runtime

    if getattr(runtime, "_agentspine_enhanced_speech_patched", False):
        return

    runtime._agentspine_original_normalize_config = getattr(runtime, "normalize_config", None)
    runtime._agentspine_original_get_config = getattr(runtime, "get_config", None)
    runtime._agentspine_original_synthesize_sentences = getattr(runtime, "synthesize_sentences", None)
    runtime._agentspine_original_is_downloaded = getattr(runtime, "is_downloaded", None)

    def normalize_config(config: dict[str, Any] | None = None) -> dict[str, Any]:
        cfg = speech_config.kokoro_runtime_config(config)
        effective_device, effective_label = _resolve_local_device(str(cfg.get("device") or "auto"))
        cfg["effective_device"] = effective_device
        cfg["effective_device_label"] = "Remote worker" if cfg.get("remote_enabled") else effective_label
        return cfg

    def get_config() -> dict[str, Any]:
        return normalize_config()

    async def synthesize_sentences(sentences: list[str], config: dict[str, Any] | None = None) -> str:
        cfg = normalize_config(config)
        if cfg.get("remote_enabled"):
            remote_url = str(cfg.get("remote_url") or "")
            try:
                result = await remote_worker.synthesize(
                    sentences=sentences,
                    voice=str(cfg["voice"]),
                    secondary_voice=str(cfg.get("secondary_voice") or ""),
                    voice_blend=int(cfg.get("voice_blend") or 50),
                    speed=float(cfg.get("speed") or 1.1),
                    remote_url=remote_url,
                    remote_token=str(cfg.get("remote_token") or ""),
                    remote_timeout=float(cfg.get("remote_timeout") or 20),
                )
                _notify_remote_state(runtime, True, remote_url)
                return result
            except Exception as exc:
                _notify_remote_state(runtime, False, remote_url, str(exc))
                raise
        return await _synthesize_local(runtime, sentences, cfg)

    async def is_downloaded() -> bool:
        cfg = normalize_config()
        if cfg.get("remote_enabled"):
            status = await _worker_status_async(cfg)
            return bool(status.get("success"))
        original = getattr(runtime, "_agentspine_original_is_downloaded", None)
        if callable(original):
            return bool(await original())
        return getattr(runtime, "_pipeline", None) is not None

    runtime.normalize_config = normalize_config
    runtime.get_config = get_config
    runtime.synthesize_sentences = synthesize_sentences
    runtime.is_downloaded = is_downloaded
    runtime._agentspine_enhanced_speech_patched = True


async def _worker_status_async(cfg: dict[str, Any]) -> dict[str, Any]:
    import asyncio

    return await asyncio.to_thread(
        remote_worker.check_worker,
        str(cfg.get("remote_url") or ""),
        str(cfg.get("remote_token") or ""),
        float(cfg.get("remote_timeout") or 3),
    )


async def _ensure_pipeline_for_device(runtime: Any, cfg: dict[str, Any]) -> None:
    if getattr(runtime, "is_updating_model", False):
        import asyncio

        while getattr(runtime, "is_updating_model", False):
            await asyncio.sleep(0.1)

    device, _label = _resolve_local_device(str(cfg.get("device") or "auto"))
    current_device = getattr(runtime, "_agentspine_current_device", None)
    if getattr(runtime, "_pipeline", None) is not None and current_device == device:
        return

    runtime.is_updating_model = True
    _notify("info", f"Loading Kokoro TTS model on {device}...", group="kokoro-preload")
    try:
        from kokoro import KPipeline

        runtime._pipeline = KPipeline(
            lang_code="a",
            repo_id="hexgrad/Kokoro-82M",
            device=device,
        )
        runtime._agentspine_current_device = device
        _notify("success", f"Kokoro TTS model loaded on {device}.", group="kokoro-preload")
    except Exception as exc:
        _notify("error", "Failed to load the Kokoro TTS model.", group="kokoro-preload", detail=str(exc))
        raise
    finally:
        runtime.is_updating_model = False


async def _synthesize_local(runtime: Any, sentences: list[str], cfg: dict[str, Any]) -> str:
    await _ensure_pipeline_for_device(runtime, cfg)
    combined_audio: list[float] = []
    voice = str(cfg.get("voice") or "am_michael")
    secondary = str(cfg.get("secondary_voice") or "").strip()
    speed = float(cfg.get("speed") or 1.1)
    voice_value: Any = voice

    if secondary:
        v1 = runtime._pipeline.load_single_voice(voice)
        v2 = runtime._pipeline.load_single_voice(secondary)
        ratio = max(1, min(99, int(cfg.get("voice_blend") or 50))) / 100.0
        voice_value = v1 * ratio + v2 * (1.0 - ratio)

    for sentence in sentences:
        if not sentence.strip():
            continue
        segments = runtime._pipeline(sentence.strip(), voice=voice_value, speed=speed)
        for segment in list(segments):
            audio_tensor = segment.audio
            audio_numpy = audio_tensor.detach().cpu().numpy()
            combined_audio.extend(audio_numpy.tolist())

    if not combined_audio:
        return ""

    buffer = io.BytesIO()
    sf.write(buffer, combined_audio, 24000, format="WAV")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
