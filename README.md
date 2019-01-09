[![Version](https://img.shields.io/badge/version-0.1.0-green.svg?style=for-the-badge)](#) [![maintained](https://img.shields.io/maintenance/yes/2019.svg?style=for-the-badge)](#)

[![maintainer](https://img.shields.io/badge/maintainer-ISabella%20Alström%20%40isabellaalstrom-blue.svg?style=for-the-badge)](#)

# sensor.krisinformation
Component to get Krisinformation for [Home Assistant](https://www.home-assistant.io/)

## Installation:

1. Install this component by copying to your `/custom_components/sensor/` folder.
2. Add the code to your `configuration.yaml` using the config options below.
3. **You will need to restart after installation for the component to start working.**

* If you're having issues, post an issue or ask for help on the forums.

**Example configuration.yaml:**

```yaml
sensor:
  - platform: krisinformation
    latitude: !secret lat_coord
    longitude: !secret long_coord
    radius: 100
```

**Configuration variables:**

key | type | description
:--- | :--- | :---
**platform (Required)** | string | `krisinformation`
**latitude (Required)** | sring | The latitude of the position from which the sensor should look for messages.
**longitude (Required)** | string | The longitude of the position from which the sensor should look for messages.
**radius (Optional)** | number | The redius from your position that the sensor should look for messages. Default `50`

***
