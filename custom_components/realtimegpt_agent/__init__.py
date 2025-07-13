import logging
from homeassistant.components import conversation as ha_conversation
from .conversation import RealtimeGPTAgent

DOMAIN = "realtimegpt_agent"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.info("%s: async_setup ausgeführt (YAML)", DOMAIN)
    return True

async def async_setup_entry(hass, entry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["api_key"] = entry.data.get("api_key")
    _LOGGER.info("%s: async_setup_entry ausgeführt. API-Key gespeichert.", DOMAIN)

    # Agent direkt registrieren
    agent = RealtimeGPTAgent(hass)
    ha_conversation.async_set_agent(hass, entry, agent)

    return True

async def async_unload_entry(hass, entry):
    hass.data[DOMAIN].pop("api_key", None)
    _LOGGER.info("%s: async_unload_entry ausgeführt. API-Key entfernt.", DOMAIN)
    return True
