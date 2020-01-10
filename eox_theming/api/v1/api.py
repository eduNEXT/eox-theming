"""
Theming API exposing methods required on frontend
"""
from importlib import import_module
import commentjson
import os
import logging
import operator
from copy import deepcopy

# forward compatibility for Python 3
from functools import reduce  # pylint: disable=redefined-builtin

from django.conf import settings

from eox_theming.utils import dict_merge

LOG = logging.getLogger(__name__)

LOCAL_JSON_OBJECT_FILENAME = 'object_exploded.json'
LOCAL_JSON_MODULE_LOCATION = 'eox_theming.api'


def from_local_file():
    """
    Load the theming configurations from a local file
    """
    location = getattr(settings, 'EOX_THEMING_JSON_THEME_CONFIG_PATH', None)

    if not location:
        # the current local object lives under eox_theming.api module
        local_json_module_location = import_module(LOCAL_JSON_MODULE_LOCATION)
        base_dir = os.path.dirname(local_json_module_location.__file__)
        location = os.path.join(base_dir, LOCAL_JSON_OBJECT_FILENAME)

    configuration = {}

    if not os.path.exists(location):
        return configuration

    with open(location, 'r') as f:
        try:
            configuration = commentjson.load(f)
        except Exception as exc:  # pylint: disable=broad-except
            LOG.warning('Found an error reading json theme object from location %s. Trace: %s',
                        location, exc)

    options_dict = configuration.get('THEME_OPTIONS', {})
    return options_dict


class ThemingOptions(object):
    """
    This class must handle all the calls to the diferential settings a theme will be allowed to use
    """
    # TODO: This value source_functions must come from a django setting
    source_functions = [from_local_file]
    _config = None

    def __init__(self):
        """
        Initialize the ThemingOptions object by loading the theme configuration
        """
        self._load_configuration()

    def options(self, *args, **kwargs):
        """Main method for accessing the current configuration for the theme"""
        value = None

        try:
            value = reduce(operator.getitem, args, self._config)
        except (AttributeError, KeyError):
            LOG.debug("Found nothing when reading the theme options for %s", ".".join(args))
            value = None

        if value is None:
            value = kwargs.pop('default', None)

        return value

    def _load_configuration(self):
        """
        Load the configuration theme values on the instance
        """
        for source in self.source_functions:
            try:
                config = source()
                if config:
                    break
            except Exception as exc:  # pylint: disable=broad-except
                LOG.warning('Unable to read Theme Options from source %s. Trace: %s',
                            source.__name__, exc)
                continue

        if not config:
            config = {}

        # Getting theme defaults
        default_config = self._get_default_configuration()
        # Updating default configs with current config
        config = dict_merge(deepcopy(default_config), config)
        self._config = config

    def _get_default_configuration(self):
        """
        obtain a set of configurations defined in the current theme
        """
        # TODO: define the logic to get the defaults from the right location
        return {}
