import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from .const import (
    CONF_NAME,
    CONF_RADIUS,
    CONF_COUNTY,
    CONF_COUNTRY,
    CONF_LATITUDE,
    CONF_LONGITUDE
)

def base_config_schema(config: dict = {}, config_flow: bool = False) -> dict:
    if not config:
        config = {
            CONF_NAME: ""
        }
    if config_flow:
        return {
            vol.Required(CONF_NAME, default=config.get(CONF_NAME)): str
        }
    return {
        vol.Optional(CONF_NAME, default=config.get(CONF_NAME)): str
    }


def standard_config_option_schema(options: dict = {}) -> dict:
    if not options:
        options = {CONF_RADIUS: 50, CONF_COUNTY: "", CONF_COUNTRY: "", CONF_LATITUDE: "", CONF_LONGITUDE: ""}
    return {
        vol.Optional(CONF_RADIUS, default=50) : cv.positive_int,
        vol.Optional(CONF_COUNTY) : cv.string,
        vol.Optional(CONF_COUNTRY) : cv.string,
        vol.Optional(CONF_LATITUDE): cv.latitude,
        vol.Optional(CONF_LONGITUDE): cv.longitude
    }
