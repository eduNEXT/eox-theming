"""
Test Django settings for eox_theming project.
"""

from __future__ import unicode_literals

from .common import *  # pylint: disable=wildcard-import


class SettingsClass(object):
    """ dummy settings class """
    pass


SETTINGS = SettingsClass()
plugin_settings(SETTINGS)
vars().update(SETTINGS.__dict__)
INSTALLED_APPS = vars().get('INSTALLED_APPS', [])
TEST_INSTALLED_APPS = [
    'django.contrib.sites',
]
for app in TEST_INSTALLED_APPS:
    if app not in INSTALLED_APPS:
        INSTALLED_APPS.append(app)

ROOT_URLCONF = 'eox_theming.urls'
ALLOWED_HOSTS = ['*']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {},
    },
]

EOX_THEMING_DEFAULT_THEME_NAME = 'default-theme'

EOX_THEMING_CONFIGURATION_HELPER_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_configuration_helpers_tests'
EOX_THEMING_THEMING_HELPER_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_theming_helpers_tests'


def plugin_settings(settings):  # pylint: disable=function-redefined, unused-argument
    """
    For the platform tests, we want everything to be disabled
    """
    pass
