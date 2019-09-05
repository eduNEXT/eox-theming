"""
Simple backend that returns the platform's ThemeTemplateLoader class
"""
from openedx.core.djangoapps.theming.template_loaders import ThemeTemplateLoader  # pylint: disable=import-error


def get_openedx_theme_loader():
    """Return the template loader class when called during runtime"""
    return ThemeTemplateLoader
