from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.tts import Provider
from .llm_interface import process_audio
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up TTS entities."""
    for subentry in config_entry.subentries.values():
        if subentry.subentry_type != "tts":
            continue

        async_add_entities(
            [RealtimeGptTtsProvider(config_entry, subentry)],
            config_subentry_id=subentry.subentry_id,
        )


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
