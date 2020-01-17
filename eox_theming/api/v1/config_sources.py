""" Config sources definition """
import os

from importlib import import_module

from eox_theming.edxapp_wrapper.configuration_helpers import get_configuration_helper
from eox_theming.utils import load_json_from_file

configuration_helpers = get_configuration_helper()
LOCAL_JSON_OBJECT_FILENAME = 'object_exploded.json'
LOCAL_JSON_MODULE_LOCATION = 'eox_theming.api'


def from_local_file():
    """
    Load the theming configurations from a local file
    """
    location = configuration_helpers.get_value('EOX_THEMING_JSON_THEME_CONFIG_PATH', None)

    if not location:
        # the current local object lives under eox_theming.api module
        local_json_module_location = import_module(LOCAL_JSON_MODULE_LOCATION)
        base_dir = os.path.dirname(local_json_module_location.__file__)
        location = os.path.join(base_dir, LOCAL_JSON_OBJECT_FILENAME)

    configuration = load_json_from_file(location)

    # TODO: is the object going to live under THEME_OPTIONS key??
    return configuration.get('THEME_OPTIONS', {})
