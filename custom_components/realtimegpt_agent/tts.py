from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.tts import Provider
from .llm_interface import process_audio

async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> bool:
    """Stellt sicher, dass HA diese Plattform lädt."""
    return True

async def async_get_engine(hass: HomeAssistant, config, discovery_info=None):
    return RealtimeGptTtsProvider(hass)

class RealtimeGptTtsProvider(Provider):
    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.name = "RealtimeGPT TTS"

    async def async_get_tts_audio(self, message: str, language: str):
        llm_resp = await process_audio(
            message, self.hass.data["realtimegpt_agent"]["api_key"]
        )
        return llm_resp["audio"], "wav"