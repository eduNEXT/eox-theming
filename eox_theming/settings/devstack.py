"""
Production Django settings for eox_theming project.
"""

from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.STATICFILES_FINDERS = [
        'eox_theming.theming.finders.EoxThemeFilesFinder',
    ] + settings.STATICFILES_FINDERS

    try:
        settings.STORAGES['staticfiles']['BACKEND'] = 'eox_theming.theming.storage.EoxDevelopmentStorage'
    except Exception:  # pylint: disable=broad-except
        logger.error("Couldn't set EoxThemeStorage as staticfiles storage backend. Check your settings configuration.")
