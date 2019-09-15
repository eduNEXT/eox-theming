"""
Theming Storage abstraction used in eox-theming
"""
import os

from django.contrib.staticfiles.storage import StaticFilesStorage

from pipeline.storage import NonPackagingMixin  # pylint: disable=import-error
from require.storage import OptimizedFilesMixin  # pylint: disable=import-error

from eox_theming.edxapp_wrapper.storage import (
    get_theme_storage, get_themecached_mixin,
    get_pipeline_forgiving_storage,
    get_themepipeline_mixin
)
from eox_theming.configuration import ThemingConfiguration


OpenedxThemeStorage = get_theme_storage()
ThemeCachedFilesMixin = get_themecached_mixin()
PipelineForgivingStorage = get_pipeline_forgiving_storage()
ThemePipelineMixin = get_themepipeline_mixin()


class EoxThemeStorage(OpenedxThemeStorage):
    """
    The eox theme storage class is the intervention point to make sure
    that we are loading all the themes statics assets into the platform.

    See: openedx/core/djangoapps/theming/storage.py
    """
    def url(self, name):
        """
        Returns url of the asset, themed url will be returned if the asset is themed otherwise default
        asset url will be returned.

        Args:
            name: name of the asset, e.g. 'images/logo.png'

        Returns:
            url of the asset, e.g. '/static/red-theme/images/logo.png' if current theme is red-theme and logo
            is provided by red-theme otherwise '/static/images/logo.png'
        """
        prefix = ''
        theme = ThemingConfiguration.theming_helpers.get_current_theme()
        default_theme = ThemingConfiguration.get_default_theme()

        # get theme prefix from site address if if asset is accessed via a url
        if theme:
            prefix = theme.theme_dir_name

        # get theme prefix from storage class, if asset is accessed during collectstatic run
        elif self.prefix:
            prefix = self.prefix

        # join theme prefix with asset name if theme is applied and themed asset exists
        if prefix and self.themed(name, prefix):
            return super(EoxThemeStorage, self).url(name)

        elif default_theme and self.themed(name, default_theme.theme_dir_name):
            name = os.path.join(default_theme.theme_dir_name, name)
        return super(EoxThemeStorage, self).url(name)



class AbsoluteUrlAssetsMixin(object):
    """
    Mixin that overrides the url method on storages
    """
    def url(self, name):
        """
        Return url of the asset.
        If the asset name is an absolute url, just return the asset name
        """
        if name.startswith("https://") or name.startswith("http://"):
            return name

        return super(AbsoluteUrlAssetsMixin, self).url(name)


class EoxProductionStorage(
        AbsoluteUrlAssetsMixin,
        PipelineForgivingStorage,
        OptimizedFilesMixin,
        ThemeCachedFilesMixin,
        EoxThemeStorage,
        StaticFilesStorage
):
    """
    This class combines Django's StaticFilesStorage class with several mixins
    that provide additional functionality. We use this version on production.
    """
    pass


class EoxDevelopmentStorage(
        AbsoluteUrlAssetsMixin,
        NonPackagingMixin,
        ThemePipelineMixin,
        EoxThemeStorage,
        StaticFilesStorage
):
    """
    This class combines Django's StaticFilesStorage class with several mixins
    that provide additional functionality. We use this version for development,
    so that we can skip packaging and optimization.
    """
    pass
