"""
"""

from importlib import import_module
from django.conf import settings


def get_openedx_theme_loader():
    """ Get the Open edX template loader class. """

    backend = import_module(settings.EOX_THEMING_BASE_LOADER_BACKEND)

    return backend.get_openedx_theme_loader()
