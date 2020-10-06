# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Tests for eox theming paths
"""
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from mock import mock, patch
from path import Path

from eox_theming.theming.paths import get_template_path_with_theme, strip_site_theme_templates_path


class ThemingPathsTest(TestCase):
    """ Tests for the eox_theming paths module """

    @patch('eox_theming.configuration.ThemingConfiguration.theming_helpers')
    @patch('eox_theming.configuration.ThemingConfiguration.get_parent_or_default_theme')
    def test_strip_site_theme_from_uri(self, parent_mock, helper_mock):
        """
        Test site theme templates path is stripped from the given template path.
        """
        theme = mock.Mock()
        theme.theme_dir_name = 'bragi'
        helper_mock.get_current_theme.return_value = theme
        helper_mock.get_project_root_name.return_value = 'lms'

        default_theme = mock.Mock()
        default_theme.theme_dir_name = 'default-theme'
        default_theme.name = 'default_theme'
        default_theme.path = Path('/themes/default_theme/lms')
        default_theme.template_path = Path('default-theme/lms/templates')

        parent_mock.return_value = default_theme
        template_path = strip_site_theme_templates_path('bragi/lms/templates/header.html')
        self.assertEqual(template_path, 'header.html')

    @patch('eox_theming.configuration.ThemingConfiguration.theming_helpers')
    @patch('eox_theming.configuration.ThemingConfiguration.get_parent_or_default_theme')
    def test_strip_site_default_theme_from_uri(self, parent_mock, helper_mock):
        """
        Test default site theme templates path is stripped from the given template path.
        """
        theme = mock.Mock()
        theme.theme_dir_name = 'bragi'
        theme.name = 'bragi'
        helper_mock.get_current_theme.return_value = theme
        helper_mock.get_project_root_name.return_value = 'lms'

        default_theme = mock.Mock()
        default_theme.theme_dir_name = 'default-theme'
        default_theme.name = 'default_theme'
        default_theme.path = Path('/themes/default_theme/lms')
        default_theme.template_path = Path('default-theme/lms/templates')

        parent_mock.return_value = default_theme
        template_path = strip_site_theme_templates_path('default-theme/lms/templates/header.html')
        self.assertEqual(template_path, 'header.html')

        template_path = strip_site_theme_templates_path('/theme-name/lms/templates/header.html')
        self.assertNotEqual(template_path, 'header.html')

    @patch('os.path.exists')
    @patch('eox_theming.configuration.ThemingConfiguration.theming_helpers')
    @patch('eox_theming.configuration.Theme')
    def test_get_template_path_with_theme(self, theme_mock, helper_mock, os_mock):
        """
        Tests template paths are returned from enabled theme.
        """
        os_mock.return_value = True

        theme = mock.Mock()
        theme.theme_dir_name = 'bragi'
        theme.path = Path('/themes/bragi/lms')
        theme.template_path = Path('bragi/lms/templates')
        helper_mock.get_current_theme.return_value = theme
        helper_mock.get_project_root_name.return_value = 'lms'

        template_path = get_template_path_with_theme('header.html')

        theme_mock.assert_called_once()
        self.assertEqual(template_path, 'bragi/lms/templates/header.html')

    @patch('os.path.exists')
    @patch('eox_theming.configuration.ThemingConfiguration.theming_helpers')
    @patch('eox_theming.configuration.ThemingConfiguration.get_parent_or_default_theme')
    def test_get_template_with_parent_theme(self, parent_mock, helper_mock, os_mock):
        """
        Tests parent theme template paths are returned if template is not found in the theme.
        """
        os_mock.side_effect = [False, True]
        theme = mock.Mock()
        theme.theme_dir_name = 'bragi'
        theme.name = 'bragi'
        theme.path = Path('/themes/bragi/lms')
        theme.template_path = Path('bragi/lms/templates')

        default_theme = mock.Mock()
        default_theme.theme_dir_name = 'default-theme'
        default_theme.name = 'default_theme'
        default_theme.path = Path('/themes/default_theme/lms')
        default_theme.template_path = Path('default-theme/lms/templates')

        parent_mock.return_value = default_theme

        helper_mock.get_current_theme.return_value = theme
        helper_mock.get_project_root_name.return_value = 'lms'

        template_path = get_template_path_with_theme('header.html')
        self.assertEqual(template_path, 'default-theme/lms/templates/header.html')

    @patch('os.path.exists')
    @patch('eox_theming.configuration.ThemingConfiguration.theming_helpers')
    @patch('eox_theming.configuration.ThemingConfiguration.get_parent_or_default_theme')
    def test_get_template_not_found_in_themes(self, parent_mock, helper_mock, os_mock):
        """
        Tests default template paths are returned if template is not found in the theme.
        """
        os_mock.side_effect = [False, False]
        theme = mock.Mock()
        theme.theme_dir_name = 'bragi'
        theme.name = 'bragi'
        theme.path = Path('/themes/bragi/lms')
        theme.template_path = Path('bragi/lms/templates')

        default_theme = mock.Mock()
        default_theme.theme_dir_name = 'default-theme'
        default_theme.name = 'default_theme'
        default_theme.path = Path('/themes/default_theme/lms')
        default_theme.template_path = Path('default-theme/lms/templates')

        parent_mock.return_value = default_theme
        helper_mock.get_current_theme.return_value = theme
        helper_mock.get_project_root_name.return_value = 'lms'

        template_path = get_template_path_with_theme('header.html')
        self.assertEqual(template_path, 'header.html')
