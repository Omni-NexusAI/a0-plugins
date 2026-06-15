# Enhanced Speech DOX

## Purpose

`enhanced_speech` owns portable Kokoro TTS enhancements for compatible Agent Zero runtimes: primary/secondary voice settings, blend ratio, speed, device policy, and remote worker configuration.

## Ownership

- `README.md` owns user-facing purpose, installation, compatibility, and high-level feature description.
- `default_config.yaml` owns default voice, blend, speed, device, and remote worker values.
- `extensions/webui/page-head/_10_enhanced_speech.html` owns runtime WebUI patching of the Agent Zero settings store.
- Any future CSS or custom dropdown markup for voice labels belongs inside this plugin and must be documented here.

## Current Upstream State

The current upstream WebUI hook injects enhanced speech defaults into `Alpine.store("settings")` and ensures basic `tts_device_options` exist. It does not yet implement the richer styled voice-selector dropdown from the Agentspine target tree.

## Required Voice Selector Design Contract

When the richer voice dropdown is added or restored, every voice label should be split into these parts:

`REGION • GENDER • ACCENT • voice_id`

Example:

`US • Male • American • am_michael`

The visual styling contract is:

- `voice-region`: region text such as `US` or `GB`; inherited text color; font weight `600`; inherited Rubik font.
- `voice-sep`: bullet separator; inherited text color with low emphasis, opacity around `0.35`; not selectable.
- `voice-meta`: gender and accent text; inherited text color with medium emphasis, opacity around `0.7`; inherited Rubik font.
- `voice-name`: final Kokoro voice id such as `am_michael`; inherited text color with stronger emphasis, opacity around `0.85`; `Roboto Mono`, monospace; about `0.8rem`.
- The select/button container should use the normal A0 UI text color and Rubik font, with the voice id as the only monospace segment.

The primary and secondary voice selectors should use the same label structure. The secondary selector may include a `None` option before the voice list.

## Local Contracts

- Keep defaults idempotent: only fill settings keys that are missing.
- Keep the plugin safe on unsupported hosts by checking for the target Alpine store/page before patching.
- Preserve unknown settings and host-provided `tts_device_options`.
- Keep the voice-label string format and CSS class contract stable once implemented; other agents may replicate it in plugin-specific UIs.
- Do not assume Agentspine-only file paths in this portable monorepo package.

## Work Guidance

- Add richer UI behavior as plugin-local WebUI extension code rather than host-runtime edits.
- If voice options come from an API, preserve API order and append unknown current values rather than dropping them.
- Keep primary voice, secondary voice, blend ratio, speed, device, remote URL, token, and timeout settings synchronized with defaults and README docs.

## Verification

- Load on a host with the settings store and confirm defaults are injected once.
- Load on a host without the target settings store and confirm no unhandled errors.
- For the rich voice selector, verify the visible label order and styling: region, dim bullet, dim metadata, dim bullet, dim metadata, dim bullet, monospace voice id.
- Verify secondary voice `None`, blend ratio, speed, and remote worker settings save correctly.

## Child DOX Index

This plugin has no child DOX files.
