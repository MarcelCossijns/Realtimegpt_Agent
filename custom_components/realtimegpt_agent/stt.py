from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.stt import Provider
from .llm_interface import process_audio

async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> bool:
    """Wird von HA aufgerufen, wenn der ConfigEntry für STT weitergeleitet wird."""
    # Hier musst Du nichts weiter tun,
    # der eigentliche Provider kommt über async_get_provider.
    return True

async def async_get_provider(
        hass: HomeAssistant, config, discovery_info=None
) -> Provider:
    """HA hook: liefert Deine KI-basierte STT-Klasse aus."""
    return RealtimeGptSttProvider(hass)

class RealtimeGptSttProvider(Provider):
    def __init__(self, hass: HomeAssistant):
        super().__init__(
            name="RealtimeGPT Multimodal STT",
            supported_languages=["de", "en"],
            recording_ext="wav",
        )
        self.api_key = hass.data["realtimegpt_agent"]["api_key"]

    async def async_process_audio(self, audio_bytes: bytes, language: str) -> str:
        llm_resp = await process_audio(audio_bytes, self.api_key)
        return llm_resp["text"]