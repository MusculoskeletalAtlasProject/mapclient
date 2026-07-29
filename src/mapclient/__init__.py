# setuptools stopped supporting pkg_resources,
# but we cannot know if every plugin has removed
# this old import device. So, we will create a shim
# if it is no longer available and protect against
# plugins still using it.
import types

mock_pkg_resources = False
try:
    import pkg_resources

    if not hasattr(pkg_resources, 'declare_namespace'):
        mock_pkg_resources = True
except ModuleNotFoundError:
    mock_pkg_resources = True

if mock_pkg_resources:
    def declare_namespace(name):
        pass


    pkg_resources = types.ModuleType('pkg_resources')
    pkg_resources.declare_namespace = declare_namespace
    sys.modules['pkg_resources'] = pkg_resources

from .settings.version import __version__

version = __version__
