"""
App configuration for eox_theming.
"""

from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings


class EoxThemingConfig(AppConfig):
    """
    Open edX Theming Plugin configuration.
    """
    name = 'eox_theming'
    verbose_name = 'Open edX Theming Plugin'

    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'eox_theming',
                'regex': r'^eox-theming/',
                'relative_path': 'urls',
            },
            'cms.djangoapp': {
                'namespace': 'eox_theming',
                'regex': r'^eox-theming/',
                'relative_path': 'urls',
            }
        },
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'test': {'relative_path': 'settings.test'},
                'production': {'relative_path': 'settings.production'},
                'devstack': {'relative_path': 'settings.devstack'},
            },
            'cms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'test': {'relative_path': 'settings.test'},
                'production': {'relative_path': 'settings.production'},
            },
        }
    }

    def ready(self):
        """
        Method to perform actions after apps registry is ended
        Setup mako lookup directories.
        See: common.djangoapps.edxmako.apps.py
        """
        from eox_theming.theming.paths import add_lookup, clear_lookups
        for backend in settings.TEMPLATES:
            if 'edxmako' not in backend['BACKEND']:
                continue
            namespace = backend['OPTIONS'].get('namespace', 'main')
            directories = backend['DIRS']
            clear_lookups(namespace)
            for directory in directories:
                add_lookup(namespace, directory)

        self.apply_patches()

    def apply_patches(self):
        """
        Method to apply monkey patches over openedX classes
        """
        from eox_theming.edxapp_wrapper.theming_helpers import get_theming_helpers_dirs, get_theming_helpers
        from eox_theming import configuration
        from eox_theming.theming.patches import EoxTheme

        theming_helpers = get_theming_helpers()
        theming_helpers_dirs = get_theming_helpers_dirs()
        theming_helpers.Theme = EoxTheme
        theming_helpers_dirs.Theme = EoxTheme
        configuration.Theme = EoxTheme
