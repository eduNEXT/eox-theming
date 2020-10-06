"""
Manages the diferent access, storage locations and methods used to read the configuration of a theme
"""
import logging

from django.conf import settings

from eox_theming.edxapp_wrapper import config_sources
from eox_theming.edxapp_wrapper.theming_helpers import get_theme_class, get_theming_helpers

LOG = logging.getLogger(__name__)
Theme = get_theme_class()


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
                if value is not None:
                    break
            except Exception as exc:  # pylint: disable=broad-except
                LOG.warning('Found an error reading %s from source %s. Trace: %s',
                            '.'.join(args), source.__name__, exc)
                continue

        if value is None:
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

        return theme_name.lower()

    @classmethod
    def get_parent_or_default_theme(cls):
        """ Get parent theme of the current request. """
        parent_theme_name = cls.options('theme', 'parent', default=None)
        if not parent_theme_name:
            parent_theme_name = settings.EOX_THEMING_DEFAULT_THEME_NAME
        return cls.get_wrapped_theme(parent_theme_name)

    @classmethod
    def get_wrapped_theme(cls, theme_name):
        """ Get theme based on the input name. """
        theme_name = theme_name.lower()
        try:
            return Theme(
                name=theme_name,
                theme_dir_name=theme_name,
                themes_base_dir=cls.theming_helpers.get_theme_base_dir(theme_name),
                project_root=cls.theming_helpers.get_project_root_name()
            )
        except ValueError as error:
            # Log exception message and return None, so that open source theme is used instead
            LOG.exception('Theme not found in any of the themes dirs. [%s]', error)
        return None
