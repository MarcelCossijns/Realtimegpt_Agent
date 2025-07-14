from homeassistant.components.tts import Provider
from homeassistant.core import HomeAssistant
from .llm_interface import process_audio

async def async_get_engine(hass: HomeAssistant, config, discovery_info=None):
    return RealtimeGptTtsProvider(hass)

class RealtimeGptTtsProvider(Provider):
    def __init__(self, hass: HomeAssistant):
        super().__init__(name="RealtimeGPT TTS")
        self.api_key = hass.data["realtimegpt_agent"]["api_key"]

    async def async_get_tts_audio(self, message: str, language: str):
        # Hier könntest du ein erneutes LLM-Call vermeiden,
        # wenn 'audio' bereits in der STT-Antwort drinsteckt.
        # Sonst: prompte nochmal dein LLM oder OpenAI-TTS.
        return audio_bytes, "wav"