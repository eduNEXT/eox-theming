"""
Simple backend that returns the platform's ThemeTemplateLoader class
"""
from openedx.core.djangoapps.theming.template_loaders import ThemeTemplateLoader, ThemeFilesystemLoader  # pylint: disable=import-error


def get_openedx_theme_loader():
    """Return the template loader class when called during runtime"""
    return ThemeTemplateLoader


def get_theme_filesystem_loader():
    """Return the filesystem loader class when called during runtime"""
    return ThemeFilesystemLoader
