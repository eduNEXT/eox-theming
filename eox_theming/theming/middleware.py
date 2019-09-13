"""
Plugin middlewares
"""
from eox_theming.edxapp_wrapper.models import get_openedx_site_theme_model
from eox_theming.configuration import ThemingConfiguration

SITE_THEME = get_openedx_site_theme_model()


class EoxThemeMiddleware(object):
    """
    This Middleware class is required to load a site_theme into the current request.

    We use the site_theme from the core platform still because it behaves well with
    the current implementation of comprehensive themes. It might not be hard requirement later.
    """

    def process_request(self, request):
        """
        Set the request's 'site_theme'
        """
        # TODO: resolve. If the site does not exist, should we create it? or use a placeholder site_id

        theme_name = ThemingConfiguration.get_theme_name()

        if theme_name:
            current_theme, _ = SITE_THEME.objects.get_or_create(
                site_id=1,
                theme_dir_name=theme_name,
            )
            request.site_theme = current_theme
