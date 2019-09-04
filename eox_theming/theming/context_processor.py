"""
This context processor is added to every request to render a mako or django template

It can be used using the theming.options(args) helper.
"""
from eox_theming.configuration import ThemingConfiguration


def eox_configuration(request):  # pylint: disable=unused-argument
    """
    It inserts a theming object with the options helper function
    This is the last processor to be run.
    """
    return {
        'theming': ThemingConfiguration,
    }
