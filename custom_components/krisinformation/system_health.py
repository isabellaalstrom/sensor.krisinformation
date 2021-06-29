"""Provide info to system health."""
import sys
import logging

from homeassistant.components import system_health
from homeassistant.core import HomeAssistant, callback

from .const import (
    INTEGRATION_DOMAIN,
    INTEGRATION_VERSION
)

logger = logging.getLogger(INTEGRATION_DOMAIN)


@callback
def async_register(
    hass: HomeAssistant, register: system_health.SystemHealthRegistration
) -> None:
    """Register system health callbacks."""

    try:
        register.domain = INTEGRATION_DOMAIN
        register.async_register_info(system_health_info, "/config/integrations")
    except Exception as e:
        logger.error("System health registration failed")



async def system_health_info(hass):
    """Get info for the info page."""
    api = hass.data[INTEGRATION_DOMAIN]["api"]
    diagData = await api.getDiag()

    try:
        statusObject = {
            "Version": INTEGRATION_VERSION,
            "Available": diagData['available'],
            "Messages": f"{diagData['count']} ({diagData['filtered']} filtered)"
        }
        return statusObject
    except Exception as e:
        return {
            "Version": INTEGRATION_VERSION,
            "Available": "Unknown",
            "Messages": "Unknown"
        }


