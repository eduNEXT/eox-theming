"""
Template tags and helper functions for displaying breadcrumbs in page titles
based on the current micro site.
"""
from __future__ import absolute_import, unicode_literals

from ast import literal_eval

from django import template

from eox_theming.configuration import ThemingConfiguration

register = template.Library()  # pylint: disable=invalid-name


class ThemingOptionsNode(template.Node):
    """
    Django templates nodes to render the advanced tag.
    Acts as a wrapper to the ThemingConfiguration.options call.
    """
    def __init__(self, args, default):
        self.options_args = args
        self.options_default = default

    def render(self, context):
        return ThemingConfiguration.options(*self.options_args, default=self.options_default)


@register.tag(name="theming_options")
def do_options_call(parser, token):  # pylint: disable=unused-argument
    """
    Django templates tag definition.
    """
    contents = token.split_contents()
    args = contents[1:]

    parsed_args = []
    default = None

    for arg in args:
        try:
            val = literal_eval(arg)
        except (SyntaxError, ValueError):
            val = arg

        try:
            if val.startswith('default='):
                default = val[8:]
            else:
                parsed_args.append(arg)
        except AttributeError:
            parsed_args.append(arg)

    return ThemingOptionsNode(parsed_args, default=default)
