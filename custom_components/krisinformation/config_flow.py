import voluptuous
import logging
import uuid

from homeassistant import config_entries
from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import callback

from .const import (
    CONF_NAME,
    INTEGRATION_DOMAIN,
    INTEGRATION_VERSION,
    CONF_INTEGRATION_ID
)

from .config_schema import (
    base_config_schema,
    standard_config_option_schema,
)

logger = logging.getLogger(INTEGRATION_DOMAIN)


class ConfigFlow(config_entries.ConfigFlow, domain=INTEGRATION_DOMAIN):
    """Config flow for Krisinformation."""

    VERSION = INTEGRATION_VERSION
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    #FIXME: DOES NOT ACTUALLY VALIDATE ANYTHING! WE NEED THIS! =)
    async def validate_input(self, data):
        """Validate input in step user"""

        if not data[CONF_NAME]:
            raise InvalidNameError

        return data


    async def async_step_user(self, user_input):
            """Handle the initial step."""
            errors = {}

            if user_input is None:
                return self.async_show_form(step_id="user",data_schema=voluptuous.Schema(base_config_schema(user_input, True)))

            try:
                user_input = await self.validate_input(user_input)
            except InvalidNameError:
                errors["base"] = "invalid_integration_name"
                logger.debug("Invalid name specified")
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown_exception"
                logger.debug("Unknown excpetion occured")
            else:

                id = str(uuid.uuid4())
                await self.async_set_unique_id(id)
                user_input[CONF_INTEGRATION_ID] = id
            
                name = user_input[CONF_NAME]
                del user_input[CONF_NAME]

                try:
                    tempResult = self.async_create_entry(title=name, data=user_input)
                    logger.debug("Integration created successfully")
                    return tempResult
                except Exception as e:
                    logger.error("Failed to create integration")
                    return self.async_abort(reason="not_supported")

            return self.async_show_form(step_id="user",data_schema=voluptuous.Schema(base_config_schema(user_input, True)),errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlow(config_entry)


class OptionsFlow(config_entries.OptionsFlow):
    """Krisinformation config flow options handler."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user(user_input)

    async def validate_input(self, data):
        """Validate input in step user"""
        #FIXME: DOES NOT ACTUALLY VALIDATE ANYTHING! WE NEED THIS! =)

        return data        

    async def async_step_user(self, user_input):
        """Handle a flow initialized by the user."""
        errors = {}

        schema = standard_config_option_schema(self.config_entry.options)

        #FIXME: DOES NOT ACTUALLY VALIDATE ANYTHING! WE NEED THIS! =)
        if user_input is not None:
            try:
                user_input = await self.validate_input(user_input)
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown_exception"
                logger.debug("Unknown exception occured")
            else:
                try:
                    tempresult = self.async_create_entry(title=self.config_entry.title, data=user_input)
                    logger.debug("Entry update succeeded")
                    return tempresult
                except Exception as e:
                    logger.error("Unknown exception occured")


            return self.async_show_form(step_id="user", data_schema=voluptuous.Schema(schema),errors=errors)    
            

        return self.async_show_form(step_id="user", data_schema=voluptuous.Schema(schema))


class InvalidNameError(HomeAssistantError):
    """Error to indicate the integration is not of a valid type."""
