from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "realtimegpt_agent"
PLATFORMS = (
    Platform.CONVERSATION,
    Platform.STT,
    Platform.TTS,
)

async def async_setup(hass: HomeAssistant, config):
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})[ "api_key"] = entry.data.get(CONF_API_KEY)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN].pop("api_key", None)
    return True
