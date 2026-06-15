from __future__ import annotations

import filecmp
import os
import shutil
from pathlib import Path


def get_a0_root(plugin_root: Path) -> Path:
    configured = os.getenv("A0_ROOT", "").strip()
    if configured:
        return Path(configured)
    for candidate in plugin_root.parents:
        if candidate.name == "a0":
            return candidate
        if (candidate / "helpers").is_dir() and (candidate / "webui").is_dir():
            return candidate
    return plugin_root.parents[1]


def apply_overrides(plugin_root: Path | None = None) -> list[str]:
    plugin_root = plugin_root or Path(__file__).resolve().parents[1]
    source_root = plugin_root / "overrides" / "a0"
    if not source_root.exists():
        return []

    target_root = get_a0_root(plugin_root)
    changed: list[str] = []
    for source in sorted(source_root.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(source_root)
        target = target_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and filecmp.cmp(source, target, shallow=False):
            continue
        shutil.copy2(source, target)
        changed.append(str(relative).replace("\\", "/"))
    return changed
