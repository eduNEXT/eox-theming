===========
EOX Theming
===========

|Maintainance Badge| |Test Badge| |PyPI Badge|

.. |Maintainance Badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
   :alt: Maintainance Status
.. |Test Badge| image:: https://img.shields.io/github/actions/workflow/status/edunext/eox-theming/.github%2Fworkflows%2Ftests.yml?label=Test
   :alt: GitHub Actions Workflow Test Status
.. |PyPI Badge| image:: https://img.shields.io/pypi/v/eox-theming?label=PyPI
   :alt: PyPI - Version

Django plugin that extends the tools and configuration for customizing the look and feel of the platform, as part of the
Edunext Open edX Extensions (EOX). 


Installation
============

1. Install eox-theming in Tutor with `OPENEDX_EXTRA_PIP_REQUIREMENTS` setting in the config.yml:

   .. code-block:: yaml
      
      OPENEDX_EXTRA_PIP_REQUIREMENTS:
         - eox-theming=={{version}}


2. Save the configuration with `tutor config save`.

3. Build the image and launch your platform with `tutor local launch`.


Usage
=====

Compatibility Notes
-------------------

+------------------+---------------------+
| Open edX Release |        Version      |
+==================+=====================+
|     Juniper      |       >= 1.0 < 2.0  |
+------------------+---------------------+
|       Koa        |       >= 2.0 < 3.0  |
+------------------+---------------------+
|      Lilac       |       >= 2.0        |
+------------------+---------------------+
|      Maple       |       >= 3.0        |
+------------------+---------------------+
|      Nutmeg      |       >= 4.0        |
+------------------+---------------------+
|      Olive       |       >= 5.0        |
+------------------+---------------------+
|      Palm        |       >= 6.0        |
+------------------+---------------------+
|      Quince      |       >= 7.0        |
+------------------+---------------------+

⚠️ From Lilac version Django 2.2 is not supported, you should use Django 3.2 and eox-tenant >=4.0.

The plugin is configured for the latest release (Redwood). The following changes in the plugin settings should be applied to be used for previous releases.


Lilac - Maple - Nutmeg - Olive - Palm - Quince
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    EOX_THEMING_STORAGE_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_storage'
    EOX_THEMING_EDXMAKO_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_mako'


Those settings can be changed in ``eox_theming/settings/common.py`` or, for example, in the instance configurations.

🚨 If the release you are looking for is not listed, please note:

- If the Open edX release is compatible with the current eox-theming version (see `Compatibility Notes <https://github.com/eduNEXT/eox-theming?tab=readme-ov-file#compatibility-notes>`_), the default configuration is sufficient.
- If incompatible, you can refer to the README from the relevant version tag for configuration details (e.g., `v6.0.0 README <https://github.com/eduNEXT/eox-theming/blob/v6.0.0/README.rst>`_).

Settings
~~~~~~~~

To start using eox-theming, we must make the settings shown in the tenant settings (if we don't have one created, create it and configure it), add some available settings to the tenant:

.. code-block:: json

    {"THEME_OPTIONS":{"theme":{"grandparent":"test-3","name":"test-1","parent":"test-2"}}}


For this, you must also make sure you have eox-tenant installed in your environment,
and to configure it we must locate the `common.py`_
file and set the ``USE_EOX_TENANT`` variable to ``True``

.. _common.py: https://github.com/eduNEXT/eox-tenant/blob/master/eox_tenant/settings/common.py#L52

Include the follow configuration in devstack.py:

.. code-block:: python

    """
    Production Django settings for eox_theming project.
    """

    from __future__ import unicode_literals


    def plugin_settings(settings):
        """
        Set of plugin settings used by the Open Edx platform.
        More info: https://github.com/openedx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
        """
        settings.STATICFILES_FINDERS = [
            'eox_theming.theming.finders.EoxThemeFilesFinder',
        ] + settings.STATICFILES_FINDERS

        settings.STATICFILES_STORAGE = 'eox_theming.theming.storage.EoxDevelopmentStorage'

        from lms.envs.common import _make_mako_template_dirs # pylint: disable=import-error
        settings.ENABLE_COMPREHENSIVE_THEMING = True
        settings.COMPREHENSIVE_THEME_DIRS = [
            '/edx/src/themes/ednx-test-themes/edx-platform/',
        ]
        settings.TEMPLATES[1]["DIRS"] = _make_mako_template_dirs
        settings.derive_settings("lms.envs.devstack")


Note that in ``COMPREHENSIVE_THEME_DIRS`` it must contain a list of directories where the folders of the themes to be tested are located.

Contributing
------------

Contributions are welcome! See our `CONTRIBUTING`_
file for more information - it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/eox-theming/blob/master/CONTRIBUTING.rst
