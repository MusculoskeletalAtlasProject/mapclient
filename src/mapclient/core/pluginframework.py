'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''

'''
Inspired by Marty Alchin's Simple plugin framework.
http://martyalchin.com/2008/jan/10/simple-plugin-framework/
'''

import logging
import os
import site
import sys
import pkgutil
from importlib import import_module
from mapclient.core.pluginlocationmanager import PluginLocationManager

if sys.version_info < (3, 0):
    import imp
else:
    import importlib
    
from mapclient.core.utils import convertExceptionToMessage

logger = logging.getLogger(__name__)

PLUGINS_PACKAGE_NAME = 'mapclientplugins'
PLUGINS_PTH = PLUGINS_PACKAGE_NAME + '.pth'
MAIN_MODULE = '__init__'

def getPlugins(pluginDirectory):
    '''
    Get all plugins from the given directory.
    '''
    plugins = []
    try:
        possibleplugins = os.listdir(pluginDirectory)
    except OSError:
        possibleplugins = []
    for i in possibleplugins:
        # print('possible plugin: ' + i)
        location = os.path.join(pluginDirectory, i)
        if not os.path.isdir(location) or not MAIN_MODULE + '.py' in os.listdir(location):
            continue
        info = imp.find_module(MAIN_MODULE, [location])
        plugins.append({'name': i, 'info': info})

    return plugins

def loadPlugin(plugin):
    return imp.load_module(MAIN_MODULE, *plugin['info'])

# class LoadDepth(object):
#    depth = 0
#
# def loadPlugins(pkgDir):
#    ii = pkgutil.ImpImporter(pkgDir)
# #    sys.path.insert(0, pkgDir)
#    LoadDepth.depth += 1
#    try:
#        for moduleName, isPkg in ii.iter_modules():
# #        projectName = os.path.basename(pkgDir)
#            if isPkg:
#                pkgPath = os.path.join(pkgDir, moduleName)
#                initPackage(pkgPath)
# #                project = __import__(moduleName)
# #                print(moduleName)
# #                sys.modules[moduleName] = project
#
#                loadPlugins(pkgPath)
#            else:
#                loadModule(moduleName, pkgDir)
# #            print(moduleName)
#    finally:
# #        print(sys.path)
# #        del sys.path[0]
#        LoadDepth.depth -= 1
# #        print(sys.path)
#
# def loadPlugins2(pkgDir):
#    ii = pkgutil.ImpImporter(pkgDir)
#    LoadDepth.depth += 1
# #    print(LoadDepth.depth)
#    for moduleName, isPkg in ii.iter_modules():
#        if isPkg:
#            pkgPath = os.path.join(pkgDir, moduleName)
#            module = initPackage(pkgPath)
# #            print(pkgPath)
#            if module and pkgDir not in sys.path and LoadDepth.depth == 1:
#                sys.path.append(pkgDir)
# #                print(pkgDir)
# #            __import__(moduleName)
#            loadPlugins(pkgPath)
#        else:
# #            print(moduleName, pkgDir)
#            loadModule(moduleName, pkgDir)
#
#    LoadDepth.depth -= 1
#
# def initPackage(pkgDir):
#    fp, path, description = imp.find_module('__init__', [pkgDir])
#    module = imp.load_module(pkgDir, fp, path, description)
# #    try:
# #        module = imp.load_module(pkgDir, fp, path, description)
# #    except:
# #        module = None
# #        print('Failed to initialise package {0}.'.format(pkgDir))
# #    finally:
# #        if fp:
# #            fp.close()
#    if LoadDepth.depth == 1:
#        print("Plugin '{0}' version {1} by {2} loaded".format(pkgDir.split(os.sep)[-1], module.__version__, module.__author__))
#    fp.close()
#
#    return module
#
# def loadModule(moduleName, moduleDir):
#    fp, path, description = imp.find_module(moduleName, [moduleDir])
#
#    print(moduleDir)
#    imp.load_module(moduleDir, fp, path, description)
# #    print('======= module', module)
#
# #    moduleVersion = '-.-.-'
# #    if hasattr(module, '__version__'):
# #        moduleVersion = module.__version__
# #    moduleAuthor = '?'
# #    if hasattr(module, '__author__'):
# #        moduleAuthor = module.__author__
# #    print("Plugin '{0}' version {1} by {2} loaded".format(moduleName, moduleVersion, moduleAuthor))
#    fp.close()
# #    try:
# #        module = imp.load_module(moduleDir, fp, path, description)
# #
# #        moduleVersion = '-.-.-'
# #        if hasattr(module, '__version__'):
# #            moduleVersion = module.__version__
# #        moduleAuthor = '?'
# #        if hasattr(module, '__author__'):
# #            moduleAuthor = module.__author__
# #        print("Plugin '{0}' version {1} by {2} loaded".format(moduleName, moduleVersion, moduleAuthor))
# #    except:
# #        # non modules will fail
# #        print("Plugin '{0}' not loaded".format(moduleName))
# #    finally:
# #        if fp:
# #            fp.close()
#
# class PluginsAt(object):
#    '''
#    Descriptor to get plugins on a given mount point.
#    '''
#    def __init__(self, mount_point):
#        '''
#        Initialise the descriptor with the mount point wanted.
#        Eg: PluginsAt(PluginFramework.MenuOption) to get extensions that change the GUI Menu.
#        '''
#        self.mount = mount_point
#
#    def __get__(self, instance, owner=None):
#        '''
#        Plugins are instantiated with the object that is calling them.
#        '''
#        return [p() for p in self.mount.plugins]


# import traceback
class MetaPluginMountPoint(type):
    '''
    * A way to declare a mount point for plugins. Since plugins are an example 
      of loose coupling, there needs to be a neutral location, somewhere between
      the plugins and the code that uses them, that each side of the system can
      look at, without having to know the details of the other side. Trac calls
      this an 'extension point'.
    * A way to register a plugin at a particular mount point. Since internal code
      can't (or at the very least, shouldn't have to) look around to find plugins 
      that might work for it, there needs to be a way for plugins to announce their
      presence. This allows the guts of the system to be blissfully ignorant of 
      where the plugins come from; again, it only needs to care about the mount point.
    * A way to retrieve the plugins that have been registered. Once the plugins 
      have done their thing at the mount point, the rest of the system needs to
      be able to iterate over the installed plugins and use them according to its need.

    For compatibility across python 2.x and python 3.x we must construct the PluginMountPoint
    classes like so:
    MyPlugin = MetaPluginMountPoint('MyPlugin', (object, ), {})
    '''

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)

#        traceback.print_stack()
#        for item in sys.modules:
#            print(item)
#        print('=========', cls, name)

    def getPlugins(self, *args, **kwargs):
        return [p(*args, **kwargs) for p in self.plugins]


# Plugin mount points are defined below.
# For running in both python 2.x and python 3.x we must follow the example found
# at http://mikewatkins.ca/2008/11/29/python-2-and-3-metaclasses/
from PySide.QtCore import QObject

MetaQObject = type(QObject)

# For multiple inheritance in classes we also need to create a metaclass that also
# inherits from the metaclasses of the inherited classes
class MetaQObjectPluginMountPoint(MetaQObject, MetaPluginMountPoint):

    def __init__(self, name, bases, attrs):
        MetaPluginMountPoint.__init__(self, name, bases, attrs)
        MetaQObject.__init__(self, name, bases, attrs)


#
# Template plugin comment:
#
# '''
# Plugins can inherit this mount point to extend
#
# A plugin that registers this mount point must have attributes
# * None
#
# A plugin that registers this mount point could have attributes
# * None
#
# It must implement
# * pass
#
# '''
#

'''
Plugins can inherit this mount point to add a tool to the tool menu.  It is passed two 
keyword arguments, the tool menu ('menu_Tool') and the parent widget ('parent').

 A plugin that registers this mount point must have attributes
 * None
 
 A plugin that registers this mount point could have attributes
 * None
 
 It must implement
 * pass 
 
'''
ToolMountPoint = MetaPluginMountPoint('ToolMountPoint', (object,), {})


class PluginManager(object):

    def __init__(self):
        self._directories = []
        self._loadDefaultPlugins = True
        self._doNotShowPluginErrors = False
        self._pluginLocationManager = PluginLocationManager()
        self._ignoredPlugins = []
        self._resourceFiles = ['resources_rc']
        self._updaterSettings = {'syntax':True, 'indentation':True, 'location':True, 'resources':True, 'dependencies':False}

    def directories(self):
        return self._directories

    def setDirectories(self, directories):
        '''
        Set the list of directories to be searched for
        plugins.  Returns true if the directories listing
        was updated and false otherwise.
        '''
        directories_changed = False
        if self._directories != directories:
            self._directories = directories
            directories_changed = True

        return directories_changed

    def loadDefaultPlugins(self):
        return self._loadDefaultPlugins
        
    def getPluginLocationManager(self):
        return self._pluginLocationManager

    def setLoadDefaultPlugins(self, loadDefaultPlugins):
        '''
        Set whether or not the default plugins should be loaded.
        Returns true if the default load plugin setting is changed
        and false otherwise.
        '''
        defaults_changed = False
        if self._loadDefaultPlugins != loadDefaultPlugins:
            self._loadDefaultPlugins = loadDefaultPlugins
            defaults_changed = True

        return defaults_changed

    def allDirectories(self):
        plugin_dirs = self._directories[:]
        if self._loadDefaultPlugins:
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
        return None

    def load(self):
        len_package_modules_prior = len(sys.modules['mapclientplugins'].__path__) if 'mapclientplugins' in sys.modules else 0
        for directory in self.allDirectories():
            if not self._addPluginDir(directory):
                try:
                    names = os.listdir(directory)
                except os.error:
                    continue

                for name in sorted(names):
                    self._addPluginDir(os.path.join(directory, name))
        if len_package_modules_prior == 0:
            package = import_module('mapclientplugins') 
        else:
            try:
                package = imp.reload(sys.modules['mapclientplugins'])
            except Exception:
                package = importlib.reload(sys.modules['mapclientplugins'])
        
        self._import_errors = []
        self._type_errors = []
        self._syntax_errors = []
        self._tab_errors = []
        self._plugin_error_directories = {}

        for _, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg:                
                try:
                    module = import_module('mapclientplugins.' + modname)
                    plugin_dependencies = self.extractPluginDependencies(_.path)
                    if hasattr(module, '__version__') and hasattr(module, '__author__'):
                        logger.info('Loaded plugin \'' + modname + '\' version [' + module.__version__ + '] by ' + module.__author__)
                    if hasattr(module, '__location__') and hasattr(module, '__stepname__'):
                        logger.info('Plugin \'' + modname + '\' available from: ' + module.__location__)
                        self._pluginLocationManager.addLoadedPluginInformation(modname, module.__stepname__, module.__author__, module.__version__, module.__location__, plugin_dependencies)
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
                        
                    message = convertExceptionToMessage(e)
                    logger.warn('Plugin \'' + modname + '\' not loaded')
                    logger.warn('Reason: {0}'.format(message))
    
    def getPluginErrors(self):
        return {'ImportError':self._import_errors, 'TypeError':self._type_errors, 'SyntaxError':self._syntax_errors, 'TabError':self._tab_errors, 'directories':self._plugin_error_directories}
            
    def showPluginErrorsDialog(self):
        from mapclient.widgets.pluginerrors import PluginErrors
        dlg = PluginErrors(self.getPluginErrors(), self._ignoredPlugins, self._resourceFiles, self._updaterSettings)
        if not self._doNotShowPluginErrors:
            dlg.setModal(True)
            dlg.fillList()
            dlg.exec_()
        ignored_plugins = dlg.getIgnoredPlugins()
        for plugin in ignored_plugins:
            if plugin not in self._ignoredPlugins:
                self._ignoredPlugins += [plugin]        
        if dlg._doNotShow:
            self._doNotShowPluginErrors = True
        if dlg._hotfixExecuted:
            self.load()

    def readSettings(self, settings):
        self._directories = []
        settings.beginGroup('Plugins')
        self._loadDefaultPlugins = settings.value('load_defaults', 'true') == 'true'
        self._doNotShowPluginErrors = settings.value('donot_show_plugin_errors', 'true') == 'true'
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
        settings.setValue('load_defaults', self._loadDefaultPlugins)
        settings.setValue('donot_show_plugin_errors', self._doNotShowPluginErrors)
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
