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
    def resolve_completely(obj):
        """
        Resuelve objetos 'Derived' de forma recursiva hasta obtener el valor real.
        """
        for _ in range(10):
            if hasattr(obj, '_resolve'):
                # pylint: disable=protected-access
                obj = obj._resolve(settings)
            else:
                break
        return obj

    finders = resolve_completely(getattr(settings, 'STATICFILES_FINDERS', []))
    settings.STATICFILES_FINDERS = [
        'eox_theming.theming.finders.EoxThemeFilesFinder',
    ] + list(finders)

    eox_cp = 'eox_theming.theming.context_processor.eox_configuration'
    templates = resolve_completely(getattr(settings, 'TEMPLATES', []))

    if isinstance(templates, (list, tuple)):
        updated_templates = []
        for engine in templates:
            engine_dict = dict(engine)
            options = dict(engine_dict.get('OPTIONS', {}))

            cp_list = options.get('context_processors', [])
            cp_list = list(resolve_completely(cp_list))

            if eox_cp not in cp_list:
                cp_list.append(eox_cp)

            options['context_processors'] = cp_list
            engine_dict['OPTIONS'] = options
            updated_templates.append(engine_dict)

        settings.TEMPLATES = updated_templates

    middleware = resolve_completely(getattr(settings, 'MIDDLEWARE', []))
    settings.MIDDLEWARE = [
        'eox_theming.theming.middleware.EoxThemeMiddleware' if 'CurrentSiteThemeMiddleware' in x else x
        for x in middleware
    ]

    if hasattr(settings, 'STORAGES'):
        current_storages = dict(resolve_completely(settings.STORAGES))
        if 'staticfiles' in current_storages:
            static_cfg = dict(current_storages['staticfiles'])
            static_cfg['BACKEND'] = 'eox_theming.theming.storage.EoxProductionStorage'
            current_storages['staticfiles'] = static_cfg
            settings.STORAGES = current_storages

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
