"""
This module abstracts the File Finder class from the platform core to prevent a dependency requirement while testing
"""
from importlib import import_module

from django.conf import settings


def get_openedx_theme_finder():
    """ Get the Open edX Theme Finder class. """

    backend = import_module(settings.EOX_THEMING_BASE_FINDER_BACKEND)

    return backend.get_openedx_theme_finder()
