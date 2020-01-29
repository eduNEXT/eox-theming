Theming API V1 development
-----------------------------

Status
======

Accepted

Context
=======

We are implementing a new set of Theming tools that offers flexibility and high level of customization for new OpenedX
themes creation process. We are trying to cover features the current comprehensive theming does not support by
exposing a robust API that, based on a self-explained theme configuration, can preview and deploy new themes with much
less effort.

Decisions
=========

#. **API development**

   a. Render method of html_block theme element does not support html sanitizing. Right now it is rendering its content
      as it comes from the theme configuration
   b. Theming configuration can have a default living in the theme. These defaults are merged recursively with the
      configuration obtained from the main source (local file, tenant configuration, etc). In this way the main
      configuration can override sections of the default configuration

      **Example**

      If defaults are:
      ::
         {
            "THEME_OPTIONS": {
               "variables": {
                  "var1": "val1",
                  "var2": "val2"
               },
               "navigation": {
                  "id": "navbar-id",
                  "class": "navbar-class"
               },
               "footer": {
                  "id": "footer-id",
                  "class": "footer-class",
                  "particles": [
                     {
                        "id": "my_footext",
                        "type": "text",
                        "class": "footer-text",
                        "variables": {
                           "text": "This is the text for the footer"
                        }
                     }
                  ]
               }
            }
         }

      and main configuration is:
      ::
         {
            "THEME_OPTIONS": {
               "variables": {
                  "var2": "val2_new",
                  "var3": "val3"
               },
               "footer": {
                  "class": "footer-new-class",
                  "particles": [
                     {
                        "id": "openedx_logo",
                        "type": "image_tag",
                        "variables": {
                           "source": "https://files.edx.org/openedx-logos/edx-openedx-logo-tag.png",
                           "alt": " Powered by Open edX",
                           "destination_url": ""
                        }
                     }
                  ]
               }
            }
         }

      the merged configuration is:
      ::
         {
            "THEME_OPTIONS": {
               "variables": {
                  "var1": "val1",
                  "var2": "val2_new",
                  "var3": "val3"
               },
               "navigation": {
                  "id": "navbar-id",
                  "class": "navbar-class"
               },
               "footer": {
                  "id": "footer-id",
                  "class": "footer-new-class",
                  "particles": [
                     {
                        "id": "openedx_logo",
                        "type": "image_tag",
                        "variables": {
                           "source": "https://files.edx.org/openedx-logos/edx-openedx-logo-tag.png",
                           "alt": " Powered by Open edX",
                           "destination_url": ""
                        }
                     }
                  ]
               }
            }
         }

      The location of the theme defaults json file must be **<theme_name>/lms/default_exploded.json**.
