import logging
from homeassistant.components.conversation import ConversationEntity, ConversationInput
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .llm_interface import process_audio
from .tool_executor import execute_tool

_LOGGER = logging.getLogger(__name__)

class RealtimeGPTAgent(ConversationEntity):
    def __init__(self, hass):
        self.hass = hass
        _LOGGER.info("RealtimeGPTAgent initialisiert.")

    @property
    def supported_languages(self) -> list[str]:
        return ["de", "en"]

    @property
    def attribution(self) -> str:
        return "Powered by GPT-4o"

    async def _async_handle_message(self, input: ConversationInput, chat_log):
        _LOGGER.debug("Verarbeite Konversationseingabe über RealtimeGPTAgent.")
        if not input.audio:
            _LOGGER.warning("Eingabe ohne Audio empfangen.")
            chat_log.async_add_assistant_content_without_tools("Audio erforderlich.")
            return self._build_response("Audio erforderlich.", chat_log)

        api_key = self.hass.data["realtimegpt_agent"].get("api_key")
        llm_response = await process_audio(input.audio, api_key)

        if llm_response.get("tool_call"):
            _LOGGER.info("Tool-Call erkannt: %s", llm_response["tool_call"])
            await execute_tool(self.hass, llm_response["tool_call"])

        chat_log.async_add_assistant_content_without_tools(llm_response["text"])
        return self._build_response(llm_response["text"], chat_log, llm_response.get("audio"))

    def _build_response(self, text: str, chat_log, audio=None):
        # ChatLog already  AssistantContent
        from homeassistant.components.conversation import ConversationResult, AssistantResponse
        res = AssistantResponse(language=chat_log.user_input.language)
        if audio:
            res.async_set_speech(text)
        return ConversationResult(conversation_id=None, response=res, continue_conversation=False)

