"""
Theming API exposing methods required on frontend
"""
import logging
import operator

# forward compatibility for Python 3
from functools import reduce  # pylint: disable=redefined-builtin

from django.conf import settings

from eox_theming.utils import dict_merge, load_json_from_file
from eox_theming.edxapp_wrapper.theming_helpers import get_theming_helpers
from eox_theming.api.v1 import config_sources
from eox_theming.api.v1.particles import Particle

LOG = logging.getLogger(__name__)


class ThemingOptions(object):
    """
    This class must handle all the calls to the diferential settings a theme will be allowed to use
    """
    source_functions = [
        getattr(config_sources, name) for name in settings.EOX_THEMING_API_CONFIG_SOURCES
    ]
    _config = None
    theming_helpers = get_theming_helpers()

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
        config = {}
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
        config = dict_merge(default_config, config)
        self._config = config

    def _get_default_configuration(self):
        """
        obtain a set of configurations defined in the current theme
        """
        # For now the default object is taken from current theme in
        # <theme_name>/lms/default_exploded.json
        return self._defaults_from_current_theme()

    def _defaults_from_current_theme(self):
        """
        Get defaults from current theme
        """
        filename = 'default_exploded.json'
        current_theme = self.theming_helpers.get_current_theme()
        if not current_theme:
            return {}

        default_file_loc = current_theme.path / filename
        default_config = load_json_from_file(default_file_loc)
        return default_config.get('THEME_OPTIONS', {})

    def get_segment(self, segment_name):
        """
        Get a high level element (Segment) of an html page
        """
        segment_obj = self.options(segment_name)
        if not segment_obj:
            return None

        # TODO: create from Factory
        return Particle(**segment_obj)
