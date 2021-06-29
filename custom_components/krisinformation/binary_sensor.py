from homeassistant.util import Throttle
from datetime import timedelta

from .device import KRISDevice
from .const import (
    INTEGRATION_DOMAIN,
    CONF_INTEGRATION_ID,
    CONF_NAME
)

async def async_setup_entry(hass, config, async_add_devices):

    if not INTEGRATION_DOMAIN in hass.data:
        return False

    async_add_devices([
        KrisInfoAlertSensor(hass.data[INTEGRATION_DOMAIN]['api'], config.title, config.data[CONF_INTEGRATION_ID]),
        KrisInfoNewsSensor(hass.data[INTEGRATION_DOMAIN]['api'], config.title, config.data[CONF_INTEGRATION_ID]),
    ])



class KrisInfoAlertSensor(KRISDevice):
    """Representation of a Krisinformation sensor."""

    def __init__(self, api, name, id):
        """Initialize a Krisinformation sensor."""
        self._api = api
        self._name = name
        self._id = id
        self._icon = "mdi:alert-outline"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} Alerts"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if (not self._api.available):
            return "mdi:close-circle-outline"

        if 'display_icon' in self._api.attributes:
            return self._api.attributes['display_icon'] 

        return self._icon

    @property
    def state(self):
        """Return the state of the device."""
        if (self._api.attributes["alert_count"]>0):
            return True

        return False

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._api.attributes

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._api.available

    @Throttle(timedelta(minutes=5))
    async def async_update(self):
        """Get the latest data from the Krisinformation API."""
        await self._api.update()

    @property
    def device_class(self):
        """Return the class of this device."""
        return "problem"

    @property
    def should_poll(self):
        """No polling needed."""
        return True
               
    @property
    def unique_id(self):
        return f"kris-{self._id}-alerts"

class KrisInfoNewsSensor(KRISDevice):
    """Representation of a Krisinformation sensor."""

    def __init__(self, api, name, id):
        """Initialize a Krisinformation sensor."""
        self._api = api
        self._name = name
        self._id = id
        self._icon = "mdi:alert-outline"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name} News"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        if (not self._api.available):
            return "mdi:close-circle-outline"

        if 'display_icon' in self._api.attributes:
            return self._api.attributes['display_icon'] 

        return self._icon

    @property
    def state(self):
        """Return the state of the device."""
        if (self._api.attributes["news_count"]>0):
            return True

        return False

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return self._api.attributes

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._api.available

    @Throttle(timedelta(minutes=5))
    async def async_update(self):
        """Get the latest data from the Krisinformation API."""
        await self._api.update()

    @property
    def device_class(self):
        """Return the class of this device."""
        return "problem"

    @property
    def should_poll(self):
        """No polling needed."""
        return True
               
    @property
    def unique_id(self):
        return f"kris-{self._id}-news"


