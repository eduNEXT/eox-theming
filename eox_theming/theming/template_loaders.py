"""
This stub module contains an empty extension point to modify the template loading
This module's logic applies both to Mako and Django Templates
"""
from eox_theming.edxapp_wrapper.loaders import get_openedx_theme_loader

OpenedxThemeLoader = get_openedx_theme_loader()


class EoxThemeTemplateLoader(OpenedxThemeLoader):
    """
    Emtpy for now, it allow for the extension of the ThemeTemplateLoader used
    for comprehensive theming.

    See: openedx.core.djangoapps.theming.template_loaders.py
    """
    pass
