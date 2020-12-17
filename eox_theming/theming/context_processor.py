"""
This context processor is added to every request to render a mako or django template

It can be used using the theming.options(args) helper.
"""
from eox_theming.configuration import ThemingConfiguration
from eox_theming.theming.extra_scripts import process_scripts


def eox_configuration(request):
    """
    It inserts a theming object with the options helper function
    This is the last processor to be run.
    """
    return {
        'scripts': process_scripts(request.path_info),
        'theming': ThemingConfiguration,
    }
