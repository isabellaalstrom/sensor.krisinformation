import asyncio
import logging
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr

from .api import KrisinformationAPI

from .const import (
    INTEGRATION_DOMAIN,
    INTEGRATION_VERSION,
    INTEGRATION_EVENTS,
    DEVICE_GUID,
    DEVICE_NAME,
    DEVICE_MODEL,
    DEVICE_MANUFACTURER,
    DEVICE_TYPE,
    CONF_COUNTRY,
    CONF_COUNTY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_RADIUS,
)

logger = logging.getLogger(INTEGRATION_DOMAIN)

@asyncio.coroutine
async def async_setup(hass, config):

    @callback
    async def refresh_data(service):
        hass.bus.fire(INTEGRATION_EVENTS, {"event_type": "manual_refresh_triggered"})
        await hass.data[INTEGRATION_DOMAIN]['api'].update()

    if not INTEGRATION_DOMAIN in hass.data:
        hass.data.setdefault(INTEGRATION_DOMAIN,{}) 

    hass.services.async_register(INTEGRATION_DOMAIN, 'refresh_data', refresh_data)

    return True


async def async_migrate_entry(hass, config_entry: ConfigEntry):
    logger.debug("[migrate_entry] Nothing to do from version %s to version %s", config_entry.version, INTEGRATION_VERSION)

    return True  

async def reload_entry(hass, entry):
    try:
        await async_unload_entry(hass, entry)
        logger.debug("Unload succeeded")
    except Exception as e:
        logger.error("Unload failed")

    try:
        await async_setup_entry(hass, entry)
        logger.debug("Setup succeeded")
    except Exception as e:
        logger.error("Setup failed")

    return True

async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry):

    latitude = config.data.get(CONF_LATITUDE) if config.data.get(CONF_LATITUDE) is not None else hass.config.latitude
    longitude = config.data.get(CONF_LONGITUDE) if config.data.get(CONF_LONGITUDE) is not None else hass.config.longitude
    radius = config.data.get(CONF_RADIUS) if config.data.get(CONF_RADIUS) is not None else 50
    county = config.data.get(CONF_COUNTY) if config.data.get(CONF_COUNTY) is not None else None
    country = config.data.get(CONF_COUNTRY) if config.data.get(CONF_COUNTRY) is not None else None

    if not "api" in hass.data[INTEGRATION_DOMAIN]:
        hass.data[INTEGRATION_DOMAIN]['api'] = KrisinformationAPI(hass, longitude, latitude, county, radius, country)

    try:
        device_registry = await dr.async_get_registry(hass)
        device_registry.async_get_or_create(
            config_entry_id=config.entry_id,
            identifiers={(INTEGRATION_DOMAIN, DEVICE_GUID)},
            name=DEVICE_NAME,
            model=DEVICE_MODEL,
            sw_version=INTEGRATION_VERSION,
            manufacturer=DEVICE_MANUFACTURER,
            entry_type=DEVICE_TYPE
        )    
    except Exception as e:
        logger.error("Failed to create device")
        return False

    try:
        hass.async_add_job(hass.config_entries.async_forward_entry_setup(config, "sensor"))
        hass.async_add_job(hass.config_entries.async_forward_entry_setup(config, "binary_sensor"))
        logger.debug("Forward entry setup succeeded")
    except Exception as e:
        logger.error("Forward entry setup failed")
        return False

    try:
        hass.data[INTEGRATION_DOMAIN]['updater'] = config.add_update_listener(reload_entry)
    except Exception as e:
        logger.error("Update listener setup failed")
        return False

    return True


async def async_unload_entry(hass, entry):
    try:
        del hass.data[INTEGRATION_DOMAIN]['updater']

        hass.async_add_job(hass.config_entries.async_forward_entry_unload(entry, "sensor"))
        hass.async_add_job(hass.config_entries.async_forward_entry_unload(entry, "binary_sensor"))
    except Exception as e:
        logger.error("Forward entry unload failed")
        return False

    return True    