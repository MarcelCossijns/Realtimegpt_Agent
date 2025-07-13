DOMAIN = "realtimegpt_agent"

async def async_setup(hass, config):
    """Set up the Voice LLM Agent integration (config.yaml-basiert)."""
    return True

async def async_setup_entry(hass, entry):
    """Set up via UI (Config Flow)."""
    return True

async def async_unload_entry(hass, entry):
    """Clean up when integration is removed."""
    return True