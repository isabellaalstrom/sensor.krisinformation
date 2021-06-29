# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Status: Tested and working on multiple installs.
Missing brands repos otherwise ready for HACS inclusion

### Added
- Added binary sensors for news and alerts
- Added a device for future enhancements
- Integration configuration using GUI (config_flow)
- System status information (system_health)
- info.md and hacs.json to prepare to add to HACS
- Dependency on httpx for better control of http operations
- Communication library (kriscom) to follow design guidance
- English translation for GUI

### Changed
- Changed default sensor property to number of messages
- Sensor icon changes due to severity and status of the sensor
- Version set to 2.0.0-beta.0 as it is breaking changes
- Updated package.yaml legacy package information file

### Removed
- configuration.yaml configuration interface

## [1.0.0] - 2019-04-04
### Changed
- Fix for migration of components in 0.91 of Home Assistant.
