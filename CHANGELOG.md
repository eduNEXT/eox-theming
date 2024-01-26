# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v7.0.0 - 2024-01-26

### [7.0.0](https://github.com/eduNEXT/eox-theming/compare/v6.0.1...v7.0.0) (2024-01-26)

#### ⚠ BREAKING CHANGES

* add compatibility with quince release
  
* chore: update constraints & upgrade requirements
  
* fix: modify deprecated method
  
* fix: was mandatory to send any get_response
  
* chore: update github-actions
  
* docs: update README for showing quince support
  

#### Performance Improvements

* add compatibility with Quince release ([#52](https://github.com/eduNEXT/eox-theming/issues/52)) ([38970ba](https://github.com/eduNEXT/eox-theming/commit/38970ba14891d32527841406296e77051ca487f6))

## v6.0.1 - 2024-01-03

### [6.0.1](https://github.com/eduNEXT/eox-theming/compare/v6.0.0...v6.0.1) (2024-01-03)

### Bug Fixes

* improved handling of empty directories in get_dirs method ([#51](https://github.com/eduNEXT/eox-theming/issues/51)) ([bd10dc3](https://github.com/eduNEXT/eox-theming/commit/bd10dc34030c8d4110009037ed928c78f895154f))

## v6.0.0 - 2023-11-20

### [6.0.0](https://github.com/eduNEXT/eox-theming/compare/v5.0.0...v6.0.0) (2023-11-20)

#### ⚠ BREAKING CHANGES

- add compatibility with palm release
  
- ci: update workflow dependencies
  
- docs: update README
  
- build: update plugin requirements
  
- fix: message_control enabled weren't being used
  
- refactor: allow 120 characters per line when pylint is executed
  
- feat: override get_dirs method
  
- chore: increase eox-tenant version
  
- fix: gh-action-pypi-publish version
  

#### Performance Improvements

- add compatibility with palm release ([#50](https://github.com/eduNEXT/eox-theming/issues/50)) ([0f21bb2](https://github.com/eduNEXT/eox-theming/commit/0f21bb2eaca9118ba998990b73b014bab94251f8))

## v5.0.0 - 2023-02-10

### [5.0.0](https://github.com/eduNEXT/eox-theming/compare/v4.0.1...v5.0.0) (2023-02-10)

#### ⚠ BREAKING CHANGES

- - refactor: delete unsupported backends for older releases
  
- 

#### Features

- add compativility with olive realese ([#44](https://github.com/eduNEXT/eox-theming/issues/44)) ([4025a14](https://github.com/eduNEXT/eox-theming/commit/4025a1487264d7c085b4364112a961f0831a972b))

#### Continuous Integration

- adds mantainer group ([fe5daff](https://github.com/eduNEXT/eox-theming/commit/fe5daff24dcf3a351a553d58a34c71c8a091094c))
- update the changelog updater step in bumpversion ([#42](https://github.com/eduNEXT/eox-theming/issues/42)) ([1c7aaa9](https://github.com/eduNEXT/eox-theming/commit/1c7aaa93f15e40a21eacb0e6844c2dfd1b3898c8))

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
