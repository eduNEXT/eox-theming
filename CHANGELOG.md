# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2021-11-09

### Added

- **BREAKING CHANGE**: Default backends for storage and mako are not compatible with Juniper or older versions anymore.
- Tests for python 3.8.
- Update readme with new information and formats.

### Removed

- Backends support to Ironwood.

## [1.1.0] - 2020-12-17

### Added

- A new feature to add extra scripts in templates.

## [1.0.1] - 2020-11-24

### Changed

- Fix typo.

## [1.0.0] - 2020-11-05

### Added

- Support for the juniper release.
- A new backend for the storages.

### Changed

- Middleware is now installed introspecting settings.MIDDLEWARE

### Removed

- Settings module aws.py. It was used only for compatibility with hawthorn releases.
