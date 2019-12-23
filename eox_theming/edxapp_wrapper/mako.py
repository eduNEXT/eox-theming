""" Backend abstraction for edxmako. """
from importlib import import_module
from django.conf import settings


def get_mako_loader():
    """ Get mako loader """
    backend_function = settings.EOX_THEMING_EDXMAKO_BACKEND
    backend = import_module(backend_function)
    return backend.get_mako_loader()
