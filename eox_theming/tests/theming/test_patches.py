"""
Module to test patched modules
"""
import operator
from collections import OrderedDict
# Forward compatibility for Python 3
from functools import reduce  # pylint: disable=redefined-builtin, useless-suppression

import six
from django.test import TestCase
from mock import patch
from path import Path

from eox_theming.theming.patches import EoxTheme


class TestEoxTheme(TestCase):
    """
    Tests for EoxTheme class which extends the Theme openedx class
    """
    def setUp(self):
        """
        Test Case Setup
        """
        theme1 = EoxTheme()
        theme1.name = 'mytheme'
        theme1.theme_dir_name = 'mytheme'
        theme1.themes_base_dir = Path('/my/path/to/theme')
        theme1.project_root = 'lms'
        theme1.path = (theme1.themes_base_dir
                       / theme1.theme_dir_name
                       / theme1.project_root)
        self.theme1 = theme1

        theme_parent = EoxTheme()
        theme_parent.name = 'mythemeparent'
        theme_parent.theme_dir_name = 'mythemeparent'
        theme_parent.themes_base_dir = Path('/my/path/to/themeparent')
        theme_parent.project_root = 'lms'
        theme_parent.path = (theme_parent.themes_base_dir
                             / theme_parent.theme_dir_name
                             / theme_parent.project_root)
        self.theme_parent = theme1

        theme_grandparent = EoxTheme()
        theme_grandparent.name = 'mythemegrandparent'
        theme_grandparent.theme_dir_name = 'mythemegrandparent'
        theme_grandparent.themes_base_dir = Path('/my/path/to/themegrandparent')
        theme_grandparent.project_root = 'lms'
        theme_grandparent.path = (theme_grandparent.themes_base_dir
                                  / theme_grandparent.theme_dir_name
                                  / theme_grandparent.project_root)
        self.theme_grandparent = theme1

    @patch('eox_theming.configuration.ThemingConfiguration.get_theme_name')
    def test_is_current_theme(self, get_theme_name_mock):
        """
        Check the is_current_theme method
        """
        # Test the case when the theme is the current theme
        get_theme_name_mock.return_value = 'mytheme'
        result = self.theme1.is_current_theme()
        get_theme_name_mock.assert_called_once()
        self.assertTrue(result)

        # Test the case when the theme is the current theme
        get_theme_name_mock.reset_mock()
        get_theme_name_mock.return_value = 'mynewtheme'
        result = self.theme1.is_current_theme()
        get_theme_name_mock.assert_called_once()
        self.assertFalse(result)

    @patch('eox_theming.configuration.ThemingConfiguration.get_wrapped_theme')
    @patch('eox_theming.configuration.ThemingConfiguration.options')
    def test_get_parent_themes(self, options_mock, get_wrapped_theme_mock):
        """
        Check the _get_parent_themes method
        """
        theme_options = {
            'theme': {
                'parent': 'mythemeparent',
                'grandparent': 'mythemegrandparent'
            }
        }

        themes_set = {
            'mythemeparent': self.theme_parent,
            'mythemegrandparent': self.theme_grandparent
        }

        def options_side_effect(*args, **kwargs):
            """
            ThemingConfiguration options side effect
            """
            if args:
                try:
                    value = reduce(operator.getitem, args, theme_options)
                except (AttributeError, KeyError):
                    value = None

            if value is None:
                value = kwargs.pop('default', None)

            return value

        def get_wrapped_theme_side_effect(name):
            """
            ThemingConfiguration get_wrapped_theme side effect
            """
            return themes_set.get(name, None)

        options_mock.side_effect = options_side_effect
        get_wrapped_theme_mock.side_effect = get_wrapped_theme_side_effect

        res = self.theme1._get_parent_themes()  # pylint: disable=protected-access
        options_mock.assert_called()
        get_wrapped_theme_mock.assert_called()
        self.assertListEqual(list(res.keys()), ['parent', 'grandparent'])

    @patch('eox_theming.theming.patches.EoxTheme._get_parent_themes')
    @patch('eox_theming.theming.patches.EoxTheme.is_current_theme')
    def test_extend_no_current_theme(self, is_current_theme_mock, get_parent_themes_mock):
        """
        Test that dirs are not modified when the theme is not the current theme
        """
        dirs = ['/mydir/fisrt', '/mydir/second']
        is_current_theme_mock.return_value = False
        res = self.theme1.extend_default_template_dirs(dirs)
        is_current_theme_mock.assert_called_once()
        get_parent_themes_mock.assert_not_called()
        self.assertListEqual(res, dirs)

    @patch('eox_theming.theming.patches.EoxTheme._get_parent_themes')
    @patch('eox_theming.theming.patches.EoxTheme.is_current_theme')
    def test_extend_template_dirs(self, is_current_theme_mock, get_parent_themes_mock):
        """
        Test that default template dirs are extended correctly
        """
        dirs = ['/mydir/fisrt', '/mydir/second']
        is_current_theme_mock.return_value = True

        parent_themes = OrderedDict()
        parent_themes['parent'] = self.theme_parent
        parent_themes['grandparent'] = self.theme_grandparent
        get_parent_themes_mock.return_value = parent_themes

        res = self.theme1.extend_default_template_dirs(dirs)
        is_current_theme_mock.assert_called_once()
        get_parent_themes_mock.assert_called_once()
        self.assertEqual(six.text_type(res[0]), six.text_type(self.theme1.path) + '/templates')
