# -*- coding: utf-8 -*-
"""
Tests for the admin views
"""
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from django.urls import exceptions, reverse

import eox_theming


class TestUrls(TestCase):
    """ Tests for the urls module """

    def test_urls(self):
        """ Check that url.py loads """
        with self.assertRaises(exceptions.NoReverseMatch):
            reverse('non-existant')


class TestInfoView(TestCase):
    """ Tests for the eox-info page """

    def test_version_is_present(self):
        """ Check that test version is present """
        response = self.client.get('/eox-info')
        self.assertContains(response, eox_theming.__version__)
