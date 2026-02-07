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
    More info: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    def resolve_settings(obj):
        """
        Ayudante para resolver objetos 'Derived' sin importar la clase
        y evitar errores de linter.
        """
        if hasattr(obj, '_resolve'):
            # pylint: disable=protected-access
            return obj._resolve(settings)
        return obj

    current_finders = getattr(settings, 'STATICFILES_FINDERS', [])
    current_finders = resolve_settings(current_finders)

    settings.STATICFILES_FINDERS = [
        'eox_theming.theming.finders.EoxThemeFilesFinder',
    ] + list(current_finders)

    eox_configuration_path = 'eox_theming.theming.context_processor.eox_configuration'

    templates = resolve_settings(getattr(settings, 'TEMPLATES', []))

    for template_engine in templates:
        options = template_engine.get('OPTIONS', {})
        cp_list = options.get('context_processors', [])
        cp_list = list(resolve_settings(cp_list))

        if eox_configuration_path not in cp_list:
            cp_list.append(eox_configuration_path)
            template_engine['OPTIONS']['context_processors'] = cp_list

    current_middleware = resolve_settings(getattr(settings, 'MIDDLEWARE', []))

    settings.MIDDLEWARE = [
        'eox_theming.theming.middleware.EoxThemeMiddleware' if 'CurrentSiteThemeMiddleware' in x else x
        for x in current_middleware
    ]

    # 4. Storage (Django 5)
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
