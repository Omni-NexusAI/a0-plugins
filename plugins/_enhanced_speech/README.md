# _enhanced_speech

Agentspine built-in speech compatibility overlay for Agent Zero v1.20.

## Purpose

This plugin keeps Agentspine speech behavior compatible with the split v1.20
Voice UI. Kokoro TTS and Whisper STT remain separate frontend providers, while
this overlay supplies the backend compatibility layer for enhanced TTS and STT
settings.

## Built-In Source And Config

- Built-in source: `/a0/plugins/_enhanced_speech`
- User config/state: `/a0/usr/plugins/_enhanced_speech/config.json`
- Kokoro sync target: `/a0/usr/plugins/_kokoro_tts/config.json`
- Whisper sync target: `/a0/usr/plugins/_whisper_stt/config.json`

The plugin should be baked as an underscore built-in overlay. Do not enable a
duplicate non-underscore `enhanced_speech` custom plugin beside it.

## Runtime Hooks

- `agent_init` patches `_kokoro_tts.helpers.runtime` for enhanced synthesis.
- API handlers expose voice discovery, worker status, config sync, and speech
  adapter behavior.
- Page-head UI patch extends Kokoro and Whisper provider-specific settings
  surfaces without creating a combined speech panel.
- The page-head adapter also patches the v1.20 speech stream after store
  registration so completed sentence tails are released before response end.
  Cold-start registration is retried for up to two minutes and does not depend
  on opening Voice settings; later chat DOM insertion also triggers an
  idempotent patch attempt.

## Behavior

- Kokoro settings include styled primary and secondary voice dropdowns, blend
  ratio, speed, compute mode, remote URL/token/timeout, and worker test.
- Compute mode is authoritative. `Remote GPU worker` enables delegation; there
  is no second remote-enable checkbox. The in-container `GPU` choice appears
  only when `torch.cuda.is_available()` is true.
- The Kokoro card keeps one `Voice` row. It displays the primary voice normally
  or `primary + secondary` for a synthesized voice, followed by a separate mode
  row.
- Worker URL normalization supports `kokoro-gpu-worker:8891`,
  `agentspine-kokoro-gpu:8891`, and `host.docker.internal:51101`.
- Known sidecar aliases prefer `agentspine-kokoro-gpu:8891` and cache the last
  successful endpoint so a stale alias does not delay every synthesis request.
- Whisper settings remain separate and sync model size, language, message mode,
  silence threshold, silence duration, and waiting timeout.
- Stable sentence tails are synthesized immediately while unfinished text is
  retained. A private held sentinel is never sent to Kokoro, preventing
  duplicated or truncated speech as streamed text grows.
- The v1.20 `ttsService` provider path prefetches the next sentence while the
  current sentence plays and removes artificial inter-part sleeps. CPU and
  remote modes therefore share the same gapless playback queue.
- Backend notifications report local model loading/success/failure and remote
  worker state transitions. Successful settings saves report voice, blend, and
  speed changes.
- Kokoro and Whisper settings use single-flight open/save guards so rapid clicks
  cannot create duplicate plugin-settings modals or submit the same config twice.

## Compatibility Notes

- Target runtime: Agent Zero `M v1.20` with Agentspine
  `v0.9.9-standard-pre`.
- Health metadata must remain truthful to upstream Agent Zero.
- Frontend observers must be scoped and debounced so opening Settings does not
  recursively refresh the modal.

## Test Checklist

- Compile plugin Python files.
- Open Settings and Voice repeatedly without UI freeze or console errors.
- Confirm Kokoro and Whisper remain separate cards.
- Confirm Kokoro dropdowns/settings save and reload.
- On standard-pre, confirm Auto, CPU, and Remote GPU worker are present and the
  local GPU option is absent. On GPU-pre, confirm GPU is present.
- Confirm Whisper settings save and reload.
- Verify primary-only, blended, and remote-worker Kokoro synthesis.
- Verify the first complete streamed sentence reaches synthesis before the
  response finishes, with no duplicate speech after later chunks arrive.
- Confirm model, worker, voice, blend, and speed notifications appear once per
  relevant state transition.
