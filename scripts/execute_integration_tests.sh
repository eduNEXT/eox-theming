#!/bin/bash

echo "Install requirements"
make install-dev-dependencies

echo "Run tests"
# Since we don't have any integration tests at the moment,
# we allow pytest to pass without running any tests.
pytest -rPf --allow-no-tests

