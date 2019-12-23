""" Backend abstraction for edxmako used in tests. """


def get_mako_loader():
    """ Get MakoLoader. """
    return object


def get_dynamictemplate_lookup():
    """ Abstraction for tests. """
    return object


def get_top_level_template_uri():
    """ Abstraction for tests. """
    return object


def get_lookup():
    """ Abstraction for tests. """
    return {}


def get_clear_lookups():
    """ Abstraction for tests. """
    def mock_function():
        """function for the tests"""
        return
    return mock_function
