![stability-wip](https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg?style=for-the-badge)


[![Version](https://img.shields.io/badge/version-2.0.0_beta.0-green.svg?style=for-the-badge)](#) [![maintained](https://img.shields.io/maintenance/yes/2021.svg?style=for-the-badge)](#)

[![maintainer](https://img.shields.io/badge/maintainer-Isabella%20Alström%20%40isabellaalstrom-blue.svg?style=for-the-badge)](#)


# sensor.krisinformation
Component to get Krisinformation for [Home Assistant](https://www.home-assistant.io/).

Will get all messages from [Krisinformations api](http://api.krisinformation.se/v2/feed?format=json) in a set radius from your coordinates.
If one of the fetched messages is an alert as opposed to news, the state of the sensor will be "Alert". The sensor contains all fetched messages as objects.

Use together with [custom card for Lovelace](https://github.com/isabellaalstrom/krisinfo-card).

<img src="https://github.com/isabellaalstrom/krisinfo-card/blob/master/krisinfo.png" alt="Krisinformation Lovelace Card" />

This component is supported by [Custom updater and Tracker card](https://github.com/custom-components/custom_updater).

## Installation:

1. Install this component by creating a `custom_components` folder in the same folder as your configuration.yaml is, if you don't already have one.
2. Inside that folder, create another folder named `krisinformation`. Put the contents of the custom_components folder in there.
2. **You will need to restart after installation for the component to start working.**
3. Add the integration in the Configuration GUI under integrations

* If you're having issues, [ask for help on the forums](https://community.home-assistant.io/t/custom-component-krisinformation-sweden/90340) or post an issue.

## Usage

**Example automation for getting a notification when the sensor has an alert:**
Make sure you change the sensor name if you didn't use the default name.

```yaml
automation:
  - alias: 'Krisinformation Alert'
    initial_state: 'on'
    trigger:
      platform: state
      entity_id: sensor.krisinformation
      to: "Alert"
    action:
      - service: notify.my_phone
        data_template:
          message: >
            {{states.sensor.krisinformation.attributes.messages[0].Headline}} - {{states.sensor.krisinformation.attributes.messages[0].Message}} {{states.sensor.krisinformation.attributes.messages[0].Web}}
```

Like my work and want to say thanks? Do it here:

<a href="https://www.buymeacoffee.com/iq1f96D" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>


## Changelog
[Changes](https://github.com/isabellaalstrom/sensor.krisinformation/blob/master/CHANGELOG.md)
