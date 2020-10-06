"""Backend abstraction for edxmako. """

from edxmako import LOOKUP, clear_lookups  # pylint: disable=import-error
from edxmako.makoloader import MakoLoader  # pylint: disable=import-error
from edxmako.paths import DynamicTemplateLookup, TopLevelTemplateURI  # pylint: disable=import-error


def get_mako_loader():
    """ Get MakoLoader. """
    return MakoLoader


def get_dynamictemplate_lookup():
    """ Get DynamicTemplateLookup. """
    return DynamicTemplateLookup


def get_top_level_template_uri():
    """ Get TopLevelTemplateURI"""
    return TopLevelTemplateURI


def get_lookup():
    """ Get edxmako LOOKUP dict"""
    return LOOKUP


def get_clear_lookups():
    """ Get clear_lookups function """
    return clear_lookups
