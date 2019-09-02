# -*- coding: utf-8 -*-
"""
Tests for the admin views
"""
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from django.urls import reverse, exceptions


class TestUrls(TestCase):
    """ Tests for the urls module """

    def test_urls(self):
        """ Check that url.py loads """
        with self.assertRaises(exceptions.NoReverseMatch):
            reverse('non-existant')
