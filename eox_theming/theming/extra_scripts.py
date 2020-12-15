"""
This function gets called during every request by the
context processor to return all the custom scripts for a specific path.
"""
import logging
import re

import six

from eox_theming.configuration import ThemingConfiguration

logger = logging.getLogger(__name__)

common_attributes = {'type': {'options': ['inline', 'external']},
                     'media_type': {'options': ['module', 'text/javascript'], 'default': 1}}


def validate_script_attributes(values):
    """
    Validate common attributes for external and inline scripts.
    """
    script_attributes = {}

    # Validate common attributes for external and inline scripts
    for key, attr_values in common_attributes.items():

        value = values.get(key)

        try:
            if value is not None:
                attr_values['options'].index(value.lower())

                script_attributes[key] = value.lower()
            else:
                default = attr_values['default']

                script_attributes[key] = attr_values['options'][default]

        except Exception:  # pylint: disable=broad-except
            logger.error("Script could not get loaded. '%s' attribute is missing or is an invalid option.", key)

            return None

    # Validate according to the script type
    attr = 'src'
    if script_attributes['type'] == 'inline':
        attr = 'content'

    script_attributes = check_attribute(values, script_attributes, attr)

    return script_attributes


def check_attribute(values, script_attributes, attribute):
    """
    Validate the existence of an specific attribute.
    """
    try:
        script_attributes[attribute] = values[attribute]
    except Exception:  # pylint: disable=broad-except
        logger.error("Script could not get loaded. '%s' attribute is missing.", attribute)

        return None

    return script_attributes


def process_scripts(path):
    """
    Process and loads all the extra scripts for the template
    rendered during the request.
    """
    scripts = ThemingConfiguration.options('scripts', default={})

    for regex, values in six.iteritems(scripts):

        regex_path_match = re.compile(regex)

        if regex_path_match.match(path):

            scripts = []

            for script in values:

                validated_script = validate_script_attributes(script)

                if validated_script:

                    scripts.append(validated_script)

            if scripts:
                return scripts

    return None
