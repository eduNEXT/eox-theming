"""
Template tags and helper functions for displaying breadcrumbs in page titles
based on the current micro site.
"""
from ast import literal_eval
from django import template

from ..configuration import ThemingConfiguration

register = template.Library()  # pylint: disable=invalid-name


class ThemingOptionsNode(template.Node):
    def __init__(self, args, default):
        self.options_args = args
        self.options_default = default

    def render(self, context):
        return ThemingConfiguration.options(*self.options_args, default=self.options_default)


@register.tag(name="theming_options")
def do_options_call(parser, token, *args, **kwargs):

    contents = token.split_contents()
    tag_name = contents[0]
    args = contents[1:]

    parsed_args = []
    default = None

    for x in args:
        try:
            val = literal_eval(x)
        except Exception as e:
            val = x

        if val.startswith('default='):
            default = val[8:]
        else:
            parsed_args.append(x)

    return ThemingOptionsNode(parsed_args, default=default)
