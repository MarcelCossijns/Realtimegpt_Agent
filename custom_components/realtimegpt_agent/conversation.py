import logging
from homeassistant.components.conversation import ConversationEntity, ConversationInput
from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .llm_interface import process_audio
from .tool_executor import execute_tool
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

_LOGGER = logging.getLogger(__name__)

class RealtimeGPTAgent(ConversationEntity):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        super().__init__()
        # … dann eigene Felder setzen
        self.hass = hass
        self.entry = entry
        _LOGGER.info("RealtimeGPTAgent initialisiert.")

    @property
    def supported_languages(self) -> list[str]:
        return ["de", "en"]

    @property
    def attribution(self) -> str:
        return "Powered by GPT-4o"

    async def async_added_to_hass(self) -> None:
        """When entity is added to Home Assistant."""
        _LOGGER.warning("async_added_to_hass (conversation.py")
        await super().async_added_to_hass()
        conversation.async_set_agent(self.hass, self.entry, self)

    async def async_will_remove_from_hass(self) -> None:
        """When entity will be removed from Home Assistant."""
        _LOGGER.warning("async_will_remove_from_hass (conversation.py")
        conversation.async_unset_agent(self.hass, self.entry)
        await super().async_will_remove_from_hass()

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

async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    _LOGGER.warning("async_setup_entry (conversation.py)")
    # Einfach genau einen Agent anlegen:
    async_add_entities([RealtimeGPTAgent(hass, entry)], True)