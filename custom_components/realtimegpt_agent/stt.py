from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.stt import Provider
from .llm_interface import process_audio
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities  # wird übergeben, aber hier nicht genutzt
) -> bool:
    """Damit HA diese Plattform lädt."""
    _LOGGER.debug("stt.async_setup_entry called")
    for subentry in config_entry.subentries.values():
        if subentry.subentry_type != "sst":
            continue

            async_add_entities(
                [RealtimeGptSttProvider(hass)],
                config_subentry_id=subentry.subentry_id,
            )

    return True

async def async_get_provider(
        hass: HomeAssistant,
        config,
        discovery_info=None
) -> Provider:
    _LOGGER.debug("stt.async_get_provider called")
    return RealtimeGptSttProvider(hass)

class RealtimeGptSttProvider(Provider):
    def __init__(self, hass: HomeAssistant):
        super().__init__(
            name="RealtimeGPT Multimodal STT",
            supported_languages=["de","en"],
            recording_ext="wav",
        )
        _LOGGER.debug("RealtimeGptSttProvider initialized")
        self.api_key = hass.data["realtimegpt_agent"]["api_key"]

    async def async_process_audio(self, audio_bytes: bytes, language: str) -> str:
        _LOGGER.debug("RealtimeGptSttProvider.async_process_audio")
        llm_resp = await process_audio(audio_bytes, self.api_key)
        return llm_resp["text"]