""" Backend abstraction for theming helpers tests. """
from eox_theming.test_utils import TestThemingHelpersDirs


def get_theming_helpers():
    """ Backend abstraction used on the tests """
    return object


def get_theming_helpers_dirs():
    """ Backend to get the theming helpers dirs on the tests. """
    return TestThemingHelpersDirs()


def get_theme_class():
    """ Backend to get the Theme class on the tests. """
    return object
