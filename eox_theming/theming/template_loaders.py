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
    Overrided to append parent theme dirs to the beginning so templates are looked up inside theme dir
    and parent theme dir first.
    """
    def get_template_sources(self, template_name, template_dirs=None):
        """
        Append to the beginning of the template dirs the dir of the parent theme.
        """
        if not template_dirs:
            template_dirs = self.engine.dirs

        parent_theme_dirs = self.get_parent_theme_template_sources()
        grandparent_theme_dirs = self.get_grandparent_theme_template_sources()
        # append parent theme dirs to the beginning so templates are looked up inside theme dir first
        if isinstance(parent_theme_dirs, list) and isinstance(grandparent_theme_dirs, list):
            template_dirs = parent_theme_dirs + grandparent_theme_dirs + template_dirs

        # on the next call, it will be appended to the beginning the site theme dir.
        return list(super(EoxThemeFilesystemLoader, self).get_template_sources(template_name, template_dirs))

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
