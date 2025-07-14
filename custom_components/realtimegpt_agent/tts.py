from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.tts import Provider
from .llm_interface import process_audio
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities  # wird übergeben, aber hier nicht genutzt
) -> bool:
    """Damit HA diese Plattform lädt."""
    _LOGGER.debug("tts.async_setup_entry called")
    return True

async def async_get_engine(
        hass: HomeAssistant,
        config,
        discovery_info=None
) -> Provider:
    _LOGGER.debug("tts.async_get_engine called")
    return RealtimeGptTtsProvider(hass)

class RealtimeGptTtsProvider(Provider):
    def __init__(self, hass: HomeAssistant):
        self.hass = hass
        self.name = "RealtimeGPT TTS"
        _LOGGER.debug("RealtimeGptTtsProvider initialized")

    async def async_get_tts_audio(self, message: str, language: str):
        _LOGGER.debug("RealtimeGptTtsProvider.async_get_tts_audio")
        llm_resp = await process_audio(
            message, self.hass.data["realtimegpt_agent"]["api_key"]
        )
        return llm_resp["audio"], "wav"
