"""
Production Django settings for eox_theming project.
"""

from __future__ import unicode_literals


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.STATICFILES_FINDERS = [
        'eox_theming.theming.finders.EoxThemeFilesFinder',
    ] + settings.STATICFILES_FINDERS

    if hasattr(settings, 'STORAGES'):
        new_storages = dict(settings.STORAGES)
        if 'staticfiles' in new_storages:
            static_cfg = dict(new_storages['staticfiles'])
            static_cfg['BACKEND'] = 'eox_theming.theming.storage.EoxDevelopmentStorage'
            new_storages['staticfiles'] = static_cfg
            settings.STORAGES = new_storages
