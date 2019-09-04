"""
"""
from eox_theming.configuration import ThemingConfiguration


def eox_configuration(*args, **kwargs):
    """
    It inserts a theming object with the options helper function
    This is the last processor to be run.
    """
    return {
        'theming': ThemingConfiguration,
    }
