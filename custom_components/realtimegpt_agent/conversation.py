import logging
from homeassistant.components.conversation.agent import Agent, ConversationInput
from .llm_interface import process_audio
from .tool_executor import execute_tool

_LOGGER = logging.getLogger(__name__)

class RealtimeGPTAgent(Agent):
    def __init__(self, hass):
        self.hass = hass
        _LOGGER.info("RealtimeGPTAgent initialisiert.")

    @property
    def supported_languages(self):
        return ["de", "en"]

    @property
    def attribution(self):
        return "Powered by GPT-4o"

    async def async_process(self, input: ConversationInput):
        _LOGGER.debug("Verarbeite Konversationseingabe über RealtimeGPTAgent.")

        if not input.audio:
            _LOGGER.warning("Eingabe ohne Audio empfangen.")
            return {"response": {"text": "Audio erforderlich."}}

        api_key = self.hass.data["realtimegpt_agent"].get("api_key")
        llm_response = await process_audio(input.audio, api_key)

        if llm_response.get("tool_call"):
            _LOGGER.info("Tool-Call erkannt: %s", llm_response["tool_call"])
            await execute_tool(self.hass, llm_response["tool_call"])

        return {
            "response": {
                "text": llm_response["text"],
                "audio": llm_response.get("audio")
            }
        }
