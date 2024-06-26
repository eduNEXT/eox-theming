#!/bin/bash

# This script installs the package in the edxapp environment, installs test requirements from Open edX and runs the tests using the Tutor settings.
echo "Install package"
pip install -e /openedx/eox-theming

echo "Install test-requirements"
make test-requirements

echo "Run tests"
pytest -s --ds=lms.envs.tutor.test /openedx/eox-theming/eox_theming/tests/tutor
