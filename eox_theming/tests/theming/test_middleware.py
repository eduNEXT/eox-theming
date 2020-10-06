# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Tests for the selection middleware
"""
from __future__ import absolute_import, unicode_literals

from django.test import RequestFactory, TestCase
from mock import mock, patch


class TestsEoxThemeMiddleware(TestCase):
    """ Tests for the eox_theming theme selection middleware """

    @patch('eox_theming.edxapp_wrapper.models.get_openedx_site_theme_model')
    def test_theme_selected(self, module_mock):
        """ The first implementation must return a site_theme in the requests object """
        request = RequestFactory().get('/')
        site_theme = mock.Mock()
        module_mock.return_value.return_value = site_theme

        from eox_theming.theming.middleware import EoxThemeMiddleware
        EoxThemeMiddleware().process_request(request)

        self.assertEqual(site_theme, request.site_theme)  # pylint: disable=no-member
