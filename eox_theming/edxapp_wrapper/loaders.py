"""
This module abstracts the Template Loader class from the
platform core toprevent a dependency requirement while testing
"""
from importlib import import_module

from django.conf import settings


def get_openedx_theme_loader():
    """ Get the Open edX template loader class. """
    backend = import_module(settings.EOX_THEMING_BASE_LOADER_BACKEND)
    return backend.get_openedx_theme_loader()


def get_theme_filesystem_loader():
    """ Get the Open edX filesystem loader class. """
    backend = import_module(settings.EOX_THEMING_BASE_LOADER_BACKEND)
    return backend.get_theme_filesystem_loader()
