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

CONTEXT_PROCESSORS = [
    # This is a minimum context processors list extracted from lms/envs/common.py in edunext-platform
    'django.template.context_processors.request',
    'django.template.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.i18n',
    'django.template.context_processors.csrf',

    # eox-theming specific context processors
    'eox_theming.theming.context_processor.eox_configuration',
]

TEMPLATES = [
    {
        'NAME': 'django',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
        'OPTIONS': {},
    },
    {
        'NAME': 'mako',
        'BACKEND': 'eox_theming.tests.mako_backend.Mako',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS,
        },
    },
]

SITE_NAME = 'default.eox-theming.site'

EOX_THEMING_DEFAULT_THEME_NAME = 'default-theme'

EOX_THEMING_CONFIGURATION_HELPER_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_configuration_helpers_tests'
EOX_THEMING_THEMING_HELPER_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_theming_helpers_tests'
EOX_THEMING_EDXMAKO_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_mako_tests'
EOX_THEMING_BASE_LOADER_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_loaders_tests'


def plugin_settings(settings):  # pylint: disable=function-redefined, unused-argument
    """
    For the platform tests, we want everything to be disabled
    """
    pass
