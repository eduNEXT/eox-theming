"""
Test integration file.
"""
from django.test import TestCase


class TutorIntegrationTestCase(TestCase):
    """
    Tests integration with Open edX
    """

    # pylint: disable=import-outside-toplevel, unused-import
    def test_current_settings_code_imports(self):
        """
        Running this imports means that our backends import the right signature
        """
        # isort: off
        import eox_theming.edxapp_wrapper.backends.j_configuration_helpers
        import eox_theming.edxapp_wrapper.backends.j_finders
        import eox_theming.edxapp_wrapper.backends.j_loaders
        import eox_theming.edxapp_wrapper.backends.j_models
        import eox_theming.edxapp_wrapper.backends.j_theming_helpers
        import eox_theming.edxapp_wrapper.backends.l_mako
        import eox_theming.edxapp_wrapper.backends.l_storage
