# -*- coding: utf-8 -*-
"""
Tests for the ThemingConfiguration class
"""
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from django.test.utils import override_settings

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

    def test_get_theme_name(self):
        """
        Test get_theme_name function.
        """
        theme = ThemingConfiguration.get_theme_name()
        self.assertEqual(theme, 'default-theme')  # pylint: disable=no-member

    @override_settings(EOX_THEMING_DEFAULT_THEME_NAME='default-theme/inherits/other-theme')
    def test_get_theme_name_tenant(self):
        """
        Test get_theme_name for microsite v0.
        """
        theme = ThemingConfiguration.get_theme_name()
        self.assertEqual(theme, 'other-theme')  # pylint: disable=no-member
