"""
Common Django settings for eox_theming project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)

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
    More info: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.STATICFILES_FINDERS = [
        'eox_theming.theming.finders.EoxThemeFilesFinder',
    ] + getattr(settings, 'STATICFILES_FINDERS', [])

    try:
        settings.TEMPLATES[0]['OPTIONS']['loaders'][0] = 'eox_theming.theming.template_loaders.EoxThemeTemplateLoader'
    except (AttributeError, TypeError):
        logger.error("Couldn't set template loaders. Check your settings.")

    try:
        eox_configuration_path = 'eox_theming.theming.context_processor.eox_configuration'
        # Register the eox-theming context processor on ``CONTEXT_PROCESSORS``. Both the Django
        # and Mako template engines build their ``context_processors`` from this setting, so this
        # works across releases: earlier releases point each engine's ``context_processors`` at
        # this very list, while from Verawood onwards those entries are ``Derived`` values that
        # resolve to ``settings.CONTEXT_PROCESSORS`` and can no longer be mutated in place.
        # Appending to the ``Derived`` object raised an ``AttributeError`` that was silently
        # swallowed, so the ``theming`` variable was never injected and every legacy Mako page
        # failed with ``'Undefined' object has no attribute 'options'``.
        context_processors = getattr(settings, 'CONTEXT_PROCESSORS', None)
        if isinstance(context_processors, list):
            if eox_configuration_path not in context_processors:
                context_processors.append(eox_configuration_path)
        else:
            # Fallback for releases that don't expose a ``CONTEXT_PROCESSORS`` setting: register
            # on every template engine whose ``context_processors`` is still a plain list.
            for engine in settings.TEMPLATES:
                engine_context_processors = engine.get('OPTIONS', {}).get('context_processors')
                if isinstance(engine_context_processors, list) \
                        and eox_configuration_path not in engine_context_processors:
                    engine_context_processors.append(eox_configuration_path)

        settings.DEFAULT_TEMPLATE_ENGINE = settings.TEMPLATES[0]
    except (AttributeError, TypeError):
        logger.error("Couldn't register the eox-theming context processor. Check your settings.")

    try:
        settings.MIDDLEWARE = [
            'eox_theming.theming.middleware.EoxThemeMiddleware' if 'CurrentSiteThemeMiddleware' in x else x
            for x in settings.MIDDLEWARE
        ]
    except (AttributeError, TypeError):
        logger.error("Couldn't set MIDDLEWARE. Check your settings.")

    if hasattr(settings, 'STORAGES'):
        new_storages = dict(settings.STORAGES)
        if 'staticfiles' in new_storages:
            static_cfg = dict(new_storages['staticfiles'])
            static_cfg['BACKEND'] = 'eox_theming.theming.storage.EoxProductionStorage'
            new_storages['staticfiles'] = static_cfg
            settings.STORAGES = new_storages

    settings.EOX_THEMING_DEFAULT_THEME_NAME = 'bragi'

    settings.EOX_THEMING_CONFIG_SOURCES = [
        'from_eox_tenant_config_theming',
        'from_eox_tenant_config_lms',
        'from_eox_tenant_microsite_v1',
        'from_eox_tenant_microsite_v2',
        'from_eox_tenant_microsite_v0',
        'from_site_config',
        'from_django_settings',
    ]

    settings.EOX_THEMING_BASE_FINDER_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_finders'
    settings.EOX_THEMING_BASE_LOADER_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_loaders'
    settings.EOX_THEMING_SITE_THEME_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_models'
    settings.EOX_THEMING_CONFIGURATION_HELPER_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_configuration_helpers'
    settings.EOX_THEMING_THEMING_HELPER_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_theming_helpers'
    settings.EOX_THEMING_STORAGE_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_storage'
    settings.EOX_THEMING_EDXMAKO_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_mako'
