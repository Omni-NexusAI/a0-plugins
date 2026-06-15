# Enhanced Speech DOX

## Purpose

`_enhanced_speech` is the built-in Agentspine speech enhancement plugin synced from the GPU-pre container. In this state it adds remote Kokoro worker detection/defaults and replaces the WebUI microphone recorder with an enhanced silence-aware STT recorder.

## Ownership

- `plugin.yaml` owns plugin identity, version `0.9.9`, always-enabled behavior, and `agent` settings-section placement.
- `README.md` owns user-facing summary and compatibility notes.
- `helpers/remote_tts.py` owns remote Kokoro URL detection, device option injection, TTS defaults, runtime settings mutation, and host patching.
- `helpers/overlay.py` owns copying changed container override files into the runtime root.
- `overrides/a0/helpers/` owns container helper/settings files required for full remote Kokoro behavior.
- `overrides/a0/webui/components/settings/agent/speech.html` owns the container speech settings UI.
- `extensions/python/agent_init/_10_enhanced_speech.py` and `extensions/python/startup_migration/_05_enhanced_speech_remote_tts.py` own loading and applying the remote TTS runtime patch.
- `extensions/webui/initFw_end/enhanced-stt-recorder.js` owns the enhanced microphone recorder patch.
- `webui/thumbnail.svg` owns the plugin thumbnail asset.

## Local Contracts

- Preserve the `remote` TTS device value and configured URL precedence.
- Remote URL detection must accept plugin/settings keys before environment variables and only probe the default worker when the build/env says remote TTS is expected.
- Runtime patching must be idempotent through `_agentspine_enhanced_speech_patched`.
- The STT recorder must avoid sending tiny/empty recordings and must return to listening after processing.
- This container-synced version does not contain the older rich voice dropdown HTML; do not document that UI as present unless it is reimplemented.
- Treat `overrides/a0` as part of the plugin's functional payload, not optional documentation.

## Work Guidance

- Keep recorder state transitions explicit: inactive, activating, listening, recording, waiting, processing.
- Keep browser APIs guarded enough to fail gracefully when microphone permissions, `MediaRecorder`, or target stores are unavailable.
- Preserve MIME type fallback order unless a target browser issue requires a deliberate change.
- Keep remote TTS patching in `helpers/remote_tts.py` so both startup hooks share the same behavior.

## Verification

- Parse touched Python files, including override helper files.
- In a compatible runtime, verify remote Kokoro URL detection/defaults and that the `remote` device option appears only when appropriate.
- In the WebUI, verify microphone permission failure, silence detection, tiny-recording filtering, transcription API submission, and return-to-listening behavior.

## Child DOX Index

This plugin has no child DOX files.
