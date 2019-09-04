"""
Manages the diferent access, storage locations and methods used to read the configuration of a theme
"""


class ThemingConfiguration(object):
    """
    This class must handle all the calls to the diferential settings a theme will be allowed to use
    """

    @staticmethod
    def options(*args, **kwargs):  # pylint: disable=unused-argument
        """Main method for accessing the current configuration for the theme"""
        return 'example'
