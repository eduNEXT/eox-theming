"""
"""

from eox_theming.edxapp_wrapper.models import get_openedx_site_theme_model

SITE_THEME = get_openedx_site_theme_model()


class EoxThemeMiddleware(object):
    """
    """

    def process_request(self, request):
        """
        Set the request's 'site_theme'
        """
        # TODO: resolve. If the site does not exist, should we create it? or use a placeholder site_id
        current_theme, _ = SITE_THEME.objects.get_or_create(site_id=1, theme_dir_name='bragi')
        request.site_theme = current_theme
