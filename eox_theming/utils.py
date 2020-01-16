"""
Utils definitions
"""
import os
import logging
import six
import commentjson

LOG = logging.getLogger(__name__)


def dict_merge(dct, merge_dct):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: modified dict dct

    Inspired on https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
    """
    for k, _ in six.iteritems(merge_dct):
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], dict)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
    return dct


def load_json_from_file(location):
    """
    load a json from a file location
    """
    configuration = {}
    if not os.path.exists(location):
        return configuration

    with open(location, 'r') as f:
        try:
            configuration = commentjson.load(f)
        except Exception as exc:  # pylint: disable=broad-except
            LOG.warning('Found an error reading json object from location %s. Trace: %s',
                        location, exc)

    return configuration
