"""
This module abstracts the storage defined in the platform
"""
from importlib import import_module

from django.conf import settings


def get_theme_storage():
    """ Get the Open edX Theme Finder class. """
    backend = import_module(settings.EOX_THEMING_STORAGE_BACKEND)
    return backend.get_theme_storage()


def get_themecached_mixin():
    """Return the ThemeCached mixin when called during runtime"""
    backend = import_module(settings.EOX_THEMING_STORAGE_BACKEND)
    return backend.get_themecached_mixin()


def get_themepipeline_mixin():
    """Return the Theme pipeline mixin when called during runtime"""
    backend = import_module(settings.EOX_THEMING_STORAGE_BACKEND)
    return backend.get_themepipeline_mixin()


def get_pipeline_forgiving_storage():
    """
    Return the PipelineForgiving storage when called during runtime
    No longer used on juniper.
    """
    backend = import_module(settings.EOX_THEMING_STORAGE_BACKEND)
    return backend.get_pipeline_forgiving_storage()


def get_production_mixin():
    """Return the Production storage mixin when called during runtime"""
    backend = import_module(settings.EOX_THEMING_STORAGE_BACKEND)
    return backend.get_production_mixin()
