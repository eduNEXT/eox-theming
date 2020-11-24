"""
Simple backend that returns the platform's SiteTheme model
"""
from openedx.core.djangoapps.theming.storage import (  # pylint: disable=import-error
    ThemeCachedFilesMixin,
    ThemePipelineMixin,
    ThemeStorage,
)
from openedx.core.storage import ProductionMixin  # pylint: disable=import-error


def get_theme_storage():
    """Return the ThemeStorage class when called during runtime"""
    return ThemeStorage


def get_themecached_mixin():
    """Return the ThemeCached mixin when called during runtime"""
    return ThemeCachedFilesMixin


def get_themepipeline_mixin():
    """Return the Theme pipeline mixin when called during runtime"""
    return ThemePipelineMixin


def get_production_mixin():
    """Return ProductionMixin when called during runtime"""
    return ProductionMixin
