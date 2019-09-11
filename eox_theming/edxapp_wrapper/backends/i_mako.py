""" Backend abstraction for edxmako. """

from edxmako.makoloader import MakoLoader  # pylint: disable=import-error


def get_mako_loader():
    """ Get MakoLoader. """
    return MakoLoader
