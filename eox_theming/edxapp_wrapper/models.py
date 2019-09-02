"""
"""

from importlib import import_module
from django.conf import settings


def get_openedx_site_theme_model():
    """ Get the Open edX site theme model class. """

    backend = import_module(settings.EOX_THEMING_SITE_THEME_BACKEND)

    return backend.get_openedx_site_theme_model()
