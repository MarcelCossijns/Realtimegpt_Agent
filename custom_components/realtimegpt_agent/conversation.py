from homeassistant.components.conversation import Agent, ConversationInput

from .audio_response import synthesize_speech
from .llm_interface import process_audio
from .tool_executor import execute_tool


class VoiceLLMAgent(Agent):
    def __init__(self, hass):
        self.hass = hass

    @property
    def supported_languages(self):
        return ["de", "en"]

    @property
    def attribution(self):
        return "Powered by GPT-4o"


    async def async_process(self, input: ConversationInput):
        if not input.audio:
            return {"response": {"text": "Audio erforderlich."}}

        api_key = self.hass.data["realtimegpt_agent"].get("api_key")
        llm_response = await process_audio(input.audio, api_key)

        if llm_response.get("tool_call"):
            await execute_tool(self.hass, llm_response["tool_call"])

        return {
            "response": {
                "text": llm_response["text"],
                "audio": llm_response.get("audio")
            }
        }


async def async_get_agent(hass):
    return VoiceLLMAgent(hass)
