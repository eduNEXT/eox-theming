"""
"""
from eox_theming.edxapp_wrapper.loaders import get_openedx_theme_loader

OpenedxThemeLoader = get_openedx_theme_loader()


class EoxThemeTemplateLoader(OpenedxThemeLoader):
    """

    See: openedx.core.djangoapps.theming.template_loaders.py
    """

    pass

