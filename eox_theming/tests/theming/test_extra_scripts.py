"""
Tests for the extra scripts.
"""
from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from mock import patch
from path import Path
from testfixtures import LogCapture

from eox_theming.theming.extra_scripts import process_scripts, validate_script_attributes


class TestsProcessExtraScripts(TestCase):
    """ Tests for extra scripts"""

    @patch('eox_theming.configuration.ThemingConfiguration.options')
    def test_returned_process_scripts(self, themingConfig_mock):
        """
        Test process_scripts function returns a dictionary with all the valid scripts
        in the correct order.
        """
        path = Path("/test")
        themingConfig_mock.return_value = {
            ".*/test": [
                {
                    "src": "https://www.test-external-script.com/js/myScript1.js",
                    "type": "external",
                    "media_type": "module"
                },
                {
                    "content": "alert('This alert box was called with the onload event');",
                    "type": "inline"
                }
            ]
        }
        test_scripts = [
            {
                "src": "https://www.test-external-script.com/js/myScript1.js",
                "type": "external",
                "media_type": "module"
            },
            {
                "content": "alert('This alert box was called with the onload event');",
                "type": "inline",
                "media_type": "text/javascript"
            },
        ]

        scripts = process_scripts(path)

        self.assertEqual(test_scripts, scripts)

    @patch('eox_theming.configuration.ThemingConfiguration')
    def test_returned_(self, themingConfig_mock):
        """
        Test process_scripts function returns only the scripts that have a valid configuration.
        """
        path = Path("/test")
        themingConfig_mock.return_value = {
            ".*/test": [
                {
                    "content": "alert('This alert box was called with the onload event');",
                    "type": "src"
                }
            ]
        }

        scripts = process_scripts(path)

        self.assertEqual(None, scripts)

    @patch('eox_theming.configuration.ThemingConfiguration')
    def test_returned_path_scripts(self, themingConfig_mock):
        """
        Test process_scripts function returns only the scripts that match the current request path.
        """
        path = Path("/test")
        themingConfig_mock.return_value = {
            ".*/dashboard": [
                {
                    "src": "https://www.test-external-script.com/js/myScript1.js",
                    "type": "external",
                    "media_type": "text/javascript"
                }
            ]
        }

        scripts = process_scripts(path)

        self.assertEqual(None, scripts)

    def test_validate_script_attributes_fails_silently(self):
        """
        Test validate_script_attributes function logs error when a script has a missing/incorrect attribute.
        """
        values = {
            "type": "external",
            "media_type": "text/javascript"
        }
        log_message = "Script could not get loaded. 'src' attribute is missing."

        with LogCapture() as log:
            validate_script_attributes(values)
            log.check(("eox_theming.theming.extra_scripts",
                       "ERROR",
                       log_message))
