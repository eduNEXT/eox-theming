"""
Static file finders for Django.

This is the original note from the edx-platform code:
https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-STATICFILES_FINDERS
Yes, this interface is private and undocumented, but we need to access it anyway.

In order to deploy Open edX in production, it's important to be able to collect
and process static assets: images, CSS, JS, fonts, etc. Django's collectstatic
system is the accepted way to do that in Django-based projects, but that system
doesn't handle every kind of collection and processing that web developers need.
Other open source projects like `Django-Pipeline`_ and `Django-Require`_ hook
into Django's collectstatic system to provide features like minification,
compression, Sass pre-processing, and require.js optimization for assets before
they are pushed to production. To make sure that themed assets are collected
and served by the system (in addition to core assets), we need to extend this
interface, as well.

.. _Django-Pipeline: https://django-pipeline.readthedocs.org/
.. _Django-Require: https://github.com/etianen/django-require
"""
from eox_theming.edxapp_wrapper.finders import get_openedx_theme_finder

OpenedxThemeFinder = get_openedx_theme_finder()


class EoxThemeFilesFinder(OpenedxThemeFinder):
    """
    The eox theme files finder is the intervention point to make sure
    that we are loading all the themes statics assets into the platform.

    See: openedx/core/djangoapps/theming/finders.py
    """
    pass
