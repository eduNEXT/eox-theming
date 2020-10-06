"""Backend abstraction for edxmako. """
from importlib import import_module

from django.conf import settings


def get_mako_loader():
    """ Get mako loader """
    backend_function = settings.EOX_THEMING_EDXMAKO_BACKEND
    backend = import_module(backend_function)
    return backend.get_mako_loader()


def get_dynamictemplate_lookup(*args, **kwargs):
    """ Get DynamicTemplateLookup class """
    backend_function = settings.EOX_THEMING_EDXMAKO_BACKEND
    backend = import_module(backend_function)
    return backend.get_dynamictemplate_lookup(*args, **kwargs)


def get_top_level_template_uri(*args, **kwargs):
    """ Get TopLevelTemplateUri """
    backend_function = settings.EOX_THEMING_EDXMAKO_BACKEND
    backend = import_module(backend_function)
    return backend.get_top_level_template_uri(*args, **kwargs)


def get_lookup(*args, **kwargs):
    """ Get lookup from platform code """
    backend_function = settings.EOX_THEMING_EDXMAKO_BACKEND
    backend = import_module(backend_function)
    return backend.get_lookup(*args, **kwargs)


def get_clear_lookups(*args, **kwargs):
    """ Get clear lookups function """
    backend_function = settings.EOX_THEMING_EDXMAKO_BACKEND
    backend = import_module(backend_function)
    return backend.get_clear_lookups(*args, **kwargs)
