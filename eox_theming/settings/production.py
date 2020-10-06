"""
Production Django settings for eox_theming project.
"""

from __future__ import unicode_literals


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.EOX_THEMING_DEFAULT_THEME_NAME = getattr(settings, 'ENV_TOKENS', {}).get(
        'EOX_THEMING_DEFAULT_THEME_NAME',
        settings.EOX_THEMING_DEFAULT_THEME_NAME
    )
