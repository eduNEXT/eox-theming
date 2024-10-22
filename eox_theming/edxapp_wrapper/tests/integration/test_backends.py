"""
This module tests the backends of the edxapp_wrapper
"""


# pylint: disable=import-outside-toplevel, unused-import
def test_current_settings_code_imports():
    """
    Running this imports means that our backends import the right signature
    """
    import eox_theming.edxapp_wrapper.backends.j_configuration_helpers
    import eox_theming.edxapp_wrapper.backends.j_finders
    import eox_theming.edxapp_wrapper.backends.j_loaders
    import eox_theming.edxapp_wrapper.backends.j_models
    import eox_theming.edxapp_wrapper.backends.j_theming_helpers
    import eox_theming.edxapp_wrapper.backends.l_mako
    import eox_theming.edxapp_wrapper.backends.l_storage
