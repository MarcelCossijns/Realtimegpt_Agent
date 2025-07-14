from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.tts import Provider
from .llm_interface import process_audio

async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities  # wird von HA übergeben, aber nicht gebraucht
) -> bool:
    """Wird von HA aufgerufen, wenn der ConfigEntry für TTS weitergeleitet wird."""
    return True

async def async_get_engine(
        hass: HomeAssistant,
        config,            # Config aus integrations UI (wird nicht genutzt)
        discovery_info=None
) -> Provider:
    """HA hook: liefert Deine TTS-Instanz aus."""
    return RealtimeGptTtsProvider(hass)

class RealtimeGptTtsProvider(Provider):
    def __init__(self, hass: HomeAssistant):
        # Kein super().__init__(), da Provider erbt von object ohne eigenes __init__
        self.hass = hass
        self.name = "RealtimeGPT TTS"

    async def async_get_tts_audio(self, message: str, language: str):
        llm_resp = await process_audio(
            message, self.hass.data["realtimegpt_agent"]["api_key"]
        )
        # llm_resp["audio"] enthält deine Audio-Bytes (z.B. WAV/MP3)
        return llm_resp["audio"], "wav"
