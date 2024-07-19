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

Eox theming is a plugin for `Open edX <https://github.com/openedx/edx-platform>`_, and part of the Edunext Open Extensiones (aka EOX) that provides a stable place from where to create and launch themes to the Open edX platform.

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

* From Lilac version Django 2.2 is not supported, you should use Django 3.2 and eox-tenant >=4.0.

************
Installation
************

Pre-requirements
----------------

- A compatible version of `eox-tenant <https://github.com/eduNEXT/eox-tenant>`_
- Ensure you have a theme or themes following the `Changing Themes guide <https://edx.readthedocs.io/projects/edx-installing-configuring-and-running/en/latest/configuration/changing_appearance/theming/index.html>`_ and compile them so they are accessible for the platform

.. note::

    In order to simplify this process, we encourage the use of ``Distro Tutor Plugin`` for managing the addition and compilation of custom themes: `README of Distro <https://github.com/eduNEXT/tutor-contrib-edunext-distro?tab=readme-ov-file#themes>`_

Using Open edX devstack
-----------------------

#. Clone this repo in the ``src`` folder of your devstack.
#. Open a new ``lms/devstack`` shell.
#. Install the plugin as follows: ``pip install -e /path/to/your/src/folder``
#. Restart lms/cms services.

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

Next,  with ``eox-tenant`` create a new ``route`` or modify an existing one to point to a ``tenant config`` that lists your theme names in hierarchical order.  This hierarchy, which follows the priority for template lookup, uses the attributes ``name``, ``parent``, and ``grandparent`` respectively. You ``tenant config`` JSON will need a property similar to the following one:

.. code-block:: json

    {
        "EDNX_USE_SIGNAL": true,
        "THEME_OPTIONS": {
            "theme": {
                "name":"my-theme-1",
                "parent":"my-theme-2"
                "grandparent":"my-theme-3",
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


#. Ensure is included the follow configuration in `devstack.py` in `eox-theming`:

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

        # If you are using devstack, ensure this file contains the following
        from lms.envs.common import _make_mako_template_dirs # pylint: disable=import-error
        settings.ENABLE_COMPREHENSIVE_THEMING = True
        settings.COMPREHENSIVE_THEME_DIRS = [
            '/edx/src/themes/ednx-test-themes/edx-platform/',
        ]
        settings.TEMPLATES[1]["DIRS"] = _make_mako_template_dirs
        settings.derive_settings("lms.envs.devstack")

.. note::
    
    Note that in ``COMPREHENSIVE_THEME_DIRS`` it must contain a list of directories where the folders of the themes to be tested are located.

Contributing
------------

Contributions are welcome! See our `CONTRIBUTING`_
file for more information - it also contains guidelines for how to maintain high code
quality, which will make your contribution more likely to be accepted.

.. _CONTRIBUTING: https://github.com/eduNEXT/eox-theming/blob/master/CONTRIBUTING.rst
