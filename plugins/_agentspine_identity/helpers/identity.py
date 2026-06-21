from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from helpers import plugins


PLUGIN_NAME = "_agentspine_identity"

DEFAULTS = {
    "product_name": "Agentspine",
    "short_name": "AS",
    "banner_prefix_main": "M",
    "banner_prefix_dev": "D",
    "compatibility_label": "A0-compatible",
    "default_release_tag": "v0.9.9-standard-pre",
}

PROTECTED_PHRASES = (
    "Agent Zero",
    "agent-zero",
    "Agent 0",
)


def get_identity_config() -> dict[str, Any]:
    try:
        loaded = plugins.get_plugin_config(PLUGIN_NAME) or {}
    except Exception:
        loaded = {}
    result = dict(DEFAULTS)
    if isinstance(loaded, dict):
        result.update({key: value for key, value in loaded.items() if value is not None})
    return result


def default_release_tag() -> str:
    return str(get_identity_config().get("default_release_tag") or DEFAULTS["default_release_tag"])


def normalize_release_tag(tag: str | None) -> str:
    value = (tag or "").strip()
    return value or default_release_tag()


def format_timestamp(value: datetime | None = None) -> str:
    when = value or datetime.now(timezone.utc)
    return when.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def friendly_version_label(version: str | None = None) -> str:
    cfg = get_identity_config()
    value = normalize_release_tag(version)
    return f"{cfg['product_name']} {value}"


def format_display_version(version: str | None = None) -> str:
    cfg = get_identity_config()
    return f"{cfg['banner_prefix_main']} {normalize_release_tag(version)}"


def apply_identity_text(text: str | None) -> str:
    if not text:
        return ""
    cfg = get_identity_config()
    result = str(text)
    result = result.replace("Agent Zero is running.", f"{cfg['product_name']} is running.")
    result = result.replace("Agent Zero", str(cfg["product_name"]))
    result = result.replace("agent-zero", "agentspine")
    return result
