'''
Created on May 19, 2015

@author: hsorby
'''
import os, sys
import logging
import subprocess
import site
import json
import pkgutil
import traceback

from mapclient.core.utils import which
from mapclient.settings.definitions import VIRTUAL_ENV_PATH, \
    VIRTUAL_ENV_SETUP_ATTEMPTED, PLUGINS_PACKAGE_NAME, PLUGINS_PTH

from importlib import import_module

# if sys.version_info < (3, 0):
#     import imp
# else:
#     import importlib

logger = logging.getLogger(__name__)

def getVirtualEnvCandidates():
    """Return a list of strings which contains possible names
    of the virtualenv program for this environment.
    """
    if sys.version_info < (3, 0):
        virtualenv_candidates = ['virtualenv', 'virtualenv2']
    else:
        virtualenv_candidates = ['virtualenv', 'virtualenv3']

    return virtualenv_candidates


class PluginManagerThe2nd(object):
    '''
    Plugin Manager class
    '''


    def __init__(self, options):
        '''
        Constructor
        '''
        self._virtualenv_dir = options[VIRTUAL_ENV_PATH]
        self._setup_attempted = options[VIRTUAL_ENV_SETUP_ATTEMPTED]

    def setupFailed(self):
        """
        Check whether the setup of the virtual environment failed.
        The first time the application is started it will attempt to create
        a virtual environment for the MAP Client plugins, if this fails then
        this method will return True.  If no virtual environment setup has
        been attempted then this method will return False.
        """
        return self._setup_attempted

    def _loadWorkflowPlugins(self, wf_location):
        wf = _getWorkflowConfiguration(wf_location)

        return PluginDatabase.load(wf)

    def checkPlugins(self, wf_location):
        required_plugins = self._loadWorkflowPlugins(wf_location)
        missing_plugins = self._plugin_database.checkForMissingPlugins(required_plugins)
        return missing_plugins

    def checkDependencies(self, wf_location):
        required_plugins = self._loadWorkflowPlugins(wf_location)
        virtenv_dir = getVirtEnvDirectory()
        vem = PluginManager(virtenv_dir)
        missing_dependencies = {}
        if vem.exists():
            missing_dependencies = self._plugin_database.checkForMissingDependencies(required_plugins, vem.list())
        return missing_dependencies


class PluginManager(object):

    def __init__(self, virtualenv_dir=None):
        self._directories = []
        self._virtualenv_enabled = True
        self._virtualenv_dir = virtualenv_dir
        self._virtualenv_setup_attempted = False
        self._reload_plugins = True
        self._load_default_plugins = True
        self._doNotShowPluginErrors = False
        self._plugin_database = PluginDatabase()
        self._ignoredPlugins = []
        self._unsuccessful_package_installations = {}
        self._resourceFiles = ['resources_rc']
        self._updaterSettings = {'syntax':True, 'indentation':True, 'location':True, 'resources':True}

    def setVirtualEnvEnabled(self, state=True):
        self._virtualenv_enabled = state

    def setVirtualEnvDirectory(self, directory):
        self._virtualenv_dir = directory

    def virtualEnvDirectory(self):
        return self._virtualenv_dir

    def directories(self):
        return self._directories

    def setReloadPlugins(self, state=True):
        self._reload_plugins = state

    def reloadPlugins(self):
        return self._reload_plugins

    def list(self):
        if self._virtualenv_enabled:
            pip_exe = which(os.path.join(self._virtualenv_dir, 'bin', 'pip'))

            install_list = subprocess.check_output([pip_exe, 'list'])
            install_list = install_list.decode('utf-8')
        else:
            install_list = []
            logger.info('VirtualEnv not enabled no list functionality availble.')

        return install_list

    def addSitePackages(self):
        '''
        Append the site-packages directory of the virtual
        environment to the system path
        '''
        if self._virtualenv_enabled:
            site_packages_path = None
            for root, _, _ in os.walk(self._virtualenv_dir , topdown=False):
                if root.endswith('site-packages'):
                    site_packages_path = root
                    break

            if site_packages_path:
                logger.info('Adding site packages directory to the system path: "{0}"'.format(site_packages_path))
                sys.path.append(site_packages_path)
            else:
                logger.warning('Site packages directory not added to sys.path.')
        else:
            logger.info('VirtualEnv not enabled not adding site-packages directory')

    def setOptions(self, options):
        self._virtualenv_dir = options[VIRTUAL_ENV_PATH]

    def setDirectories(self, directories):
        '''
        Set the list of directories to be searched for
        plugins.  Returns true if the directories listing
        was updated and false otherwise.
        '''
        if self._directories != directories:
            self._directories = directories
            self._reload_plugins = True

    def virtualenvSetupAttempted(self):
        return self._virtualenv_setup_attempted

    def virtualEnvExists(self):
        return os.path.exists(os.path.join(self._virtualenv_dir, 'bin'))

    def setupVirtualEnv(self):
        if self._virtualenv_enabled:
            for candidate in getVirtualEnvCandidates():
                try:
                    p = subprocess.Popen([candidate, '--clear', '--system-site-packages', self._virtualenv_dir],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
                    stdout, stderr = p.communicate()

                    if stdout:
                        logger.info(stdout.decode('utf-8'))
                    if stderr:
                        logger.error(stderr.decode('utf-8'))
                except SyntaxError:
                    pass

        else:
            logger.info('VirtualEnv not enabled cannot setup.')

        self._virtualenv_setup_attempted = True

    def loadDefaultPlugins(self):
        return self._load_default_plugins

    def getPluginDatabase(self):
        return self._plugin_database

    def setLoadDefaultPlugins(self, loadDefaultPlugins):
        '''
        Set whether or not the default plugins should be loaded.
        Returns true if the default load plugin setting is changed
        and false otherwise.
        '''
        if self._load_default_plugins != loadDefaultPlugins:
            self._load_default_plugins = loadDefaultPlugins
            self._reload_plugins = True

    def allDirectories(self):
        plugin_dirs = self._directories[:]
        if self._load_default_plugins:
            file_dir = os.path.dirname(os.path.abspath(__file__))
            inbuilt_plugin_dir = os.path.realpath(os.path.join(file_dir, '..', '..', 'plugins'))
            plugin_dirs.insert(0, inbuilt_plugin_dir)

        return plugin_dirs

    def _addPluginDir(self, directory):
        added = False
        if isMapClientPluginsDir(directory):
            site.addsitedir(directory)
            added = True

        return added

    def extractPluginDependencies(self, path):
        return []
        setupFileDir = path[:-16] + 'setup.py'
        dependencies = ''
        if os.path.exists(setupFileDir):
            with open(setupFileDir, 'r') as setup_file:
                contents = setup_file.readlines()
                for line in contents:
                    if dependencies and ']' not in dependencies:
                        if ']' in line:
                            dependencies = dependencies.strip('\n') + line.lstrip()
                            break
                        else:
                            dependencies = dependencies.strip('\n') + line.lstrip()
                            continue
                    if 'dependencies' in line:
                        index = 0
                        for char in line:
                            index += 1
                            if char == '[':
                                break
                        dependencies = line[index - 1:]
            if "'" in dependencies:
                dependencies = dependencies.replace("'", '"')
            if dependencies:
                return json.loads(dependencies)
            else:
                return []

    def load(self):
        self._reload_plugins = False
        len_package_modules_prior = len(sys.modules[PLUGINS_PACKAGE_NAME].__path__) if PLUGINS_PACKAGE_NAME in sys.modules else 0
        for directory in self.allDirectories():
            if not self._addPluginDir(directory):
                try:
                    names = os.listdir(directory)
                except os.error:
                    continue

                for name in sorted(names):
                    self._addPluginDir(os.path.join(directory, name))
        if len_package_modules_prior == 0:
            package = import_module(PLUGINS_PACKAGE_NAME)
        else:
            package = reload(sys.modules[PLUGINS_PACKAGE_NAME])
#             try:
#                 package = imp.reload(sys.modules[PLUGINS_PACKAGE_NAME])
#             except Exception:
#                 package = importlib.reload(sys.modules[PLUGINS_PACKAGE_NAME])
        self._import_errors = []
        self._type_errors = []
        self._syntax_errors = []
        self._tab_errors = []
        self._plugin_error_directories = {}

        for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg:
                try:
                    module = import_module(PLUGINS_PACKAGE_NAME + '.' + modname)
                    plugin_dependencies = self.extractPluginDependencies(package.__path__)
                    if hasattr(module, '__version__') and hasattr(module, '__author__'):
                        logger.info('Loaded plugin \'' + modname + '\' version [' + module.__version__ + '] by ' + module.__author__)
                    if hasattr(module, '__location__') and hasattr(module, '__stepname__'):
                        logger.info('Plugin \'' + modname + '\' available from: ' + module.__location__)

                    self._plugin_database.addLoadedPluginInformation(modname,
                                                                     module.__stepname__ if hasattr(module, '__stepname__') else 'None',
                                                                     module.__author__ if hasattr(module, '__author__') else 'Anon.',
                                                                     module.__version__ if hasattr(module, '__version__') else '0.0.0',
                                                                     module.__location__ if hasattr(module, '__location__') else '',
                                                                     plugin_dependencies)
                except Exception as e:
                    from mapclient.mountpoints.workflowstep import removeWorkflowStep
                    # call remove partially loaded plugin manually method
                    removeWorkflowStep(modname)

                    if type(e) == ImportError:
                        self._import_errors += [modname]
                    elif type(e) == TypeError:
                        self._type_errors += [modname]
                    elif type(e) == SyntaxError:
                        self._syntax_errors += [modname]
                    elif type(e) == TabError:
                        self._tab_errors += [modname]
                    self._plugin_error_directories[modname] = _.path

#                     message = convertExceptionToMessage(e)
                    logger.warn('Plugin \'' + modname + '\' not loaded')
                    logger.warn('Reason: {0}'.format(e))
                    _, _, tb = sys.exc_info()
                    for line in traceback.format_tb(tb):
                        logger.warn(line)
#                     logger.warn('\n'.join(traceback.format_tb(tb)))

    def haveErrors(self):
        return len(self._import_errors) or len(self._type_errors) or \
                len(self._syntax_errors) or len(self._tab_errors) or len(self._plugin_error_directories)

    def getPluginErrors(self):
        return {'ImportError': self._import_errors, 'TypeError': self._type_errors, 'SyntaxError': self._syntax_errors, 'TabError': self._tab_errors, 'directories': self._plugin_error_directories}

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
        init_file = os.path.join(plugin_dir, PLUGINS_PACKAGE_NAME, '__init__.py')
        if os.path.isfile(init_file):
            contents = open(init_file).read()
            if 'pkgutil' in contents and 'extend_path' in contents:
                result = True

    return result

class PluginSiteManager(object):
    """
    Python site module/pth based plugin manager.  WIP.
    """

    def __init__(self):
        pass

    def generate_pth_entries(self, target_dir):
        if not os.path.isdir(target_dir):
            return []
        g = os.walk(target_dir)
        _, dirs, _ = next(g)
        return [os.path.join(target_dir, d) for d in dirs]

    def build_site(self, target_dir):
        pth_entries = self.generate_pth_entries(target_dir)
        pth_filename = os.path.join(target_dir, PLUGINS_PTH)

        with open(pth_filename, 'w') as f:
            # should probably check that they are valid packages
            f.write('\n'.join(pth_entries))

    def load_site(self, target_dir):
        site.addsitedir(target_dir)

class PluginDatabase:
    '''
    Manages plugin information for the current workflow.
    '''

    def __init__(self):
        self._database = {}

    def saveState(self, ws, scene):
        '''
        Save the state of the current workflow plugin requirements
        to the given workflow configuration.
        '''
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
        '''
        Load the given Workflow configuration and return it as a dict.
        '''
        pluginDict = {}
        ws.beginGroup('required_plugins')
        pluginCount = ws.beginReadArray('plugin')
        for i in range(pluginCount):
            ws.setArrayIndex(i)
            name = ws.value('name')
            pluginDict[name] = {
                'author':ws.value('author'),
                'version':ws.value('version'),
                'location':ws.value('location')
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
        '''
        Check for the given plugin dict against the dict of plugins currently available.
        '''
        missing_plugins = {}
        for plugin in to_check:
            if not (plugin in self._database and \
                to_check[plugin]['author'] == self._database[plugin]['author'] and \
                to_check[plugin]['version'] == self._database[plugin]['version']):
                missing_plugins[plugin] = to_check[plugin]

        return missing_plugins

    def checkForMissingDependencies(self, to_check, available_dependencies):
        '''
        Check the given plugin dependencies against the list of currently available
        dependencies
        '''
        print('CHECK ME: INCOMPLETE')
        required_dependencies = {}
        for plugin in to_check:
            pass
#         for name in dependencies:
#             if name not in install_list:
#                 required_dependencies += [name]

#         print sys.modules[PLUGINS_PACKAGE_NAME]
        return required_dependencies

    def getDatabase(self):
        return self._database

