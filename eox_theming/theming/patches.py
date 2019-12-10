"""
Monkey patches over openedX classes
"""
from collections import OrderedDict

from eox_theming.configuration import ThemingConfiguration
from eox_theming.edxapp_wrapper.theming_helpers import get_theme_class

# This is the original Theme class from edx-platform
# See openedx/core/djangoapps/theming/helpers_dirs.py
Theme = get_theme_class()


class EoxTheme(Theme):
    """
    This is an extension of the openedX Theme class
    """
    def is_current_theme(self):
        """
        Check if the theme instance is the current tenant theme
        """
        return self.name == ThemingConfiguration.get_theme_name()

    def _get_parent_themes(self):
        """
        Get the parent themes for the EoxTheme instance
        """
        parent_themes = OrderedDict()
        # The order of this list is important!
        parent_types = ['parent', 'grandparent']

        for parent in parent_types:
            parent_themes[parent] = None
            parent_theme_name = ThemingConfiguration.options('theme', parent, default=None)
            if parent_theme_name:
                parent_themes[parent] = ThemingConfiguration.get_wrapped_theme(parent_theme_name)

        return parent_themes

    def extend_default_template_dirs(self, dirs):
        """
        Given a list of default template dirs, extend it by prepending the dirs of theme instance and
        its parents
        """
        if not self.is_current_theme():
            return dirs

        dirs = list(dirs)
        parent_themes = self._get_parent_themes()
        dirs_to_prepend = [theme.path / 'templates' for theme in parent_themes.values() if theme]
        dirs_to_prepend.insert(0, self.path / 'templates')

        return dirs_to_prepend + dirs
