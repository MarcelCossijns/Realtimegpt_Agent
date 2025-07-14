from homeassistant.core import HomeAssistant
from homeassistant.components.tts import Provider
from .llm_interface import process_audio

async def async_get_engine(hass: HomeAssistant, config, discovery_info=None):
    """HA hook: liefert deine TTS-Instanz aus."""
    return RealtimeGptTtsProvider(hass)

class RealtimeGptTtsProvider(Provider):
    def __init__(self, hass: HomeAssistant):
        # Kein super().__init__()!
        self.hass = hass
        # Name, unter dem HA das Modul in der UI anzeigt
        self.name = "RealtimeGPT TTS"

    async def async_get_tts_audio(self, message: str, language: str):
        """
        Hier erzeugst du deine Sprach-Antwort.
        Z.B. rufst du process_audio nochmal auf, wenn
        dein LLM direkt Audio (bytes) zurückgibt.
        """
        llm_resp = await process_audio(message, self.hass.data["realtimegpt_agent"]["api_key"])
        # llm_resp["audio"] enthält die Audio-Bytes, z.B. WAV/MP3
        return llm_resp["audio"], "wav"
