from homeassistant.components.stt import Provider
from homeassistant.core import HomeAssistant
from .llm_interface import process_audio

async def async_get_provider(hass: HomeAssistant, config, discovery_info=None):
    """Home Assistant hook: liefert Deine KI-basierte STT-Klasse aus."""
    return RealtimeGptSttProvider(hass)

class RealtimeGptSttProvider(Provider):
    def __init__(self, hass: HomeAssistant):
        super().__init__(
            name="RealtimeGPT Multimodal STT",
            supported_languages=["de", "en"],
            recording_ext="wav",
        )
        _LOGGER.info("RealtimeGPTAgent initialisiert.")
        self.api_key = hass.data["realtimegpt_agent"]["api_key"]
        _LOGGER.info("RealtimeGPTAgent initialisiert.")

    async def async_process_audio(self, audio_bytes: bytes, language: str) -> str:
        """
        Hier greifst Du das rohe Audio ab und kannst direkt
        dein LLM aufrufen, z.B. Whisper oder GPT4o-Streaming.
        Rückgabe ist der erkannte Text.
        """
        _LOGGER.info("async_process_audio")
        llm_resp = await process_audio(audio_bytes, self.api_key)
        return llm_resp["text"]