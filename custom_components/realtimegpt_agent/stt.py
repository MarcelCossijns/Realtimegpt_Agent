from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.stt import Provider, AudioStream
from homeassistant.config_entries import ConfigEntry
from .llm_interface import process_audio
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities  # wird übergeben, aber hier nicht genutzt
) -> bool:
    """Damit HA diese Plattform lädt."""
    _LOGGER.debug("stt.async_setup_entry called")

    async_add_entities(
        [RealtimeGptSttProvider(hass)]
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
    @property
    def supported_audio_formats(self) -> list[str]:
        return ["wav", "mp3"]

    @property
    def supported_codecs(self) -> list[str]:
        return ["pcm"]

    @property
    def supported_sample_rates(self) -> list[int]:
        return [16000, 32000]

    @property
    def supported_bit_rates(self) -> list[int]:
        return [16, 24]

    @property
    def supported_channels(self) -> list[int]:
        return [1]

    async def async_process_audio(self, audio_bytes: bytes, language: str) -> str:
        _LOGGER.debug("RealtimeGptSttProvider.async_process_audio")
        llm_resp = await process_audio(audio_bytes, self.api_key)
        return llm_resp["text"]
    async def async_process_audio_stream(
                self, stream: AudioStream, language: str
        ) -> str:
        # Beispiel: lese den ganzen Stream und processe ihn
        data = bytearray()
        async for chunk in stream:
            data.extend(chunk)
        return await self.async_process_audio(bytes(data), language)