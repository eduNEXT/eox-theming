"""
Tests for :func:`eox_theming.settings.common.plugin_settings`.

These focus on the registration of the ``theming`` context processor, which must work both on
releases where each template engine's ``context_processors`` is a plain list and on Verawood and
later releases, where those entries are ``Derived`` values that resolve to
``settings.CONTEXT_PROCESSORS``.
"""
from types import SimpleNamespace

from django.test import TestCase

from eox_theming.settings.common import plugin_settings

CONTEXT_PROCESSOR_PATH = 'eox_theming.theming.context_processor.eox_configuration'


def build_settings(**overrides):
    """Return a minimal settings-like object with everything ``plugin_settings`` touches."""
    settings = SimpleNamespace(
        STATICFILES_FINDERS=[],
        MIDDLEWARE=[],
        TEMPLATES=[
            {'OPTIONS': {'loaders': ['placeholder'], 'context_processors': []}},
            {'OPTIONS': {'context_processors': []}},
        ],
    )
    for key, value in overrides.items():
        setattr(settings, key, value)
    return settings


class DerivedContextProcessors:
    """Stand-in for the edx-platform ``Derived`` object: not a list, not iterable."""


class PluginSettingsContextProcessorTests(TestCase):
    """Tests for the ``theming`` context processor registration."""

    def test_registers_on_context_processors_setting(self):
        """Verawood+: engines use ``Derived`` values, so registration lands on CONTEXT_PROCESSORS."""
        settings = build_settings(CONTEXT_PROCESSORS=[])
        settings.TEMPLATES[0]['OPTIONS']['context_processors'] = DerivedContextProcessors()
        settings.TEMPLATES[1]['OPTIONS']['context_processors'] = DerivedContextProcessors()

        plugin_settings(settings)

        self.assertIn(CONTEXT_PROCESSOR_PATH, settings.CONTEXT_PROCESSORS)

    def test_registration_is_idempotent(self):
        """Registering twice must not duplicate the context processor."""
        settings = build_settings(CONTEXT_PROCESSORS=[CONTEXT_PROCESSOR_PATH])

        plugin_settings(settings)

        self.assertEqual(settings.CONTEXT_PROCESSORS.count(CONTEXT_PROCESSOR_PATH), 1)

    def test_legacy_shared_list_reaches_template_engines(self):
        """Legacy releases share one list between CONTEXT_PROCESSORS and every engine."""
        shared = []
        settings = build_settings(CONTEXT_PROCESSORS=shared)
        settings.TEMPLATES[0]['OPTIONS']['context_processors'] = shared
        settings.TEMPLATES[1]['OPTIONS']['context_processors'] = shared

        plugin_settings(settings)

        self.assertIn(CONTEXT_PROCESSOR_PATH, settings.TEMPLATES[0]['OPTIONS']['context_processors'])
        self.assertIn(CONTEXT_PROCESSOR_PATH, settings.TEMPLATES[1]['OPTIONS']['context_processors'])

    def test_fallback_when_no_context_processors_setting(self):
        """Without a CONTEXT_PROCESSORS setting, register on each engine's list."""
        settings = build_settings()  # no CONTEXT_PROCESSORS attribute

        plugin_settings(settings)

        self.assertIn(CONTEXT_PROCESSOR_PATH, settings.TEMPLATES[0]['OPTIONS']['context_processors'])
        self.assertIn(CONTEXT_PROCESSOR_PATH, settings.TEMPLATES[1]['OPTIONS']['context_processors'])
