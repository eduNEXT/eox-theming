# -*- coding: utf-8 -*-
"""
Tests for the custom template tags
"""
from __future__ import absolute_import, unicode_literals

from django.template import Context, Template
from django.test import TestCase
from mock import patch


class TestsEoxThemingTags(TestCase):
    """ Tests for the eox_theming template tags """

    @patch('eox_theming.templatetags.eox_theming.ThemingConfiguration.options', return_value='Unique_Return_Value')
    def test_tag_renders(self, _):
        """ Rendering the template must return the value of calling theming.options """
        context = {}
        context = Context(context)

        result = Template("""
            {% load eox_theming %}
            {% theming_options footer item subitem default='my_default' %}
        """).render(context)

        self.assertIn('Unique_Return_Value', result)
