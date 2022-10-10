# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v4.0.1 - 2022-10-10

### [4.0.1](https://github.com/eduNEXT/eox-theming/compare/v4.0.0...v4.0.1) (2022-10-10)

### Bug Fixes

- add workflow to publish in pypi ([77b7e81](https://github.com/eduNEXT/eox-theming/commit/77b7e8192b81ba90d8810602899fb29710728325))

### Documentation

- update README file ([e6bdc9f](https://github.com/eduNEXT/eox-theming/commit/e6bdc9fa4e2ad517f82db3a27670887656c5c8a5))

## v4.0.0 - 2022-09-20

### [4.0.0](https://github.com/eduNEXT/eox-theming/compare/v3.1.0...v4.0.0) (2022-09-20)

#### ⚠ BREAKING CHANGES

- remove support version v3.1.0
- 
- perf: add compatibility with openedx nutmeg release
- 
- ci(circleci): remove ci and update github actions
- 
- build: update requirements and tox
- 
- docs: add nutmeg info to README file
- 
- build: update requirements
- 

#### Performance Improvements

- eox-theming support for Nutmeg release ([#40](https://github.com/eduNEXT/eox-theming/issues/40)) ([5e094e7](https://github.com/eduNEXT/eox-theming/commit/5e094e7871f04a575580d1be1c7ee32128d87212))

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
