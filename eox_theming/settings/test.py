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
EOX_THEMING_EDXMAKO_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_mako_tests'
EOX_THEMING_BASE_LOADER_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_loaders_tests'


def plugin_settings(settings):  # pylint: disable=function-redefined
    """
    For the platform tests, we want everything to be disabled
    """
    theme_template_loader = 'openedx.core.djangoapps.theming.template_loaders.ThemeTemplateLoader'
    settings.TEMPLATES[0]['OPTIONS']['loaders'][0] = theme_template_loader

    try:
        settings.MIDDLEWARE = [
            'openedx.core.djangoapps.theming.middleware.CurrentSiteThemeMiddleware' if 'EoxThemeMiddleware' in x else x
            for x in settings.MIDDLEWARE
        ]
    except AttributeError:
        pass

    settings.STATICFILES_STORAGE = 'openedx.core.storage.ProductionStorage'

    settings.STATICFILES_FINDERS = [
        x for x in settings.STATICFILES_FINDERS if 'EoxThemeFilesFinder' not in x
    ]
