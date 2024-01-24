=======================
Open edX Theming Plugin
=======================

Features
--------

This plugin provides a stable place from where to create and launch your openedx theme.


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

**NOTE**: From Lilac version Django 2.2 is not supported, you should use Django 3.2 and eox-tenant >=4.0.

The following changes to the plugin settings are necessary. If the release you are looking for is
not listed, then the accumulation of changes from previous releases is enough.

Juniper
~~~~~~~

.. code-block:: bash

    EOX_THEMING_BASE_FINDER_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_finders'
    EOX_THEMING_BASE_LOADER_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_loaders'
    EOX_THEMING_SITE_THEME_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_models'
    EOX_THEMING_CONFIGURATION_HELPER_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_configuration_helpers'
    EOX_THEMING_THEMING_HELPER_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_theming_helpers'
    EOX_THEMING_STORAGE_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_storage'
    STATICFILES_STORAGE = 'eox_theming.theming.storage.EoxProductionStorage'
    EOX_THEMING_EDXMAKO_BACKEND = 'eox_theming.edxapp_wrapper.backends.j_mako'


Koa (optional)**
~~~~~~~~~~~~~~~~

.. code-block:: bash

    EOX_THEMING_STORAGE_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_storage'
    EOX_THEMING_EDXMAKO_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_mako'


Lilac - Maple - Nutmeg - Olive - Palm - Quince
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    EOX_THEMING_STORAGE_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_storage'
    EOX_THEMING_EDXMAKO_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_mako'


Those settings can be changed in ``eox_theming/settings/common.py`` or, for example, in ansible configurations.

**NOTE**: the current ``common.py`` works with Open edX lilac version.

Installation
------------

Open edX devstack
~~~~~~~~~~~~~~~~~

- Clone this repo in the src folder of your devstack.
- Open a new Lms/Devstack shell.
- Install the plugin as follows: pip install -e /path/to/your/src/folder
- Restart lms/cms services.

Tutor
~~~~~

- Install the plugin with OPENEDX_EXTRA_PIP_REQUIREMENTS, this should be added in the config.yml. 
- Restart lms/cms services.

Usage
-----

Include a usage description for your plugin.

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
        More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
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
