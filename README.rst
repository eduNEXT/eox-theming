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

********
Overview
********

Eox theming is a plugin for `Open edX platform <https://github.com/openedx/edx-platform>`_, and part of the Edunext Open edX Extensions (aka EOX) that provides a series of tools to customize and launch themes.

This plugin improves the ``edx-platform`` by enhancing its Django and Mako template management. It allows for a more flexible theming process by introducing different levels of customization, enabling templates to be accessed from various theme directories where custom themes were stored.

The plugin conducts a hierarchical search for the requested template. It begins with the main theme (identified by ``name``), then moves to the second level (identified by ``parent``), and finally to the third level (identified by ``grandparent``). This hierarchical approach ensures that the plugin searches through the theme directories, prioritizing the most specific customizations over the default ones. You can find how to use the theme hierarchy in the upcoming **Usage** section.

If you are looking for professional development or support with multitenancy or multi-sites in the Open edX platform, you can reach out to sales@edunext.co

*******************
Compatibility Notes
*******************

+------------------+--------------+
| Open edX Release | Version      |
+==================+==============+
| Juniper          | >= 1.0 < 2.0 |
+------------------+--------------+
| Koa              | >= 2.0 < 3.0 |
+------------------+--------------+
| Lilac            | >= 2.0       |
+------------------+--------------+
| Maple            | >= 3.0       |
+------------------+--------------+
| Nutmeg           | >= 4.0       |
+------------------+--------------+
| Olive            | >= 5.0       |
+------------------+--------------+
| Palm             | >= 6.0       |
+------------------+--------------+
| Quince           | >= 7.0       |
+------------------+--------------+
| Redwood          | >= 7.0       |
+------------------+--------------+

⚠️ From Lilac version Django 2.2 is not supported, you should use Django 3.2 and eox-tenant >=4.0.

The plugin is configured for the latest release (Redwood). If you need compatibility for previous releases, go to the README of the relevant version tag and if it is necessary you can change the configuration in ``eox_theming/settings/common.py``.

For example, if you need compatibility for Koa, you can go to the `v2.0.0 README <https://github.com/eduNEXT/eox-theming/blob/v2.0.0/README.md>`_ to the ``Compatibility Notes`` section; you'll see something like this:

.. code-block:: python

    EOX_THEMING_STORAGE_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_storage'
    EOX_THEMING_EDXMAKO_BACKEND = 'eox_theming.edxapp_wrapper.backends.l_mako'

Then you need to change the configuration in ``eox_theming/settings/common.py`` to use the previous ones.

🚨 If the release you are looking for is not listed, please note:

- If the Open edX release is compatible with the current eox-theming version (see `Compatibility Notes <https://github.com/eduNEXT/eox-theming?tab=readme-ov-file#compatibility-notes>`_), the default configuration is sufficient.
- If incompatible, you can refer to the README from the relevant version tag for configuration details (e.g., `v2.0.0 README <https://github.com/eduNEXT/eox-theming/blob/v2.0.0/README.md>`_).


************
Installation
************

Pre-requirements
----------------

- Ensure you have a theme or themes following the `Changing Themes guide <https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/configuration/changing_appearance/theming/index.html>`_ and compile them so they are accessible for the platform

**NOTE**

In order to simplify this process, we encourage the use of ``Distro Tutor Plugin`` for managing the addition and compilation of custom themes: `README of Distro <https://github.com/eduNEXT/tutor-contrib-edunext-distro?tab=readme-ov-file#themes>`_

Using Tutor
-----------

#. Install the plugin adding it to ``OPENEDX_EXTRA_PIP_REQUIREMENTS`` in the ``config.yml``.
   
   .. code-block:: yaml
      
      OPENEDX_EXTRA_PIP_REQUIREMENTS:
         - eox-theming=={{version}}

#. Save the configuration with ``tutor config save``
#. Launch the platform with ``tutor [local | dev] launch``

*****
Usage
*****

Settings
--------

Next,  with ``eox-tenant`` create a new ``route`` or modify an existing one to point to a ``tenant config`` that lists your theme names in hierarchical order.  This hierarchy, which follows the priority for template lookup, uses the attributes ``name``, ``parent``, and ``grandparent`` respectively. Your ``tenant config`` JSON will need a property similar to the following one:

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

If you chose to use ``Distro Tutor Plugin``, just follow the instructions given in the `Themes section <https://github.com/eduNEXT/tutor-contrib-edunext-distro/blob/master/README.md#themes>`_. Otherwise, if you are doing the process manually, follow this steps:

#. Add the following settings to your environment file ``env/apps/openedx/settings/lms/[development | production].py``:

   .. code:: python
   
       COMPREHENSIVE_THEME_DIRS.extend(
           [
               "/path-to-your-theme/in-the-lms-container/my-theme-1/edx-platform",
               "/path-to-your-theme/in-the-lms-container/my-theme-2/edx-platform",
               "/path-to-your-theme/in-the-lms-container/my-theme-3/edx-platform"
           ]
       )
       EOX_THEMING_DEFAULT_THEME_NAME = "my-theme-1" # Or the theme you want
   
       ################## EOX_THEMING ##################
       if "EOX_THEMING_DEFAULT_THEME_NAME" in locals() and EOX_THEMING_DEFAULT_THEME_NAME:
           from lms.envs.common import _make_mako_template_dirs  # pylint: disable=import-error
           ENABLE_COMPREHENSIVE_THEMING = True
           TEMPLATES[1]["DIRS"] = _make_mako_template_dirs
           derive_settings("lms.envs.[devstack | production]")  # lms.envs.devstack or lms.envs.production

#. Compile the before added themes according to you are using a `production environment <https://github.com/eduNEXT/tutor-contrib-edunext-distro/blob/a63e585b9bc3089e00623974c8b365ea874f0a2b/README.md?plain=1#L219>`_ or a `dev environment <https://github.com/eduNEXT/tutor-contrib-edunext-distro/blob/a63e585b9bc3089e00623974c8b365ea874f0a2b/README.md?plain=1#L234>`_


#. Ensure is included the following configuration in `devstack.py` in `eox-theming`:

   .. code-block:: python
    
       """
       Production Django settings for eox_theming project.s
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

**NOTE** 

In ``COMPREHENSIVE_THEME_DIRS`` it must contain a list of directories where the folders of the themes to be tested are located.

************
Contributing
************

Contributions are welcome! See our `CONTRIBUTING`_
file for more information - it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/eox-theming/blob/master/CONTRIBUTING.rst
