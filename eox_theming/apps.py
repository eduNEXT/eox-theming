"""
App configuration for eox_theming.
"""

from __future__ import unicode_literals

from django.apps import AppConfig


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
                'regex': r'^eox_theming/',
                'relative_path': 'urls',
            },
            'cms.djangoapp': {
                'namespace': 'eox_theming',
                'regex': r'^eox_theming/',
                'relative_path': 'urls',
            }
        },
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'test': {'relative_path': 'settings.test'},
                'aws': {'relative_path': 'settings.aws'},
                'production': {'relative_path': 'settings.production'},
                'devstack': {'relative_path': 'settings.devstack'},
            },
            'cms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
                'test': {'relative_path': 'settings.test'},
                'aws': {'relative_path': 'settings.aws'},
                'production': {'relative_path': 'settings.production'},
            },
        }
    }
