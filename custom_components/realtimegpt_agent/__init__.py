import logging
from homeassistant.components import conversation as ha_conversation
from .conversation import RealtimeGPTAgent
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, Platform

DOMAIN = "realtimegpt_agent"
_LOGGER = logging.getLogger(__name__)

PLATFORMS = (
    Platform.CONVERSATION,
)


async def async_setup(hass, config):
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.info("%s: async_setup ausgeführt (YAML)", DOMAIN)
    return True

async def async_setup_entry(hass, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["api_key"] = entry.data.get("api_key")
    _LOGGER.info("%s: async_setup_entry ausgeführt. API-Key gespeichert.", DOMAIN)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass, entry):
    hass.data[DOMAIN].pop("api_key", None)
    _LOGGER.info("%s: async_unload_entry ausgeführt. API-Key entfernt.", DOMAIN)
    return True
