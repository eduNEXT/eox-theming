""" Backend abstraction for theming helpers. """
from openedx.core.djangoapps.theming import helpers as theming_helpers  # pylint: disable=import-error
from openedx.core.djangoapps.theming import helpers_dirs as theming_helpers_dirs  # pylint: disable=import-error


def get_theming_helpers():
    """ Backend to get the theming helpers. """
    return theming_helpers


def get_theming_helpers_dirs():
    """ Backend to get the theming helpers dirs. """
    return theming_helpers_dirs


def get_theme_class():
    """ Backend to get the Theme class. """
    return theming_helpers_dirs.Theme
