"""
Manages the diferent access, storage locations and methods used to read the configuration of a theme
"""
from django.conf import settings
from eox_theming.edxapp_wrapper import config_sources


class ThemingConfiguration(object):
    """
    This class must handle all the calls to the diferential settings a theme will be allowed to use
    """
    source_functions = [getattr(config_sources, name) for name in settings.EOX_THEMING_CONFIG_SOURCES]

    @classmethod
    def options(cls, *args, **kwargs):  # pylint: disable=unused-argument
        """Main method for accessing the current configuration for the theme"""
        value = None

        for source in cls.source_functions:
            try:
                value = source(*args)
                if value:
                    break
            except Exception:
                # LOG
                continue

        if not value:
            value = kwargs.pop('default', None)

        return value
