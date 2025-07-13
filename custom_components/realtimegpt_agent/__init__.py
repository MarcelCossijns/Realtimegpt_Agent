import logging

DOMAIN = "realtimegpt_agent"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up from configuration.yaml (optional)."""
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.info("%s: async_setup ausgeführt (YAML)", DOMAIN)
    return True

async def async_setup_entry(hass, entry):
    """Set up via UI (Config Flow)."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["api_key"] = entry.data.get("api_key")
    _LOGGER.info("%s: async_setup_entry ausgeführt. API-Key gespeichert.", DOMAIN)
    return True

async def async_unload_entry(hass, entry):
    """Clean up when integration is removed."""
    hass.data[DOMAIN].pop("api_key", None)
    _LOGGER.info("%s: async_unload_entry ausgeführt. API-Key entfernt.", DOMAIN)
    return True
async def async_get_agent(hass, agent_id: str):
    _LOGGER.warning("conversation: requested agent ID: %s", agent_id)