"""
Utils definitions
"""
import six


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
        elif (k in dct and isinstance(dct[k], list)
                and isinstance(merge_dct[k], list)):
            dct[k].append(merge_dct[k])
        else:
            dct[k] = merge_dct[k]
    return dct
