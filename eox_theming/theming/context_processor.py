"""
"""

class ThemingConfiguration(object):
    """docstring for ThemingConfiguration"""

    @staticmethod
    def options(*args, **kwargs):
        return 'example'


def eox_configuration(*args, **kwargs):
    """
    It inserts a theming object with the options helper function
    This is the last processor to be run.
    """
    return {
        'theming': ThemingConfiguration
    }
