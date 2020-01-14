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
import commentjson

from django.conf import settings

from eox_theming.utils import dict_merge

LOG = logging.getLogger(__name__)

LOCAL_JSON_OBJECT_FILENAME = 'object_exploded.json'
LOCAL_JSON_MODULE_LOCATION = 'eox_theming.api'


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

    configuration = {}

    if not os.path.exists(location):
        return configuration

    with open(location, 'r') as f:
        try:
            configuration = commentjson.load(f)
        except Exception as exc:  # pylint: disable=broad-except
            LOG.warning('Found an error reading json theme object from location %s. Trace: %s',
                        location, exc)

    options_dict = configuration.get('THEME_OPTIONS', {})
    return options_dict


class ThemingOptions(object):
    """
    This class must handle all the calls to the diferential settings a theme will be allowed to use
    """
    # TODO: This value source_functions must come from a django setting
    source_functions = [from_local_file]
    _config = None

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
        config = dict_merge(deepcopy(default_config), config)
        self._config = config

    def _get_default_configuration(self):
        """
        obtain a set of configurations defined in the current theme
        """
        # TODO: define the logic to get the defaults from the right location
        return {}


class Particle(object):
    """
    Basic definition of a particle
    """
    context = None
    config = None
    default_config = {}
    template_name = None  # Should this one be included in the configuration?
    parent = None  # Determine if the Particle will have a parent
    _loaded_children = None

    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Initiating a new Particle
        """
        self.context = kwargs.pop('context', {})  # This is the parameter to pass globlal context like globals variables
        default_config = self._get_default_configuration()
        self.config = dict_merge(default_config, kwargs)

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
        except (AttributeError, KeyError):
            LOG.debug("Found nothing when reading the theme options for %s", ".".join(args))
            value = None

        if value is None:
            value = kwargs.pop('default', None)

        return value

    def render(self):
        """
        render the particle
        """

    def get_context_render(self):
        """
        get the context to render a particle
        """
        context = {
            'config': self.config,
            'children': self.children
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

        children = self.options('objects')
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
