"""
This stub module contains an empty extension point to modify the template loading
This module's logic applies both to Mako and Django Templates
"""
from eox_theming.configuration import ThemingConfiguration
from eox_theming.edxapp_wrapper.loaders import get_openedx_theme_loader, get_theme_filesystem_loader
from eox_theming.edxapp_wrapper.mako import get_mako_loader

MakoLoader = get_mako_loader()
OpenedxThemeLoader = get_openedx_theme_loader()
ThemeFilesystemLoader = get_theme_filesystem_loader()


class EoxThemeTemplateLoader(OpenedxThemeLoader):
    """
    Overrided to use EoxThemeFilesystemLoader instead of platform ThemeFilesystemLoader.

    See: openedx.core.djangoapps.theming.template_loaders.py
    """
    def __init__(self, *args):
        MakoLoader.__init__(self, EoxThemeFilesystemLoader(*args))


class EoxThemeFilesystemLoader(ThemeFilesystemLoader):
    """
    Overrode to append current theme, parent, and grandparent theme dirs so templates are looked up
    in the correct order.
    """

    @staticmethod
    def get_theme_template_sources():
        """
        Return template sources for the given theme and if request object is None (this would be the case for
        management commands) return template sources for all themes.
        """
        if not ThemingConfiguration.theming_helpers.get_current_request():
            # if request object is not present, then this method is being called inside a management
            # command and return all theme template sources for compression
            return ThemingConfiguration.theming_helpers.get_all_theme_template_dirs()
        else:
            # template is being accessed by a view, so return templates sources for current theme
            template_dirs = list()
            theme = ThemingConfiguration.theming_helpers.get_current_theme()
            if theme:
                template_dirs = theme.template_dirs

                parent_theme_dirs = EoxThemeFilesystemLoader.get_parent_theme_template_sources()
                grandparent_theme_dirs = EoxThemeFilesystemLoader.get_grandparent_theme_template_sources()
                # append parent and grandparent dirs to the end so templates are looked up in the correct order
                if isinstance(parent_theme_dirs, list) and isinstance(grandparent_theme_dirs, list):
                    template_dirs += parent_theme_dirs + grandparent_theme_dirs

            return template_dirs

    @staticmethod
    def get_parent_theme_template_sources():
        """
        Return the template dirs of the parent theme.
        """
        default_theme = ThemingConfiguration.get_parent_or_default_theme()
        template_paths = list()
        if default_theme:
            return default_theme.template_dirs

        return template_paths

    @staticmethod
    def get_grandparent_theme_template_sources():
        """
        Return the template dirs of the grandparent theme.
        """
        grandparent_theme = None
        grandparent_name = ThemingConfiguration.options('theme', 'grandparent', default=None)
        if grandparent_name:
            grandparent_theme = ThemingConfiguration.get_wrapped_theme(grandparent_name)

        template_paths = list()
        if grandparent_theme:
            return grandparent_theme.template_dirs

        return template_paths
