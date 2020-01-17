""" Renderers defintion """
from django.template.loader import render_to_string

DEFAULT_TEMPLATE_ENGINE_NAME = 'mako'


class Renderer(object):
    """
    Class in charge to handle the render process for Theme segments and particles
    """
    @classmethod
    def render_to_string(cls, template_name, context, request=None):
        """
        render a template with a given context
        """
        engine_name = cls.get_template_engine_name()
        return render_to_string(template_name, context, request, using=engine_name)

    @classmethod
    def get_template_engine_name(cls):
        """
        return a template engine name to use in a render process
        """
        # Only MAKO engine is supported. A more complex logic can be added here to decide
        # which engine to use
        return DEFAULT_TEMPLATE_ENGINE_NAME
