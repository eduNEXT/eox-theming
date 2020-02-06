"""
Django template system engine for Mako templates.
"""
from __future__ import absolute_import, unicode_literals

import logging
from six import text_type

from mako.exceptions import (
    MakoException,
    text_error_template,
    TemplateLookupException,
    CompileException
)
from mako.template import Template as MakoTemplate

from django.utils.module_loading import import_string
from django.conf import settings
from django.template import Context, RequestContext, TemplateDoesNotExist, TemplateSyntaxError
from django.template.backends.base import BaseEngine

LOGGER = logging.getLogger(__name__)
KEY_CSRF_TOKENS = ('csrf_token', 'csrf')


def get_template_request_context(request=None):
    """
    Returns the template processing context to use for the current request,
    or returns None if there is not a current request.
    """
    if request is None:
        return None

    context = RequestContext(request)
    context['is_secure'] = request.is_secure()

    return context


class MakoEngine(object):
    """
    This is the engine that handles getting the template and
    compiling the template the code.
    """
    def __init__(self, **options):
        """
        :param options: The template options that are passed to the
        template lookup class.
        """
        environment = options.pop(
            'environment', 'mako.lookup.TemplateLookup')
        # Just to get a dotted module path as an/a attribute/class
        Environment = import_string(environment)
        self.context_processors = options.pop('context_processors', [])
        self.lookup = Environment(**options)

    def from_string(self, template_code):
        """
        Compiles the template code and return the compiled version.

        :param template_code: Textual template source.
        :return: Returns a compiled Mako template.
        """
        return MakoTemplate(template_code, lookup=self.lookup)

    def get_template(self, name):
        """
        Locates template source files from the local filesystem given
        a template name.
        :param name: The template name.
        :return: the located template.
        """
        return self.lookup.get_template(name)


class Mako(BaseEngine):
    """
    A Mako template engine to be added to the ``TEMPLATES`` Django setting.
    """
    app_dirname = 'templates'

    def __init__(self, params):
        """
        Fetches template options, initializing BaseEngine properties,
        and assigning our Mako default settings.
        Note that OPTIONS contains backend-specific settings.
        :param params: This is simply the template dict you
                       define in your settings file.
        """
        params = params.copy()
        options = params.pop('OPTIONS').copy()
        super(Mako, self).__init__(params)
        # A list of directory names which will be searched for a
        # particular template URI
        options.setdefault('directories', self.template_dirs)
        self.engine = MakoEngine(**options)

    def from_string(self, template_code):
        """
        Trying to compile and return the compiled template code.

        :raises: TemplateSyntaxError if there's a syntax error in
        the template.
        :param template_code: Textual template source.
        :return: Returns a compiled Mako template.
        """
        try:
            return Template(self.engine.from_string(template_code), self)
        except MakoException:
            message = text_error_template().render()
            raise TemplateSyntaxError(message)

    def get_template(self, template_name):
        """
        Loads and returns a template for the given name.
        """
        try:
            return Template(self.engine.get_template(template_name), self)
        except TemplateLookupException:
            raise TemplateDoesNotExist(template_name)
        except CompileException:
            raise TemplateSyntaxError(template_name)


class Template(object):
    """
    This bridges the gap between a Mako template and a Django template. It can
    be rendered like it is a Django template because the arguments are transformed
    in a way that MakoTemplate can understand.
    """

    def __init__(self, template, backend):
        """
        Overrides base __init__ to provide django variable overrides
        """
        self.mako_template = template
        self.backend = backend

    def render(self, context=None, request=None):
        """
        This takes a render call with a context (from Django) and translates
        it to a render call on the mako template.
        """
        context_object = self._get_context_object(request)
        context_dictionary = self._get_context_processors_output_dict(context_object)

        if isinstance(context, Context):
            context_dictionary.update(context.flatten())
        elif context is not None:
            context_dictionary.update(context)

        self._add_core_context(context_dictionary)
        self._evaluate_lazy_csrf_tokens(context_dictionary)

        return self.mako_template.render_unicode(**context_dictionary)

    @staticmethod
    def _get_context_object(request):
        """
        Get a Django RequestContext or Context, as appropriate for the situation.
        In some tests, there might not be a current request.
        """
        request_context = get_template_request_context(request)
        if request_context is not None:
            return request_context
        else:
            return Context({})

    def _get_context_processors_output_dict(self, context_object):
        """
        Run the context processors for the given context and get the output as a new dictionary.
        """
        with context_object.bind_template(self):
            return context_object.flatten()

    @staticmethod
    def _add_core_context(context_dictionary):
        """
        Add to the given dictionary context variables which should always be
        present, even when context processors aren't run during tests.  Using
        a context processor should almost always be preferred to adding more
        variables here.
        """
        context_dictionary['settings'] = settings
        context_dictionary['EDX_ROOT_URL'] = getattr(settings, 'EDX_ROOT_URL', '')

    @staticmethod
    def _evaluate_lazy_csrf_tokens(context_dictionary):
        """
        Evaluate any lazily-evaluated CSRF tokens in the given context.
        """
        for key in KEY_CSRF_TOKENS:
            if key in context_dictionary:
                context_dictionary[key] = text_type(context_dictionary[key])
