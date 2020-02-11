""" Particles definition"""
import logging
import operator

# Forward compatibility for Python 3
from functools import reduce  # pylint: disable=redefined-builtin
import six

from django.conf import settings

from eox_theming.utils import dict_merge
from eox_theming.api.v1.renderers import Renderer
from eox_theming.edxapp_wrapper.configuration_helpers import get_configuration_helper

configuration_helpers = get_configuration_helper()
LOG = logging.getLogger(__name__)

DEFAULT_PARTICLES_TEMPLATES_FOLDER = 'particles'


class ThemingFlexibleObject(object):
    """
    This class defines the basic functionality required from the frontend
    to render an html section based on a provided configuration.
    To define more complex Flexible Objects, inherit from this class and
    extend the functionality.
    An instance of this class is named 'particle' on the frontend side.
    """
    _config = None
    parent = None  # Determine if the Flexible Object will have a parent
    _loaded_children = None

    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Initiating a new Flexible Object
        TODO: Maybe a Flexible Object should be initialized with a global context (global vars?)
        TODO: could a template path be a configuration variable for a Flexible Object
        """
        default_config = self._get_default_configuration()
        self._config = dict_merge(default_config, kwargs)

    def _get_default_configuration(self):
        """
        Get the default configuration for the Flexible Object
        """
        return {}

    def options(self, *args, **kwargs):
        """Main method for accessing the current configuration for the theme"""
        value = None

        try:
            value = reduce(operator.getitem, args, self._config)
        except (AttributeError, KeyError, TypeError):
            LOG.debug("Found nothing when reading the theme options for %s", ".".join(args))
            value = None

        if value is None:
            value = kwargs.pop('default', None)

        return value

    def get_template_names_list(self):
        """
        Get a list of template names ordered by priority to render the Flexible Object
        """
        default_template_name = '{}/particle.html'.format(DEFAULT_PARTICLES_TEMPLATES_FOLDER)
        template_names = [
            self.template_name,
            self.get_template_name_by_type(),
            default_template_name
        ]

        return [tpl for tpl in template_names if tpl]

    def render(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Render the Flexible Object
        TODO: It could be desirable to support input arguments, for now they're unused
        """
        context = self.get_context_render()
        raw_result = ''

        template_names = self.get_template_names_list()
        # TODO: is this the best way to get the current site?
        current_site_name = configuration_helpers.get_value(
            'SITE_NAME',
            getattr(settings, 'SITE_NAME', '')
        )

        try:
            raw_result = Renderer.render_to_string(template_names, context)
        except Exception as e:  # pylint: disable=broad-except
            LOG.warning(
                "The error %s ocurred when rendering %s templates for particle with id [%s] in site [%s]",
                e, ",".join(template_names),
                self.options('id', default=''),
                current_site_name
            )
            raw_result = ''

        return self.post_render(raw_result)

    def post_render(self, raw_output):
        """
        Apply some processing to a given raw output
        """
        # TODO: for now this method just return the raw output
        return raw_output

    def render_children(self):
        """
        Render and concatenate every children contained in the
        Flexible Object
        """
        result = ''
        for sub_part in self.children:
            partial = sub_part.render()
            result += partial

        return result

    def get_template_name_by_type(self, extension=None):
        """
        return a template name based on the type of the Flexible Object
        """
        if extension is None:
            extension = 'html'
        particle_type = self.options('type')
        if not particle_type:
            return ''
        return '{}/{}.{}'.format(
            DEFAULT_PARTICLES_TEMPLATES_FOLDER,
            particle_type,
            extension
        )

    def get_context_render(self):
        """
        get the context to render a Flexible Object
        """
        context = {
            'particle': self
        }
        return context

    @property
    def template_name(self):
        """
        return the template name defined for the Flexible Object
        """
        return self.options('template_name')

    @property
    def children(self):
        """
        Get the Flexible Object children, if they exist
        """
        if self._loaded_children is not None:
            return self._loaded_children

        # TODO: This is an ugly line to get children from different locations
        children = self.options('particles') or self.options('variables', 'particles')
        if not children:
            return []

        children_particles = []
        for el in children:
            new_particle = ThemingFlexibleObjectFactory.create(**el)
            children_particles.append(new_particle)

        self._loaded_children = children_particles
        return children_particles

    def get_css(self):
        """
        return a string with all the CSS rules defined for the Flexible Object concatenated and
        ready to use in a "style" property of an html tag
        """
        string_css_rules = ''
        css_rules = self.options('css', default={})
        try:
            string_css_rules = ';'.join(
                ['{}: {}'.format(key, value) for key, value in six.iteritems(css_rules)]
            )
        # TODO: logging a warning here
        except (AttributeError, TypeError):
            string_css_rules = ''

        return string_css_rules


class NcolumnContent(ThemingFlexibleObject):
    """
    Class definition for Flexible Object with columns
    """
    @property
    def columns_number(self):
        """
        Return the number of columns of the NcolumnContent Flexible Object
        """
        columns_layout = self.options('variables', 'column_layout')
        if not columns_layout or not isinstance(columns_layout, list):
            return 1

        return len(columns_layout)

    def children_by_column(self, column_number):
        """
        Return an iterator that filter the children based on the passed
        column_number
        """
        def predicate(child):
            """
            Useful to filter children by column
            """
            return child.options('column', default=1) == column_number

        iter_column = six.moves.filter(predicate, self.children)
        return iter_column


class ThemingFlexibleObjectFactory(object):
    """
    Flexible Object factory
    """
    localizer = {
        "default": ThemingFlexibleObject,
        "2_column_content": NcolumnContent,
        "3_column_content": NcolumnContent
    }

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Create a new Flexible Object
        """
        particle_type = kwargs.get('type')
        creator_class = cls.localizer.get(particle_type)
        if creator_class is None:
            creator_class = cls.localizer.get('default')

        return creator_class(*args, **kwargs)
