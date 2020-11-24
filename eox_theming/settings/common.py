"""
Common Django settings for eox_theming project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from __future__ import unicode_literals

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'eox_theming'
]

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_TZ = True

# This key needs to be defined so that the check_apps_ready passes and the
# AppRegistry is loaded
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.STATICFILES_FINDERS = [
        'eox_theming.theming.finders.EoxThemeFilesFinder',
    ] + getattr(settings, 'STATICFILES_FINDERS', [])

    try:
        settings.TEMPLATES[0]['OPTIONS']['loaders'][0] = 'eox_theming.theming.template_loaders.EoxThemeTemplateLoader'
    except AttributeError:
        # We must find a way to register this error
        pass

    try:
        eox_configuration_path = 'eox_theming.theming.context_processor.eox_configuration'
        if eox_configuration_path not in settings.TEMPLATES[0]['OPTIONS']['context_processors']:
            settings.TEMPLATES[0]['OPTIONS']['context_processors'].append(eox_configuration_path)
        if eox_configuration_path not in settings.TEMPLATES[1]['OPTIONS']['context_processors']:
            settings.TEMPLATES[1]['OPTIONS']['context_processors'].append(eox_configuration_path)

        settings.DEFAULT_TEMPLATE_ENGINE = settings.TEMPLATES[0]
    except AttributeError:
        # We must find a way to register this error
        pass

    try:
        settings.MIDDLEWARE = [
            'eox_theming.theming.middleware.EoxThemeMiddleware' if 'CurrentSiteThemeMiddleware' in x else x
            for x in settings.MIDDLEWARE
        ]
    except AttributeError:
        # We must find a way to register this error.
        pass

    settings.EOX_THEMING_DEFAULT_THEME_NAME = 'bragi'

    settings.EOX_THEMING_CONFIG_SOURCES = [
        'from_eox_tenant_config_theming',
        'from_eox_tenant_config_lms',
        'from_eox_tenant_microsite_v1',
        'from_eox_tenant_microsite_v0',
        'from_site_config',
        'from_django_settings',
    ]

    settings.EOX_THEMING_BASE_FINDER_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_finders'
    settings.EOX_THEMING_BASE_LOADER_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_loaders'
    settings.EOX_THEMING_SITE_THEME_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_models'
    settings.EOX_THEMING_CONFIGURATION_HELPER_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_configuration_helpers'
    settings.EOX_THEMING_THEMING_HELPER_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_theming_helpers'
    settings.EOX_THEMING_STORAGE_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_storage'
    settings.STATICFILES_STORAGE = 'eox_theming.theming.storage.EoxProductionStorage'

    settings.EOX_THEMING_EDXMAKO_BACKEND = 'eox_theming.edxapp_wrapper.backends.i_mako'
