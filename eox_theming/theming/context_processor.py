"""
This context processor is added to every request to render a mako or django template

It can be used using the theming.options(args) helper.
"""
from eox_theming.edxapp_wrapper.configuration_helpers import get_configuration_helper
from eox_theming.configuration import ThemingConfiguration
from eox_theming.api.v1.api import ThemingOptions


def eox_configuration(request):  # pylint: disable=unused-argument
    """
    It inserts a theming object with the options helper function
    This is the last processor to be run.
    """
    theming_api = get_active_theming_api()
    return {
        'theming': theming_api,
    }


def get_active_theming_api():
    """
    Determine which Theming API to use in the frontend
    """
    configuration_helpers = get_configuration_helper()
    localizer = {
        "V0": ThemingConfiguration,
        "V1": ThemingOptions()
    }

    current_api = configuration_helpers.get_value('EOX_THEMING_CURRENT_THEMING_API', 'V1')
    return localizer.get(current_api, localizer['V1'])
