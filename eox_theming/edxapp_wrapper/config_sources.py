"""
This module abstracts the source functions from the platform or plugins code
to prevent a dependency requirement while testing.

Some functions are so simple they do not require a backend.
"""
import logging
import operator

# forward compatibility for Python 3
from functools import reduce  # pylint: disable=redefined-builtin

from django.conf import settings

LOG = logging.getLogger(__name__)


def from_site_config(*args):  # pylint: disable=unused-argument
    """
    This source is compatible with the site_configurations from Open edX platform.
    """
    LOG.info("Not implemented: from_site_config")


def from_eox_tenant_config_theming(*args):  # pylint: disable=unused-argument
    """
    This source is the most modern way of reading the theme configuration.
    Fully dependant on an advanced use of eox-tenant.
    """
    LOG.info("Not implemented: from_eox_tenant_config_theming")


def from_eox_tenant_microsite_v0(*args):  # pylint: disable=unused-argument
    """
    This source must act as a compatibility layer with the ungrouped way of storing
    config variables from the first iteration of the bragi theme.
    """
    LOG.info("Not implemented: from_eox_tenant_microsite_v0 compatibility layer")


def from_eox_tenant_config_lms(*args):
    """
    Given that the eox_microsite version loads all the config variables into
    the django.conf.settings object, we can defer to the django_settings source.
    """
    return from_django_settings(*args)


def from_eox_tenant_microsite_v1(*args):
    """
    Given that the eox_microsite version loads all the config variables into
    the django.conf.settings object, we can defer to the django_settings source.
    """
    return from_django_settings(*args)


def from_django_settings(*args):
    """
    Takes a THEME_OPTIONS dictionary in the settings module as the source.
    """
    options_dict = getattr(settings, "THEME_OPTIONS", {})

    if args:
        try:
            value = reduce(operator.getitem, args, options_dict)
        except (AttributeError, KeyError):
            LOG.debug("Found nothing when reading the theme options for %s", ".".join(args))
            value = None
    return value
