from __future__ import annotations


def patch_runtime() -> None:
    from . import kokoro_adapter

    kokoro_adapter.patch_runtime()
