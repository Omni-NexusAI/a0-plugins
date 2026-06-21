# Enhanced Speech DOX

## Purpose

`_enhanced_speech` is the backend compatibility layer for split Kokoro TTS and Whisper STT on A0 v1.20.

## Contracts

- Built-in source is `/a0/plugins/_enhanced_speech`; provider config remains in `_kokoro_tts` and `_whisper_stt`.
- Keep Kokoro and Whisper as separate cards and settings flows.
- The stream adapter may release only stable sentence tails; its held sentinel must never reach synthesis.
- v1.20 `ttsService` must synthesize one sentence ahead while current audio plays; do not await playback before starting the next synthesis or add artificial inter-sentence sleeps.
- Runtime patching and store patching must be idempotent and tolerate cold-start store registration for up to two minutes.
- Notifications are state-transition based to avoid one toast per utterance.
- Kokoro and Whisper config opening and Save submission are single-flight; plugin patches must never create or reveal duplicate settings modals.

## Compatibility And Verification

- Target A0 `M v1.20`, Agentspine `v0.9.9-standard-pre` with CPU and remote-worker modes; local GPU remains build-dependent.
- Compile Python, syntax-check page-head JavaScript, verify split UI controls, and test primary, blended, CPU, and remote synthesis.
- Verify early streamed speech has no duplicate, truncated, markdown, abbreviation, or sentinel output and that model/voice notifications appear.
