"""
Test util modules
"""
import re

from django.conf import settings


class TestThemingHelpersDirs(object):
    """
    Theme class for helpers_dirs
    """
    Theme = object


class TestConfigurationHelpers(object):
    """
    Test class mocking openedx configuration helpers
    """
    @staticmethod
    def get_value(val_name, default=None, **kwargs):  # pylint: disable=unused-argument
        """
        Return key from global settings
        """
        return getattr(settings, val_name, default)


def process_multiline_string(string):
    """
    This method remove new lines from multiline string outputs and
    other undesirable characters
    """
    # Multiple lines to single line and strip
    string = ''.join(string.splitlines()).strip()
    # In HTML case, remove spaces and tabs not inside html tags
    output = re.sub(r'(>)([\t\s]+)(<[^/])', r'\1\3', string)
    return output
