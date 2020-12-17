===============
Extra scripts
===============

This feature allows the addition of multiple scripts (JavaScript) in any template.

For instance if you want to have specific scripts to be rendered to the login page, add the path (regular expression) and the list of scripts to the settings in THEME_OPTIONS::

    "THEME_OPTIONS": { "scripts": 
                        { 
                            "/login": [ 
                                { 
                                    "type": "external",
                                    "media_type": "text/javascript",
                                    "src": "https://www.test.com/js/myScript1.js" 
                                }, 

                                { 
                                    "type": "inline",
                                    "content": "alert('This is a test for the inline script');"
                                }
                            ]
                        }
                        ... 
                    
                    }

Attributes
------------------

The attributes that can be specified for each script are:

(1) **type**: to indicate whether is an *'external'* or *'inline'* script. This value is required.
(2) **media_type**: whose options are *'module'* or *'text/javascript'*. This attribute has 'text/javascript' as its default value.
(3) In case the script type is *'external'*, then is necessary to add the **src** attribute. If on the contrary, the script type is *'inline'*, then the **content** attribute with the script content is required.

In case one of the attributes is missing (if the attribute is required) or is a invalid option, an error gets logged and the failing script will not be rendered, however all the other valid scripts will. 
Here is an example of a logged error::
    
    2020-12-16 15:20:37,113 ERROR 2821 [eox_theming.theming.extra_scripts] [user None] extra_scripts.py:40 - Script could not get loaded. 'type' attribute is missing or is an invalid option.