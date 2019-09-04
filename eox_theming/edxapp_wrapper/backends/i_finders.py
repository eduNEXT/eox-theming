"""
Simple backend that returns the platform's ThemeFilesFinder class
"""
from openedx.core.djangoapps.theming.finders import ThemeFilesFinder  # pylint: disable=import-error


def get_openedx_theme_finder():
    """Return the Finder class when called during runtime"""
    return ThemeFilesFinder
