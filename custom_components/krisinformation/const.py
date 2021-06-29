from homeassistant.const import (
    CONF_NAME,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_RADIUS
)

INTEGRATION_NAME = 'Krisinformation'
INTEGRATION_VERSION = '2.0.0-beta.0'
INTEGRATION_DOMAIN = 'krisinfo'
INTEGRATION_ATTRIBUTION = 'Krisinformation.se'
INTEGRATION_EVENTS = "krisinformation"

DEVICE_NAME = "Krisinformation API"
DEVICE_MANUFACTURER = "isabellaalstrom"
DEVICE_MODEL = f"api-v{INTEGRATION_VERSION}"
DEVICE_GUID = "1235386-5fad-49c6-8f03-c7a047cd5aa5-6a618956-520c-41d2-9a10-6d7e7353c7f5"
DEVICE_TYPE = "service"

CONF_COUNTY = 'county'
CONF_COUNTRY = 'country'
CONF_INTEGRATION_ID = "id"