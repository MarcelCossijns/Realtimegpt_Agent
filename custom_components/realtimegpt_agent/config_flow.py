from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
import voluptuous as vol

DOMAIN = "realtimegpt_agent"


class RealtimeGPTConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Realtime GPT Agent",
                data={CONF_API_KEY: user_input[CONF_API_KEY]}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str
            }),
            errors=errors
        )
