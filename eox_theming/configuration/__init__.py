"""
Manages the diferent access, storage locations and methods used to read the configuration of a theme
"""
import logging

from django.conf import settings
from eox_theming.edxapp_wrapper import config_sources
from eox_theming.edxapp_wrapper.theming_helpers import get_theming_helpers

LOG = logging.getLogger(__name__)


class ThemingConfiguration(object):
    """
    This class must handle all the calls to the diferential settings a theme will be allowed to use
    """
    source_functions = [getattr(config_sources, name) for name in settings.EOX_THEMING_CONFIG_SOURCES]
    theming_helpers = get_theming_helpers()

    @classmethod
    def options(cls, *args, **kwargs):
        """Main method for accessing the current configuration for the theme"""
        value = None

        for source in cls.source_functions:
            try:
                value = source(*args)
                if value:
                    break
            except Exception as exc:  # pylint: disable=broad-except
                LOG.warning('Found an error reading %s from source %s. Trace: %s',
                            '.'.join(args), source.__name__, exc)
                continue

        if not value:
            value = kwargs.pop('default', None)

        return value

    @classmethod
    def get_theme_name(cls):
        """
        Get the current theme name

        Returns:
            (str): Theme name associated to the request.
        """
        theme_name = cls.options('theme', 'name', default=None)

        if not theme_name:
            theme_name = cls.options('template_dir', default=settings.EOX_THEMING_DEFAULT_THEME_NAME)

        if theme_name:
            theme_name = theme_name.split('/')[-1]

        return theme_name

    @classmethod
    def get_default_theme(cls):
        """ Get parent theme of the current request. """
        parent_theme_name = cls.options('theme', 'parent', default=None)
        if not parent_theme_name:
            parent_theme_name = settings.EOX_THEMING_DEFAULT_THEME_NAME

        themes = cls.theming_helpers.get_themes()

        for theme in themes:
            if theme.name == parent_theme_name:
                return theme
        return None
