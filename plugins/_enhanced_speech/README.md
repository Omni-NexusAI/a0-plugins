# Enhanced Speech

Built-in Agentspine speech enhancement plugin.

This directory is copied from the `agentspine-gpu-pre` container state synced on
2026-06-15. The manifest version is `0.9.9` and the installed plugin name is
`_enhanced_speech`.

## Purpose

`_enhanced_speech` improves speech behavior for Agentspine runtimes without
editing the host runtime directly. In this container state it focuses on:

- discovering and defaulting to a remote Kokoro worker when appropriate;
- exposing a `remote` TTS device option when a worker is reachable/configured;
- applying remote TTS defaults during startup and settings reads;
- replacing the WebUI microphone recorder with a silence-aware recorder that
  filters tiny recordings before transcription.

## Design

The plugin has one shared backend helper:

- `helpers/remote_tts.py` owns URL normalization, remote worker detection,
  runtime settings defaults, device-option injection, and idempotent host
  patching.

Two Python extension hooks load that same helper:

- `extensions/python/agent_init/_10_enhanced_speech.py`
- `extensions/python/startup_migration/_05_enhanced_speech_remote_tts.py`

The duplicate entry points make the patch available during normal agent startup
and during startup migration flows without duplicating behavior.

The WebUI hook lives in:

- `extensions/webui/initFw_end/enhanced-stt-recorder.js`

It imports the speech and microphone setting stores, replaces
`speechStore.initMicrophone`, and creates an `EnhancedMicrophoneInput` that
tracks explicit recorder states.

## Function

Remote TTS URL detection uses this precedence:

1. settings keys: `tts_kokoro_remote_url`, `kokoro_remote_url`,
   `tts_remote_url`;
2. environment keys: `A0_TTS_KOKORO_REMOTE_URL`,
   `A0_SET_TTS_KOKORO_REMOTE_URL`, `KOKORO_WORKER_URL`,
   `KOKORO_GPU_WORKER_URL`, `A0_TTS_REMOTE_URL`;
3. default worker `http://kokoro-gpu-worker:8891`, but only when remote TTS is
   enabled by environment or the build type is `HYBRID_GPU`.

When a remote worker is detected, runtime settings are defaulted to enable
Kokoro TTS and prefer the `remote` device unless the user already selected a
non-auto/non-CPU device.

The STT recorder uses `MediaRecorder`, browser audio analysis, silence
thresholds from `speechStore`, and `/transcribe` API calls. It ignores recordings
smaller than `256` bytes, filters bracket-only transcription artifacts, and
returns to listening after each processing pass.

## Current Limits

This synced container version does not include the older rich voice dropdown
HTML/CSS. If that UI needs to be restored, implement it deliberately and update
`AGENTS.md`, this README, and the WebUI verification notes together.

## Verification

- Parse the Python files after backend changes.
- In a compatible runtime, confirm the `remote` TTS device appears only when a
  configured or expected worker is available.
- In the WebUI, verify microphone permission failure, silence detection,
  transcription submission, tiny-recording filtering, and return-to-listening
  behavior.
