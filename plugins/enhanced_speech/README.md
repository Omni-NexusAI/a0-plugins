# Enhanced Speech

Plugin package providing Kokoro TTS enhancements for compatible Agent Zero runtimes.

## Features

- **Dual-voice blending** – primary and secondary Kokoro voice fields with adjustable blend ratio
- **Speed control** – configurable speech rate default
- **Device policy** – auto or CPU device selection for TTS inference
- **Remote worker support** – optional remote Kokoro worker URL, token, and timeout settings
- **Graceful fallback** – loads as a no-op compatibility shim when the host runtime does not expose enhanced speech settings

## Compatibility

- Agent Zero runtimes with the v1.7+ plugin loader and speech settings surface
- Safe to install on unsupported hosts – the plugin degrades silently

## Installation

Copy the `enhanced_speech` directory into your Agent Zero `plugins_custom/` folder and restart the runtime.

## Configuration

Defaults are defined in `default_config.yaml`. Override values through the Agent Zero settings UI or your runtime's configuration layer.

## License

MIT
