"""
Created on May 19, 2015

@author: hsorby
"""
import io
import json
import os
import sys
import logging
import subprocess
import pkg_resources
import pkgutil
import traceback
import shutil
import types
import importlib

from contextlib import redirect_stdout


from mapclient.core.utils import which, FileTypeObject, grep, is_frozen, determineStepName, determineStepClassName
from mapclient.settings.definitions import VIRTUAL_ENV_PATH, \
    PLUGINS_PACKAGE_NAME, PLUGINS_PTH
from mapclient.core.checks import getPipExecutable, getActivateScript

from setuptools import sandbox

from importlib import import_module

from mapclient.settings.general import get_virtualenv_site_packages_directory

logger = logging.getLogger(__name__)


def getVirtualEnvCandidates():
    """Return a list of strings which contains possible names
    of the virtualenv program for this environment.
    """
    if sys.version_info < (3, 0):
        virtualenv_candidates = [which('virtualenv'), which('virtualenv2')]
    else:
        virtualenv_candidates = [which('virtualenv'), which('virtualenv3')]

    return virtualenv_candidates


class PluginManager(object):

    def __init__(self):
        self._directories = []
        self._virtualenv_enabled = True
        self._virtualenv_dir = None
        self._virtualenv_setup_attempted = False
        self._reload_plugins = True
        self._load_default_plugins = True
        self._doNotShowPluginErrors = False
        self._plugin_database = PluginDatabase()
        self._ignoredPlugins = []
        self._unsuccessful_package_installations = {}
        self._resourceFiles = ['resources_rc']
        self._updaterSettings = {'syntax': True, 'indentation': True, 'location': True, 'resources': True}
        self._import_errors = []
        self._type_errors = []
        self._syntax_errors = []
        self._tab_errors = []
        self._plugin_error_directories = {}
        self._plugin_error_names = []

    def setVirtualEnvEnabled(self, state=True):
        self._virtualenv_enabled = state

    def setVirtualEnvDirectory(self, directory):
        self._virtualenv_dir = directory

    def getVirtualEnvDirectory(self):
        return self._virtualenv_dir

    def directories(self):
        return self._directories

    def setReloadPlugins(self, state=True):
        self._reload_plugins = state

    def reloadPlugins(self):
        return self._reload_plugins

    def checkPlugins(self, wf_location):
        # TODO: Re-think how this will work
        pass

    def checkDependencies(self, wf_location):
        # TODO: Re-think how this will work
        pass

    def list(self):
        if self._virtualenv_enabled:
            pip_exe = getPipExecutable(self._virtualenv_dir)

            install_list = subprocess.check_output([pip_exe, 'list'])
            install_list = install_list.decode('utf-8')
        else:
            install_list = []
            logger.info('VirtualEnv not enabled no list functionality available.')

        return install_list

    def setOptions(self, options):
        self._virtualenv_dir = options[VIRTUAL_ENV_PATH]

    def setDirectories(self, directories):
        """
        Set the list of directories to be searched for
        plugins.  Returns true if the directories listing
        was updated and false otherwise.
        """
        if self._directories != directories:
            self._directories = directories
            self._reload_plugins = True

    def virtualenvSetupAttempted(self):
        return self._virtualenv_setup_attempted

    def virtualEnvExists(self):
        pip_exe = getPipExecutable(self._virtualenv_dir)
        return pip_exe is not None and os.path.exists(pip_exe)

    def setupVirtualEnv(self):

        for candidate in getVirtualEnvCandidates():
            try:
                p = subprocess.Popen([candidate, '--clear', '--system-site-packages', self._virtualenv_dir],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                # p = subprocess.Popen([candidate, '--clear', '--system-site-packages', self._virtualenv_dir],
                #                       stdout=subprocess.PIPE,
                #                       stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()

                # Make a plugins directory with a namespace package file in it.  This is to avoid problems
                # with other packages using namespace packages in Python 3.
                site_packages_dir = get_virtualenv_site_packages_directory(self._virtualenv_dir)
                os.makedirs(os.path.join(site_packages_dir, PLUGINS_PACKAGE_NAME))
                with open(os.path.join(site_packages_dir, PLUGINS_PACKAGE_NAME, '__init__.py'), 'w') as f:
                    f.write("from pkgutil import extend_path\n__path__ = extend_path(__path__, __name__)\n")

                if os.name == 'nt' and os.path.isfile('VCRUNTIME140.dll'):
                    shutil.copy('VCRUNTIME140.dll', os.path.join(self._virtualenv_dir, 'Scripts'))

                if stdout:
                    logger.info(stdout.decode('utf-8'))
                if stderr:
                    logger.error(stderr.decode('utf-8'))
            except SyntaxError:
                pass
            except:
                pass

        if self.virtualEnvExists():
            logger.info('Virtual environment successfully setup')
            self._virtualenv_enabled = True
        else:
            logger.warning('Virtual environment setup unsuccessful')
        self._virtualenv_setup_attempted = True

        return self.virtualEnvExists()

    def loadDefaultPlugins(self):
        return self._load_default_plugins

    def getPluginDatabase(self):
        return self._plugin_database

    def setLoadDefaultPlugins(self, loadDefaultPlugins):
        """
        Set whether or not the default plugins should be loaded.
        Returns true if the default load plugin setting is changed
        and false otherwise.
        """
        if self._load_default_plugins != loadDefaultPlugins:
            self._load_default_plugins = loadDefaultPlugins
            self._reload_plugins = True

    def allDirectories(self):
        plugin_dirs = self._directories[:]
        if self._load_default_plugins:
            if is_frozen():
                inbuilt_plugin_dir = os.path.join(sys._MEIPASS, PLUGINS_PACKAGE_NAME)
            else:
                file_dir = os.path.dirname(os.path.abspath(__file__))
                inbuilt_plugin_dir = os.path.realpath(os.path.join(file_dir, '..', '..', '..', ))
            plugin_dirs.insert(0, inbuilt_plugin_dir)

        return plugin_dirs

    def _addPluginDir(self, directory):
        added = False
        if isMapClientPluginsDir(directory):
            if directory not in sys.path:
                sys.path.append(directory)
                added = True

        return added

    def installPackage(self, uri):
        logger.info('Installing package : %s.' % uri)
        my_env = os.environ.copy()

        if is_frozen():
            python_executable = os.path.join(sys._MEIPASS, "python.exe")
            my_env["PYTHONPATH"] = sys._MEIPASS
        else:
            python_executable = sys.executable

        if not is_frozen():
            subprocess.Popen([python_executable, "-m", "pip", "install", str(uri)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)

            importlib.reload(pkg_resources)

    def extractPluginDependencies(self, path):
        setup_dir, step_dir = os.path.split(path)
        setup_py_file = os.path.join(setup_dir, 'setup.py')
        if os.path.exists(setup_py_file):
            current_dir = os.getcwd()
            os.chdir(setup_dir)
            try:
                # Skip this for now and move to using packagemeta package instead.
                dependencies_str = '[]'
                # f = io.StringIO()
                # with redirect_stdout(f):
                #     sandbox.run_setup('setup.py', ['--install-requires'])
                # dependencies_str = f.getvalue().rstrip()
                # if "'" in dependencies_str:
                #     dependencies_str = dependencies_str.replace("'", '"')

                dependencies = json.loads(dependencies_str)
            finally:
                os.chdir(current_dir)

            return dependencies

        return []

    def load(self):
        self._reload_plugins = False

        len_package_modules_prior = len(sys.modules[PLUGINS_PACKAGE_NAME].__path__) if PLUGINS_PACKAGE_NAME in sys.modules else 0
        new_plugin_directories = []
        for directory in self.allDirectories():
            if self._addPluginDir(directory):
                new_plugin_directories.append(directory)
            else:
                try:
                    names = os.listdir(directory)
                except os.error:
                    continue

                for name in sorted(names):
                    if self._addPluginDir(os.path.join(directory, name)):
                        new_plugin_directories.append(os.path.join(directory, name))

        if len_package_modules_prior == 0:
            try:
                package = import_module(PLUGINS_PACKAGE_NAME)
            except ModuleNotFoundError:
                return
        else:
            for d in new_plugin_directories:
                sys.modules[PLUGINS_PACKAGE_NAME].__path__.append(os.path.join(d, PLUGINS_PACKAGE_NAME))

            package = sys.modules[PLUGINS_PACKAGE_NAME]

        self._import_errors = []
        self._type_errors = []
        self._syntax_errors = []
        self._tab_errors = []
        self._plugin_error_directories = {}
        self._plugin_error_names = []

        # a(pkg_resources.working_set)
        # installed = [pkg.key for pkg in pkg_resources.working_set]
        # print(installed)

        for module_finder, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg:
                try:
                    if is_frozen() and not isinstance(module_finder, importlib.machinery.FileFinder):
                        plugin_dependencies = []
                    else:
                        plugin_dependencies = self.extractPluginDependencies(module_finder.path)
                    missing_dependencies = self._plugin_database.check_for_missing_dependencies(plugin_dependencies)
                    for dependency in missing_dependencies:
                        self.installPackage(dependency)

                    module = import_module(PLUGINS_PACKAGE_NAME + '.' + modname)
                    if hasattr(module, '__version__') and hasattr(module, '__author__'):
                        logger.info('Loaded plugin \'' + modname + '\' version [' + module.__version__ + '] by ' + module.__author__)
                    if hasattr(module, '__location__') and module.__location__:
                        logger.info('Plugin \'' + modname + '\' available from: ' + module.__location__)
                    else:
                        logger.info('Plugin \'' + modname + '\' has no location set.')

                    self._plugin_database.addLoadedPluginInformation(modname,
                                                                     module.__stepname__ if hasattr(module, '__stepname__') else 'None',
                                                                     module.__author__ if hasattr(module, '__author__') else 'Anon.',
                                                                     module.__version__ if hasattr(module, '__version__') else '0.0.0',
                                                                     module.__location__ if hasattr(module, '__location__') else '',
                                                                     plugin_dependencies)
                except Exception as e:
                    from mapclient.mountpoints.workflowstep import removeWorkflowStep
                    # Call remove partially loaded plugin manually method
                    removeWorkflowStep(modname)

                    if type(e) == ImportError:
                        self._import_errors += [modname]
                    elif type(e) == TypeError:
                        self._type_errors += [modname]
                    elif type(e) == SyntaxError:
                        self._syntax_errors += [modname]
                    elif type(e) == TabError:
                        self._tab_errors += [modname]

                    if is_frozen():
                        self._plugin_error_directories[modname] = '<frozen-directory>'
                        step_name = '<frozen-name>'
                    else:
                        self._plugin_error_directories[modname] = module_finder.path
                        step_file_dir = os.path.join(module_finder.path, modname, 'step.py')
                        class_name = determineStepClassName(step_file_dir)
                        step_name = determineStepName(step_file_dir, class_name)
                    self._plugin_error_names.append(step_name)

                    logger.warning('Plugin \'' + modname + '\' not loaded')
                    logger.warning('Reason: {0}'.format(e))
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    redirect_output = FileTypeObject()
                    traceback.print_exception(exc_type, exc_value, exc_traceback, file=redirect_output)
                    logger.warning(''.join(redirect_output.messages))

        # installed = [pkg.key for pkg in pkg_resources.working_set]
        # print(installed)

    def get_plugin_error_names(self):
        return self._plugin_error_names

    def haveErrors(self):
        return len(self._import_errors) or len(self._type_errors) or \
               len(self._syntax_errors) or len(self._tab_errors) or len(self._plugin_error_directories)

    def getPluginErrors(self):
        return {'ImportError': self._import_errors, 'TypeError': self._type_errors, 'SyntaxError': self._syntax_errors, 'TabError': self._tab_errors,
                'directories': self._plugin_error_directories}

    def readSettings(self, settings):
        self._directories = []
        settings.beginGroup('Plugins')
        self._load_default_plugins = settings.value('load_defaults', 'true') == 'true'
        self._doNotShowPluginErrors = settings.value('donot_show_plugin_errors', 'true') == 'true'
        self._virtualenv_setup_attempted = settings.value('virtualenv_setup_attempted', 'false') == 'true'
        directory_count = settings.beginReadArray('directories')
        for i in range(directory_count):
            settings.setArrayIndex(i)
            self._directories.append(settings.value('directory'))
        settings.endArray()
        settings.endGroup()
        settings.beginGroup('Ignored Plugins')
        plugin_count = settings.beginReadArray('plugins')
        for i in range(plugin_count):
            settings.setArrayIndex(i)
            self._ignoredPlugins.append(settings.value('plugins'))
        settings.endArray()
        settings.endGroup()
        settings.beginGroup('Resource Filenames')
        filename_count = settings.beginReadArray('filenames')
        for i in range(filename_count):
            settings.setArrayIndex(i)
            if settings.value('filenames') not in self._resourceFiles:
                self._resourceFiles.append(settings.value('filenames'))
        settings.endArray()
        settings.endGroup()
        settings.beginGroup('Updater Settings')
        option_count = settings.beginReadArray('settings')
        for i in range(option_count):
            settings.setArrayIndex(i)
            bool_str = settings.value('settings').split(' - ')[-1]
            if bool_str == 'True':
                bool_str = True
            else:
                bool_str = False
            self._updaterSettings[settings.value('settings').split(' - ')[0]] = bool_str
        settings.endArray()
        settings.endGroup()

    def writeSettings(self, settings):
        settings.beginGroup('Plugins')
        settings.setValue('load_defaults', self._load_default_plugins)
        settings.setValue('donot_show_plugin_errors', self._doNotShowPluginErrors)
        settings.setValue('virtualenv_setup_attempted', self._virtualenv_setup_attempted)
        settings.beginWriteArray('directories')
        directory_index = 0
        for directory in self._directories:
            settings.setArrayIndex(directory_index)
            settings.setValue('directory', directory)
            directory_index += 1
        settings.endArray()
        settings.endGroup()
        settings.beginGroup('Ignored Plugins')
        settings.beginWriteArray('plugins')
        plugin_index = 0
        for plugin in self._ignoredPlugins:
            settings.setArrayIndex(plugin_index)
            settings.setValue('plugins', plugin)
            plugin_index += 1
        settings.endArray()
        settings.endGroup()
        settings.beginGroup('Resource Filenames')
        settings.beginWriteArray('filenames')
        filename_index = 0
        for filename in self._resourceFiles:
            settings.setArrayIndex(filename_index)
            settings.setValue('filenames', filename)
            filename_index += 1
        settings.endArray()
        settings.endGroup()
        settings.beginGroup('Updater Settings')
        settings.beginWriteArray('settings')
        option_index = 0
        for setting in self._updaterSettings:
            settings.setArrayIndex(option_index)
            settings.setValue('settings', setting + ' - ' + str(self._updaterSettings[setting]))
            option_index += 1
        settings.endArray()
        settings.endGroup()


def isMapClientPluginsDir(plugin_dir):
    result = False
    try:
        names = os.listdir(plugin_dir)
    except:
        return result

    if PLUGINS_PACKAGE_NAME in names:
        files = grep(os.path.join(plugin_dir, PLUGINS_PACKAGE_NAME),
                     r'(from|import) mapclient.mountpoints.workflowstep', one_only=True, file_endswith='.py')
        if files:
            result = True

    return result


class PluginSiteManager(object):
    """
    Python site module/pth based plugin manager.  WIP.
    """

    def __init__(self):
        pass

    def build_site(self, target_dir):
        pth_entries = self.generate_pth_entries(target_dir)
        pth_filename = os.path.join(target_dir, PLUGINS_PTH)

        with open(pth_filename, 'w') as f:
            # should probably check that they are valid packages
            f.write('\n'.join(pth_entries))

    def load_site(self, target_dir):
        # site.addsitedir(target_dir)
        pass


def reload_package(package):
    assert (hasattr(package, "__package__"))
    fn = package.__file__
    fn_dir = os.path.dirname(fn) + os.sep
    module_visit = {fn}
    del fn

    def reload_recursive_ex(module):
        importlib.reload(module)
        print('reloading module: %s' % module)
        for module_child in list(vars(module).values()):
            if isinstance(module_child, types.ModuleType):
                fn_child = getattr(module_child, "__file__", None)
                if (fn_child is not None) and fn_child.startswith(fn_dir):
                    if fn_child not in module_visit:
                        # print("reloading:", fn_child, "from", module)
                        module_visit.add(fn_child)
                        reload_recursive_ex(module_child)

    return reload_recursive_ex(package)


def generate_pth_entries(target_dir):
    if not os.path.isdir(target_dir):
        return []
    g = os.walk(target_dir)
    _, dirs, _ = next(g)
    return [os.path.join(target_dir, d) for d in dirs]


class PluginDatabase:
    """
    Manages plugin information for the current workflow.
    """

    def __init__(self):
        self._database = {}

    def saveState(self, ws, scene):
        """
        Save the state of the current workflow plugin requirements
        to the given workflow configuration.
        """
        ws.remove('required_plugins')
        ws.beginGroup('required_plugins')
        ws.beginWriteArray('plugin')
        pluginIndex = 0
        for item in scene._items:
            if item.Type == 'Step':
                step_name = item._step.getName()
                if step_name in self._database:
                    information_dict = self._database[step_name]
                    ws.setArrayIndex(pluginIndex)
                    ws.setValue('name', step_name)
                    ws.setValue('author', information_dict['author'])
                    ws.setValue('version', information_dict['version'])
                    ws.setValue('location', information_dict['location'])

                    ws.beginWriteArray('dependencies')
                    for dependency_index, dependency in enumerate(information_dict['dependencies']):
                        ws.setArrayIndex(dependency_index)
                        ws.setValue('dependency', dependency)
                    ws.endArray()
                    ws.setValue('dependencies', information_dict['dependencies'])

                    pluginIndex += 1
        ws.endArray()
        ws.endGroup()

    @staticmethod
    def load(ws):
        """
        Load the given Workflow configuration and return it as a dict.
        """
        pluginDict = {}
        ws.beginGroup('required_plugins')
        pluginCount = ws.beginReadArray('plugin')
        for i in range(pluginCount):
            ws.setArrayIndex(i)
            name = ws.value('name')
            pluginDict[name] = {
                'author': ws.value('author'),
                'version': ws.value('version'),
                'location': ws.value('location')
            }
            dependencies = []
            dependency_count = ws.beginReadArray('dependencies')
            for j in range(dependency_count):
                ws.setArrayIndex(j)
                dependencies.append(ws.value('dependency'))
            ws.endArray()
            pluginDict[name]['dependencies'] = dependencies
        ws.endArray()
        ws.endGroup()

        return pluginDict

    def addLoadedPluginInformation(self, plugin_name, step_name, plugin_author, plugin_version, plugin_location, plugin_dependencies):
        plugin_dict = {}
        plugin_dict['plugin name'] = plugin_name
        plugin_dict['author'] = plugin_author
        plugin_dict['version'] = plugin_version
        plugin_dict['location'] = plugin_location
        plugin_dict['dependencies'] = plugin_dependencies
        self._database[step_name] = plugin_dict

    def checkForMissingPlugins(self, to_check):
        """
        Check for the given plugin dict against the dict of plugins currently available.
        """
        missing_plugins = {}
        for plugin in to_check:
            if not (plugin in self._database and \
                    to_check[plugin]['author'] == self._database[plugin]['author'] and \
                    to_check[plugin]['version'] == self._database[plugin]['version']):
                missing_plugins[plugin] = to_check[plugin]

        return missing_plugins

    # Would it be worth using a dictionary instead of a list?
    def check_for_missing_dependencies(self, dependencies):
        """
        Takes a list of dependencies as input. Returns a list of all the dependencies that aren't already installed.
        If a dependency has a url supplied AND it isn't installed, add just the url to the missing_dependencies list.
        """
        installed = [pkg.key for pkg in pkg_resources.working_set]
        missing_dependencies = []
        for dependency in dependencies:
            if '@' in dependency:
                index = dependency.find('@')
                dependency_name = dependency[:index - 1]
                dependency = dependency[index + 2:]
            else:
                dependency_name = dependency

            if dependency_name.lower() not in installed:
                missing_dependencies.append(dependency)

        return missing_dependencies

    def getDatabase(self):
        return self._database
