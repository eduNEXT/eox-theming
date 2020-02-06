""" Backend abstraction of configuration helpers used in the tests. """
from eox_theming.test_utils import TestConfigurationHelpers


def get_configuration_helper():
    """ Backend to get the configuration helper. """
    return TestConfigurationHelpers
