# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Tests for the template loaders
"""
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from mock import mock, patch
from path import Path

from eox_theming.theming.template_loaders import EoxThemeFilesystemLoader


class TestsEoxFSLoader(TestCase):
    """ Tests for the eox_theming filesystem loader """

    @patch('eox_theming.configuration.ThemingConfiguration.theming_helpers')
    @patch('eox_theming.configuration.ThemingConfiguration.get_parent_or_default_theme')
    def test_returned_default_theme_template_sources(self, parent_mock, helper_mock):
        """
        Test if it is returned the template dirs of the default theme.
        """
        theme = mock.Mock()
        theme.theme_dir_name = 'bragi'
        theme.name = 'bragi'
        helper_mock.get_current_theme.return_value = theme
        helper_mock.get_project_root_name.return_value = 'lms'

        parent_theme = mock.Mock()
        parent_theme.theme_dir_name = 'default-theme'
        parent_theme.name = 'default-theme'
        parent_theme.template_dirs = Path('/ednx/var/themes/edx-platform/default-theme')
        parent_mock.return_value = parent_theme

        parent_theme_sources = EoxThemeFilesystemLoader.get_parent_theme_template_sources()
        self.assertEqual(parent_theme_sources, parent_theme.template_dirs)

    @patch('eox_theming.configuration.ThemingConfiguration.theming_helpers')
    @patch('eox_theming.theming.template_loaders.EoxThemeFilesystemLoader.get_grandparent_theme_template_sources')
    @patch('eox_theming.theming.template_loaders.EoxThemeFilesystemLoader.get_parent_theme_template_sources')
    def test_returned_theme_template_sources(self, parent_mock, grandparent_mock, helper_mock):
        """
        Test if get_theme_template_sources method returns the template directories in the correct order.
        """
        theme = mock.Mock()
        theme.theme_dir_name = 'bragi'
        theme.name = 'bragi'
        theme.template_dirs = [Path('/ednx/var/themes/edx-platform/bragi')]
        helper_mock.get_current_theme.return_value = theme
        helper_mock.get_project_root_name.return_value = 'lms'

        parent_theme_template_dirs = [Path('/ednx/var/themes/edx-platform/parent-theme')]
        grandparent_theme_template_dirs = [Path('/ednx/var/themes/edx-platform/grandparent-theme')]
        template_dirs = theme.template_dirs + parent_theme_template_dirs + grandparent_theme_template_dirs

        parent_mock.return_value = parent_theme_template_dirs
        grandparent_mock.return_value = grandparent_theme_template_dirs

        theme_template_sources = EoxThemeFilesystemLoader.get_theme_template_sources()
        self.assertEqual(theme_template_sources, template_dirs)
