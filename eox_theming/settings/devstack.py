"""
Production Django settings for eox_theming project.
"""

from __future__ import unicode_literals


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.STATICFILES_FINDERS = [
        'eox_theming.theming.finders.EoxThemeFilesFinder',
    ] + settings.STATICFILES_FINDERS

    settings.STATICFILES_STORAGE = 'eox_theming.theming.storage.EoxDevelopmentStorage'
