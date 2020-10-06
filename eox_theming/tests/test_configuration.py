# -*- coding: utf-8 -*-
"""
Tests for the ThemingConfiguration class
"""
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from django.test.utils import override_settings
from mock import patch

from eox_theming.configuration import ThemingConfiguration


class TestThemingConfiguration(TestCase):
    """ Tests for the ThemingConfiguration class """

    def test_options_call_default(self):
        """ Calling options must return the default """
        result = ThemingConfiguration.options('section', 'item', default='Unique_string')
        self.assertEqual('Unique_string', result)

    @override_settings(THEME_OPTIONS={'section': {'item': 'Given_String'}})
    def test_options_call_exists_django_settings(self):
        """ Calling options must return the real value  """
        result = ThemingConfiguration.options('section', 'item', default='Unique_string')
        self.assertEqual('Given_String', result)

    @override_settings(THEME_OPTIONS=[])
    def test_options_call_error(self):
        """ Calling options with error data must return the Default """
        result = ThemingConfiguration.options('section', 'item', default='Unique_string')
        self.assertEqual('Unique_string', result)

    @override_settings(THEME_OPTIONS={'section': {'item': False}})
    def test_falsy_value(self):
        """ Calling options must return the value defined in the source even if that is false """
        result = ThemingConfiguration.options('section', 'item', default=None)
        self.assertIsNotNone(result)
        self.assertFalse(result)

    def test_get_theme_name(self):
        """
        Test get_theme_name function.
        """
        theme = ThemingConfiguration.get_theme_name()
        self.assertEqual(theme, 'default-theme')

    @override_settings(EOX_THEMING_DEFAULT_THEME_NAME='default-theme/inherits/other-theme')
    def test_get_theme_name_tenant(self):
        """
        Test get_theme_name for microsite v0.
        """
        theme = ThemingConfiguration.get_theme_name()
        self.assertEqual(theme, 'other-theme')

    @override_settings(THEME_OPTIONS=[])
    @patch('eox_theming.edxapp_wrapper.config_sources.configuration_helpers')
    def test_comfiguration_helpers_called(self, conf_helpers_mock):
        """ If not found on settings it should use configuration helpers """
        ThemingConfiguration.options('section', 'item', default='Unique_string')
        conf_helpers_mock.get_value.assert_called()

    @patch('eox_theming.configuration.ThemingConfiguration.theming_helpers')
    @patch('eox_theming.configuration.Theme')
    def test_get_parent_theme_is_default(self, theme_mock, helper_mock):
        """
        Test that method return default theme if parent is not defined.
        """
        helper_mock.get_project_root_name.return_value = 'lms'
        helper_mock.get_theme_base_dir.return_value = 'templates'
        ThemingConfiguration.get_parent_or_default_theme()
        theme_mock.assert_called_with(
            name='default-theme',
            project_root='lms',
            theme_dir_name='default-theme',
            themes_base_dir='templates'
        )

    @override_settings(THEME_OPTIONS={'theme': {'parent': 'parent-theme'}})
    @patch('eox_theming.configuration.ThemingConfiguration.theming_helpers')
    @patch('eox_theming.configuration.Theme')
    def test_get_parent_theme(self, theme_mock, helper_mock):
        """
        Test that method return parent theme.
        """
        helper_mock.get_project_root_name.return_value = 'lms'
        helper_mock.get_theme_base_dir.return_value = 'templates'
        ThemingConfiguration.get_parent_or_default_theme()
        theme_mock.assert_called_with(
            name='parent-theme',
            project_root='lms',
            theme_dir_name='parent-theme',
            themes_base_dir='templates'
        )
