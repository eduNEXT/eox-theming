""" Config sources definition """
import os

from importlib import import_module

from django.conf import settings

from eox_theming.edxapp_wrapper.configuration_helpers import get_configuration_helper
from eox_theming.utils import load_json_from_file

configuration_helpers = get_configuration_helper()
LOCAL_JSON_OBJECT_FILENAME = 'object_exploded.json'
LOCAL_JSON_MODULE_LOCATION = 'eox_theming.api'


def from_local_file():
    """
    Load the theming configurations from a local file
    """
    location = configuration_helpers.get_value('EOX_THEMING_API_JSON_CONFIG_PATH', None)

    if not location:
        # the current local object lives under eox_theming.api module
        local_json_module_location = import_module(LOCAL_JSON_MODULE_LOCATION)
        base_dir = os.path.dirname(local_json_module_location.__file__)
        location = os.path.join(base_dir, LOCAL_JSON_OBJECT_FILENAME)

    configuration = load_json_from_file(location)

    # TODO: is the object going to live under THEME_OPTIONS key??
    return configuration.get('THEME_OPTIONS', {})


def from_site_config():
    """
    This source is compatible with the site_configurations from Open edX platform.
    It will fallback to global platform settings if the theme object is not found in
    the site configuration
    """
    options_dict = configuration_helpers.get_value(
        'THEME_OPTIONS',
        getattr(settings, 'THEME_OPTIONS', {})
    )
    return options_dict
