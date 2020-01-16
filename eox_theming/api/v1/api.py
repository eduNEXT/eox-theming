"""
Theming API exposing methods required on frontend
"""
from importlib import import_module
import os
import logging
import operator
from copy import deepcopy

# forward compatibility for Python 3
from functools import reduce  # pylint: disable=redefined-builtin

from django.conf import settings
from django.template.loader import render_to_string
from django.template.exceptions import TemplateDoesNotExist

from eox_theming.utils import dict_merge, load_json_from_file
from eox_theming.edxapp_wrapper.theming_helpers import get_theming_helpers

LOG = logging.getLogger(__name__)

LOCAL_JSON_OBJECT_FILENAME = 'object_exploded.json'
LOCAL_JSON_MODULE_LOCATION = 'eox_theming.api'
DEFAULT_TEMPLATE_ENGINE_NAME = 'mako'
DEFAULT_PARTICLES_TEMPLATES_FOLDER = 'particles'


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


def from_local_file():
    """
    Load the theming configurations from a local file
    """
    location = getattr(settings, 'EOX_THEMING_JSON_THEME_CONFIG_PATH', None)

    if not location:
        # the current local object lives under eox_theming.api module
        local_json_module_location = import_module(LOCAL_JSON_MODULE_LOCATION)
        base_dir = os.path.dirname(local_json_module_location.__file__)
        location = os.path.join(base_dir, LOCAL_JSON_OBJECT_FILENAME)

    configuration = load_json_from_file(location)

    # TODO: is the object going to live under THEME_OPTIONS key??
    return configuration.get('THEME_OPTIONS', {})


class ThemingOptions(object):
    """
    This class must handle all the calls to the diferential settings a theme will be allowed to use
    """
    # TODO: This value source_functions must come from a django setting
    source_functions = [from_local_file]
    _config = None
    theming_helpers = get_theming_helpers()

    def __init__(self):
        """
        Initialize the ThemingOptions object by loading the theme configuration
        """
        self._load_configuration()

    def options(self, *args, **kwargs):
        """Main method for accessing the current configuration for the theme"""
        value = None

        try:
            value = reduce(operator.getitem, args, self._config)
        except (AttributeError, KeyError):
            LOG.debug("Found nothing when reading the theme options for %s", ".".join(args))
            value = None

        if value is None:
            value = kwargs.pop('default', None)

        return value

    def _load_configuration(self):
        """
        Load the configuration theme values on the instance
        """
        for source in self.source_functions:
            try:
                config = source()
                if config:
                    break
            except Exception as exc:  # pylint: disable=broad-except
                LOG.warning('Unable to read Theme Options from source %s. Trace: %s',
                            source.__name__, exc)
                continue

        if not config:
            config = {}

        # Getting theme defaults
        default_config = self._get_default_configuration()
        # Updating default configs with current config
        config = dict_merge(default_config, config)
        self._config = config

    def _get_default_configuration(self):
        """
        obtain a set of configurations defined in the current theme
        """
        # For now the default is taken from current theme in theme_name/lms/default_exploded.json
        return self._defaults_from_current_theme()

    def _defaults_from_current_theme(self):
        """
        Get defaults from current theme
        """
        filename = 'default_exploded.json'
        current_theme = self.theming_helpers.get_current_theme()
        if not current_theme:
            return {}

        default_file_loc = current_theme.path / filename
        default_config = load_json_from_file(default_file_loc)
        return default_config.get('THEME_OPTIONS', {})

    def get_segment(self, segment_name):
        """
        Get a high level element of an html page
        """
        segment_obj = self.options(segment_name)
        if not segment_obj:
            return None

        return Particle(**segment_obj)


class Particle(object):
    """
    Basic definition of a particle
    """
    _config = None
    default_config = {}
    template_name = None  # Should this one be included in the configuration?
    parent = None  # Determine if the Particle will have a parent
    _loaded_children = None

    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Initiating a new Particle
        TODO: Maybe a Particle should be initialized with a global context (global vars?)
        TODO: could a template path be a configuration variable for a particle
        """
        default_config = self._get_default_configuration()
        self._config = dict_merge(default_config, kwargs)

    def _get_default_configuration(self):
        """
        Get the default configuration for the particle
        """
        return deepcopy(self.default_config)

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

    def render(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        render the particle
        TODO: It could be desirable to support input arguments, for now they're unused
        """
        context = self.get_context_render()
        raw_result = ''
        template_names = []

        if self.template_name:
            template_names.append(self.template_name)

        template_by_type = self.get_template_name_by_type()
        if template_by_type:
            template_names.append(template_by_type)

        try:
            if template_names:
                raw_result = Renderer.render_to_string(template_names, context)
        except TemplateDoesNotExist:
            LOG.debug("Templates %s not found for particle", ",".join(template_names))
            raw_result = ''

        if not raw_result:
            if self.children:
                raw_result = self.render_children()
            else:
                raw_result = Renderer.render_to_string(
                    '{}/particle.html'.format(DEFAULT_PARTICLES_TEMPLATES_FOLDER),
                    context
                )

        return self.post_render(raw_result)

    def post_render(self, raw_output):
        """
        Apply some processing to a given raw output
        """
        # TODO: for now this method just return the raw output
        return raw_output

    def render_children(self):
        """
        Render and concatenate every children particle
        """
        result = ''
        for sub_part in self.children:
            partial = sub_part.render()
            result += partial

        return result

    def get_template_name_by_type(self, extension=None):
        """
        return a template name based on the type of the particle
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
        get the context to render a particle
        """
        context = {
            'particle': self
        }
        return context

    @property
    def template(self):
        """
        return the template defined for the particle
        """
        return self.template_name

    @property
    def children(self):
        """
        Get the particle children, if they exist
        """
        if self._loaded_children is not None:
            return self._loaded_children

        # TODO: This is an ugly line to get children from different locations
        children = self.options('particles') or self.options('variables', 'particles')
        if not children:
            return []

        children_particles = []
        for el in children:
            new_particle = ParticleFactory.create(**el)
            children_particles.append(new_particle)

        self._loaded_children = children_particles
        return children_particles


class ParticleFactory(object):
    """
    Particle factory to allow parent particles to instantiate their children
    """
    localizer = {
        "default": Particle
    }

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Create a new particle
        """
        particle_type = kwargs.get('type')
        creator_class = cls.localizer.get(particle_type)
        if creator_class is None:
            creator_class = cls.localizer.get('default')

        return creator_class(*args, **kwargs)
