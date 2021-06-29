from homeassistant.helpers.entity import Entity

from .const import (
    INTEGRATION_DOMAIN,
    DEVICE_GUID,
    DEVICE_NAME,
    DEVICE_MANUFACTURER,
    DEVICE_MODEL,
    INTEGRATION_VERSION
)

class KRISDevice(Entity):
    """HASL Device class."""
    @property
    def device_info(self):
        """Return device information about HASL Device."""
        return {
            "identifiers": {(INTEGRATION_DOMAIN, DEVICE_GUID)},
            "name": DEVICE_NAME,
            "manufacturer": DEVICE_MANUFACTURER,
            "model": DEVICE_MODEL,
            "sw_version": INTEGRATION_VERSION,
            "entry_type": "service"
        }