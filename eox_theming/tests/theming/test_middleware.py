# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Tests for the custom template tags
"""
from __future__ import absolute_import, unicode_literals

from django.test import RequestFactory, TestCase
from django.test.client import Client
from django.template import Context, Template
from mock import patch, mock



class TestsEoxThemeMiddleware(TestCase):
    """ Tests for the eox_theming theme selection middleware """

    @patch('eox_theming.edxapp_wrapper.models.get_openedx_site_theme_model')
    def test_theme_selected(self, module_mock):

        request = RequestFactory().get('/')
        site_theme = mock.Mock()
        module_mock.return_value.objects.get_or_create.return_value = site_theme, mock.Mock()

        from eox_theming.theming.middleware import EoxThemeMiddleware
        EoxThemeMiddleware().process_request(request)

        self.assertEquals(site_theme, request.site_theme)
