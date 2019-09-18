""" Backend abstraction for theming helpers. """
from importlib import import_module
from django.conf import settings


def get_theming_helpers(*args, **kwargs):
    """ Get theming helper module """
    backend_function = settings.EOX_THEMING_THEMING_HELPER_BACKEND
    backend = import_module(backend_function)
    return backend.get_theming_helpers(*args, **kwargs)
