""" Backend abstraction for theming helpers. """
from openedx.core.djangoapps.theming import helpers as theming_helpers  # pylint: disable=import-error


def get_theming_helpers():
    """ Backend to get the theming helpers. """
    return theming_helpers
