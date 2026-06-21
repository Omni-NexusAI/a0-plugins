from __future__ import annotations

from helpers.api import ApiHandler, Request, Response


VOICE_OPTIONS = [
    *({"value": name, "label": f"US | Female | American | {name}"} for name in (
        "af_alloy", "af_aoede", "af_bella", "af_heart", "af_jessica", "af_kore",
        "af_nicole", "af_nova", "af_river", "af_sarah", "af_sky",
    )),
    *({"value": name, "label": f"US | Male | American | {name}"} for name in (
        "am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael",
        "am_onyx", "am_puck", "am_santa",
    )),
    *({"value": name, "label": f"UK | Female | British | {name}"} for name in (
        "bf_alice", "bf_emma", "bf_isabella", "bf_lily",
    )),
    *({"value": name, "label": f"UK | Male | British | {name}"} for name in (
        "bm_daniel", "bm_fable", "bm_george", "bm_lewis",
    )),
]


def _cuda_available() -> bool:
    try:
        import torch

        return bool(torch.cuda.is_available())
    except Exception:
        return False


class Voices(ApiHandler):
    @classmethod
    def get_methods(cls) -> list[str]:
        return ["GET", "POST"]

    async def process(self, input: dict, request: Request) -> dict | Response:
        current_values = []
        for key in ("voice", "primary_voice", "secondary_voice"):
            value = str(input.get(key, "") or "").strip()
            if value:
                current_values.append(value)

        seen = {item["value"] for item in VOICE_OPTIONS}
        options = list(VOICE_OPTIONS)
        for value in current_values:
            if value not in seen:
                seen.add(value)
                options.append({"value": value, "label": value})

        return {"success": True, "voices": options, "cuda_available": _cuda_available()}
