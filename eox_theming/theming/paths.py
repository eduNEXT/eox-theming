"""
Set up lookup paths for mako templates.

See: common.djangoapps.edxmako.paths
"""

import os
import re

import pkg_resources
from django.conf import settings
from mako.exceptions import TopLevelLookupException

from eox_theming.configuration import ThemingConfiguration
from eox_theming.edxapp_wrapper.mako import (
    get_clear_lookups,
    get_dynamictemplate_lookup,
    get_lookup,
    get_top_level_template_uri,
)

DynamicTemplateLookup = get_dynamictemplate_lookup()
TopLevelTemplateURI = get_top_level_template_uri()
LOOKUP = get_lookup()
clear_lookups = get_clear_lookups()

import  logging
LOG = logging.getLogger(__name__)

class EoxDynamicTemplateLookup(DynamicTemplateLookup):
    """
    The eox theme EoxDynamicTemplateLookup is the intervention point to make sure
    that we are loading the templates from the request theme and the default site theme.

    See: common.djangoapps.edxmako.paths
    """
    def adjust_uri(self, uri, calling_uri):
        """
        This method was reimplemented to use eox-theming strip_site_theme_templates_path and
        get_template_path_with_theme instead of the equivalent functions used in the platform.
        """
        # Make requested uri relative to the calling uri.
        relative_uri = super().adjust_uri(uri, calling_uri)
        adjusted_uri = get_template_path_with_theme(strip_site_theme_templates_path(relative_uri))
        # Is the calling template (calling_uri) which is including or inheriting current template (uri)
        # located inside a theme?
        if calling_uri != strip_site_theme_templates_path(calling_uri):
            # Is the calling template trying to include/inherit itself?
            if calling_uri == adjusted_uri:
                return TopLevelTemplateURI(relative_uri)
        return adjusted_uri

    def get_template(self, uri):
        """
        Overridden method for using get_template_path_with_theme from eox-theming instead of the function used in
        the platform.
        """

        if isinstance(uri, TopLevelTemplateURI):
            LOG.error("URI IS INSTANCE OF TopLevelTemplateURI")
            template = self._get_toplevel_template(uri)
        else:
            try:
                # Try to find themed template, i.e. see if current theme overrides the template
                template = super().get_template(get_template_path_with_theme(uri))
            except TopLevelLookupException:
                LOG.error("SE EJECUTO LA EXCEPCION: TopLevelLookupException")
                template = self._get_toplevel_template(uri)
        
        LOG.error(f"GET_TEMPLATE: {type(template)}")
        return template

    def _get_toplevel_template(self, uri):
        """
        Lookup a default/toplevel template, ignoring current theme.
        """
        # Strip off the prefix path to request theme and parent theme and look in default template dirs.
        return super()._get_toplevel_template(strip_site_theme_templates_path(uri))


def add_lookup(namespace, directory, package=None, prepend=False):
    """
    The difference with the edxmako implementation is that this uses the EoxDynamicTemplateLookup
    instead of DynamicTemplateLookup.

    See: common.djangoapps.edxmako.paths

    """
    templates = LOOKUP.get(namespace)
    if not templates:
        LOOKUP[namespace] = templates = EoxDynamicTemplateLookup(
            module_directory=settings.MAKO_MODULE_DIR,
            output_encoding='utf-8',
            input_encoding='utf-8',
            default_filters=['decode.utf8'],
            encoding_errors='replace',
        )
    if package:
        directory = pkg_resources.resource_filename(package, directory)
    templates.add_directory(directory, prepend=prepend)


def get_template_path_with_theme(relative_path):
    """
    The change with respect of the edx-platform version is that in this case, the templates are
    not searched only on the current site theme. They are also searched in the parent(default) theme.

    See: openedx.core.djangoapps.theming.helpers

    Example:
        >> get_template_path_with_theme('header.html')
        '/red-theme/lms/templates/header.html'

    Parameters:
        relative_path (str): template's path relative to the templates directory e.g. 'footer.html'

    Returns:
        (str): template path in current site's theme
    """
    relative_path = os.path.normpath(relative_path)
    return relative_path


def strip_site_theme_templates_path(uri):
    """
    The change with respect of the edx-platform version is that in this case, are stripped the
    theme and parent theme from the uri

    See: openedx.core.djangoapps.theming.helpers

    Example:
        >> strip_site_theme_templates_path('/red-theme/lms/templates/header.html')
        'header.html'

    Arguments:
        uri (str): template path from which to remove site theme path. e.g. '/red-theme/lms/templates/header.html'

    Returns:
        (str): template path with site theme path removed.
    """

    return uri
