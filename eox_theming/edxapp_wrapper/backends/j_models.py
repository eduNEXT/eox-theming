"""
Simple backend that returns the platform's SiteTheme model
"""
from openedx.core.djangoapps.theming.models import SiteTheme  # pylint: disable=import-error


def get_openedx_site_theme_model():
    """Return the model class when called during runtime"""
    return SiteTheme
