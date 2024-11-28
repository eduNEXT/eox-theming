===========
EOX Theming
===========
|Maintainance Badge| |Test Badge| |PyPI Badge| |Python Badge|

.. |Maintainance Badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
   :alt: Maintainance Status
.. |Test Badge| image:: https://img.shields.io/github/actions/workflow/status/edunext/eox-theming/.github%2Fworkflows%2Ftests.yml?label=Test
   :alt: GitHub Actions Workflow Test Status
.. |PyPI Badge| image:: https://img.shields.io/pypi/v/eox-theming?label=PyPI
   :alt: PyPI - Version
.. |Python Badge| image:: https://img.shields.io/pypi/pyversions/eox-theming.svg

Overview
========

Eox theming is a plugin for `Open edX platform <https://github.com/openedx/edx-platform>`_, and part of the Edunext Open edX Extensions (aka EOX) that provides a series of tools to customize and launch themes.

This plugin improves the ``edx-platform`` by enhancing its Django and Mako template management. It allows for a more flexible theming process by introducing different levels of customization, enabling templates to be accessed from various theme directories where custom themes were stored.

The plugin conducts a hierarchical search for the requested template. It begins with the main theme (identified by ``name``), then moves to the second level (identified by ``parent``), and finally to the third level (identified by ``grandparent``). This hierarchical approach ensures that the plugin searches through the theme directories, prioritizing the most specific customizations over the default ones. You can find how to use the theme hierarchy in the upcoming `Usage`_ section.

Compatibility Notes
===================

+------------------+---------------+
| Open edX Release | Version       |
+==================+===============+
| Juniper          | >= 1.0 < 2.0  |
+------------------+---------------+
| Koa              | >= 2.0 < 3.0  |
+------------------+---------------+
| Lilac            | >= 2.0 < 8.0  |
+------------------+---------------+
| Maple            | >= 3.0 < 8.0  |
+------------------+---------------+
| Nutmeg           | >= 4.0 < 8.0  |
+------------------+---------------+
| Olive            | >= 5.0 < 8.0  |
+------------------+---------------+
| Palm             | >= 6.0 < 8.0  |
+------------------+---------------+
| Quince           | >= 7.0        |
+------------------+---------------+
| Redwood          | >= 7.2.0      |
+------------------+---------------+
| Sumac            | >= 8.1.0      |
+------------------+---------------+

⚠️ From Lilac version Django 2.2 is not supported, you should use Django 3.2 and eox-tenant >=4.0.

The plugin is configured for the latest release (Sumac). If you need compatibility for previous releases, go to the README of the relevant version tag and if it is necessary you can change the configuration in ``eox_theming/settings/common.py``.

For example, if you need compatibility for Koa, you can go to the `v2.0.0 README <https://github.com/eduNEXT/eox-theming/blob/v2.0.0/README.md>`_ to the ``Compatibility Notes`` section; you'll see something like this:

.. code-block:: python

    EOX_THEMING_STORAGE_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_storage'
    EOX_THEMING_EDXMAKO_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_mako'

Then you need to change the configuration in ``eox_theming/settings/common.py`` to use the appropriated ones.

🚨 If the release you are looking for is not listed, please note:

- If the Open edX release is compatible with the current eox-theming version (see `Compatibility Notes <https://github.com/eduNEXT/eox-theming?tab=readme-ov-file#compatibility-notes>`_), the default configuration is sufficient.
- If incompatible, you can refer to the README from the relevant version tag for configuration details (e.g., `v2.0.0 README <https://github.com/eduNEXT/eox-theming/blob/v2.0.0/README.md>`_).

Pre-requirements
================
#. Ensure you have a theme or themes following the `Changing Themes guide <https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/configuration/changing_appearance/theming/index.html>`_
#. Ensure your environment is well-configured according to the `Settings`_ section

   .. note::
      In order to simplify this process, we encourage the use of ``Distro Tutor Plugin`` for managing the addition and compilation of custom themes: `README of Distro <https://github.com/eduNEXT/tutor-contrib-edunext-distro?tab=readme-ov-file#themes>`_

Installation
============

#. Install the plugin adding it to ``OPENEDX_EXTRA_PIP_REQUIREMENTS`` in the ``config.yml``.

   .. code-block:: yaml

      OPENEDX_EXTRA_PIP_REQUIREMENTS:
         - eox-theming=={{version}}

#. Save the configuration with ``tutor config save``
#. Launch the platform with ``tutor local launch``

Settings
========

If you chose to use ``Distro Tutor Plugin``, just follow the instructions given in the `Themes section <https://github.com/eduNEXT/tutor-contrib-edunext-distro/blob/master/README.md#themes>`_. Otherwise, if you are doing the process manually, follow this steps:

#. Add the themes to your instance by adding your themes folder to the container shared folder ``env/build/openedx/themes``

#. Compile the themes after adding them:

   .. code-block:: bash

      tutor images build openedx
      tutor local do init

       # or

      tutor local launch

#. Add the following settings to your environment file ``env/apps/openedx/settings/lms/production.py``:

   .. code:: python

       COMPREHENSIVE_THEME_DIRS.extend(
           [
               "/path-to-your-themes-folder/in-the-lms-container/edx-platform",
               "/path-to-your-themes-folder/in-the-lms-container/edx-platform/sub-folder-with-more-themes",
           ]
       )
       EOX_THEMING_DEFAULT_THEME_NAME = "my-theme-1" # Or the theme you want

       ################## EOX_THEMING ##################
       if "EOX_THEMING_DEFAULT_THEME_NAME" in locals() and EOX_THEMING_DEFAULT_THEME_NAME:
           from lms.envs.common import _make_mako_template_dirs  # pylint: disable=import-error
           ENABLE_COMPREHENSIVE_THEMING = True
           TEMPLATES[1]["DIRS"] = _make_mako_template_dirs
           derive_settings("lms.envs.production")

Usage
=====

#. With ``eox-tenant`` create a new ``route`` or modify an existing one to point to a ``tenant config`` that lists your theme names in hierarchical order.  This hierarchy, which follows the priority for template lookup, uses the attributes ``name``, ``parent``, and ``grandparent`` respectively. Your ``tenant config`` JSON will need a property similar to the following one:

   .. code-block:: json

      {
          "EDNX_USE_SIGNAL": true,
          "THEME_OPTIONS": {
              "theme": {
                  "name":"my-theme-1",
                  "parent":"my-theme-2",
                  "grandparent":"my-theme-3"
              }
          }
      }

#. If you want to use different themes or modify the hierarchy, you just have to modify the `"THEME_OPTIONS"` property in your ``tenant config`` ensuring the theme you want to use was previously added to the platform.

Use case example
================

Having the following theme folder structure:

.. code-block:: txt

    themes-main-folder
    ├── edx-platform
        └── global-customizations
            └── lms
                └── static
                └── templates
            └── cms
                └── static
                └── templates
        └── more-specific-customizations
            └── org-customization-theme
                └── lms
                    └── static
                    └── templates
                └── cms
                    └── static
                    └── templates
        └── much-more-specific-customizations
            └── client-customization-theme
                └── lms
                    └── static
                    └── templates
                └── cms
                    └── static
                    └── templates

**NOTE**

You can see there are 3 levels of customization in the themes folder: ``global-customizations``, ``more-specific-customizations``, and ``much-more-specific-customizations``; the names are just to illustrate the hierarchy that the example will follow.

#. Add the ``themes-main-folder`` to ``env/build/openedx/themes`` folder in your environment to make the themes available to the platform; this folder is shared with the container.

#. Compile the themes running `tutor local launch`

#. Then, ensure are properly configured the `Settings`_ required and customize these: 

   .. code:: python

       COMPREHENSIVE_THEME_DIRS.extend(
           [
               "/openedx/themes/themes-main-folder/edx-platform",
               "/openedx/themes/themes-main-folder/edx-platform/more-specific-customizations",
               "/openedx/themes/themes-main-folder/edx-platform/most-specific-customizations"
           ]
       )
       EOX_THEMING_DEFAULT_THEME_NAME = "client-customization-theme"

#. And finally, restart the platform with the ``tutor local restart`` so this settings are properly added

#. Now you just have to create a ``Route`` with the ``"theme"`` attribute in the ``tenant config`` to point to your themes in the hierarchy you choose:

   .. code-block:: json

       "theme": {
         "name":"client-customization-theme",
         "parent":"org-customization-theme",
         "grandparent":"global-customizations"
       }

#. Restart again with ``tutor local restart`` and enjoy :)

Contributing
============

Contributions are welcome! See our `CONTRIBUTING`_
file for more information - it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/eox-theming/blob/master/CONTRIBUTING.rst


License
=======

This project is licensed under the AGPL-3.0 License. See the `LICENSE <LICENSE.txt>`_ file for details.
