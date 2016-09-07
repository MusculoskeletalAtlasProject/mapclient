"""
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
"""
import unittest
import sys
import os
import pkgutil
import shutil
import logging

logger = logging.getLogger()

from mapclient.view.managers.plugins.pluginupdater import PluginUpdater

root_dir = os.path.join(os.path.realpath(__file__)[:-29], 'test_resources', 'updater_test')
if not os.path.exists(os.path.join(root_dir[:-13], 'updater_test_updated_plugins')):
    os.mkdir(os.path.join(root_dir[:-13], 'updater_test_updated_plugins'))
copy_dir = os.path.join(root_dir[:-13], 'updater_test_updated_plugins')

class PluginUpdaterTestCase(unittest.TestCase):

    def setUp(self):
        self._pluginUpdater = PluginUpdater()
        self.testPlugins = {}
        package = [os.path.join(root_dir, name, 'mapclientplugins') for name in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, name, 'mapclientplugins'))]
        for importer, modname, _ in pkgutil.iter_modules(package):
            self.testPlugins[modname] = importer
        for plugin in [os.path.join(root_dir, name) for name in os.listdir(root_dir)]:
            shutil.copytree(plugin, plugin.replace('updater_test', 'updater_test_updated_plugins'))

    def updatePlugin(self, plugin):
        if self._pluginUpdater._pluginUpdateDict[plugin][4] and sys.version_info > (2, 7):
            self._pluginUpdater.fixTabbedIndentation(plugin, self._pluginUpdater._pluginUpdateDict[plugin][7], False)
        if self._pluginUpdater._pluginUpdateDict[plugin][3]:
            self._pluginUpdater.updateSyntax(plugin, self._pluginUpdater._pluginUpdateDict[plugin][0])
        if self._pluginUpdater._pluginUpdateDict[plugin][1]:
            self._pluginUpdater.updateInitContents(plugin, self._pluginUpdater._pluginUpdateDict[plugin][5])
        if self._pluginUpdater._pluginUpdateDict[plugin][2]:
            self._pluginUpdater.updateResourcesFile(plugin, self._pluginUpdater._pluginUpdateDict[plugin][6])

    @unittest.skip('Not currently working, possibly out of date to current implmentation')
    def test_plugin_1(self):
        test1 = self.testPlugins['fieldworkmodelevaluationstep']
        self._pluginUpdater._directory = test1.path.replace('updater_test', 'updater_test_updated_plugins')

        plugin_resources_update, resourcesDir = self._pluginUpdater.checkResourcesUpdate(os.path.join(test1.path, 'fieldworkmodelevaluationstep'), [])
        plugin_init_update = self._pluginUpdater.checkPluginInitContents(os.path.join(test1.path, 'fieldworkmodelevaluationstep', '__init__.py'))
        plugin_tabbed_indentation, tabbed_modules = self._pluginUpdater.checkTabbedIndentation(test1.path)
        if plugin_tabbed_indentation:
            self._pluginUpdater.fixTabbedIndentation('fieldworkmodelevaluationstep', tabbed_modules, True)
        plugin_syntax_update = self._pluginUpdater.checkModuleSyntax(test1.path)
        self._pluginUpdater.deleteTempFiles(tabbed_modules)

        resourcesDir = resourcesDir.replace('updater_test', 'updater_test_updated_plugins')
        new_tabbed_modules = []
        for module in tabbed_modules:
            module = module.replace('updater_test', 'updater_test_updated_plugins')
            new_tabbed_modules += [module]
        tabbed_modules = new_tabbed_modules

        self._pluginUpdater.pluginUpdateDict('fieldworkmodelevaluationstep', plugin_init_update, plugin_resources_update, plugin_syntax_update, \
                                                    plugin_tabbed_indentation, os.path.join(os.path.join(copy_dir, 'fieldworkmodelevaluationstep-master', 'mapclientplugins'), 'fieldworkmodelevaluationstep', '__init__.py'), resourcesDir, tabbed_modules)

        self.assertEqual([plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation], [True, True, False, False])

        self.updatePlugin('fieldworkmodelevaluationstep')
        init_status = self._pluginUpdater.checkSuccessfulInitUpdate(self._pluginUpdater._pluginUpdateDict['fieldworkmodelevaluationstep'][5])
        resources_status = self._pluginUpdater.checkSuccessfulResourceUpdate(self._pluginUpdater._pluginUpdateDict['fieldworkmodelevaluationstep'][6])

        self.assertEqual([init_status, resources_status], [False, False])

    @unittest.skip('Not currently working, possibly out of date to current implmentation')
    def test_plugin_2(self):
        test2 = self.testPlugins['fieldworkpcregfemur2landmarksstep']
        self._pluginUpdater._directory = test2.path.replace('updater_test', 'updater_test_updated_plugins')

        plugin_resources_update, resourcesDir = self._pluginUpdater.checkResourcesUpdate(os.path.join(test2.path, 'fieldworkpcregfemur2landmarksstep'), [])
        plugin_init_update = self._pluginUpdater.checkPluginInitContents(os.path.join(test2.path, 'fieldworkpcregfemur2landmarksstep', '__init__.py'))
        plugin_tabbed_indentation, tabbed_modules = self._pluginUpdater.checkTabbedIndentation(test2.path)
        if plugin_tabbed_indentation:
            self._pluginUpdater.fixTabbedIndentation('fieldworkpcregfemur2landmarksstep', tabbed_modules, True)
        plugin_syntax_update = self._pluginUpdater.checkModuleSyntax(test2.path)
        self._pluginUpdater.deleteTempFiles(tabbed_modules)

        resourcesDir = resourcesDir.replace('updater_test', 'updater_test_updated_plugins')
        new_tabbed_modules = []
        for module in tabbed_modules:
            module = module.replace('updater_test', 'updater_test_updated_plugins')
            new_tabbed_modules += [module]
        tabbed_modules = new_tabbed_modules

        self._pluginUpdater.pluginUpdateDict('fieldworkpcregfemur2landmarksstep', plugin_init_update, plugin_resources_update, plugin_syntax_update, \
                                                    plugin_tabbed_indentation, os.path.join(os.path.join(copy_dir, 'fieldworkpcregfemur2landmarksstep-master', 'mapclientplugins'), 'fieldworkpcregfemur2landmarksstep', '__init__.py'), resourcesDir, tabbed_modules)

        self.assertEqual([plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation], [True, True, True, True])

        self.updatePlugin('fieldworkpcregfemur2landmarksstep')
        init_status = self._pluginUpdater.checkSuccessfulInitUpdate(self._pluginUpdater._pluginUpdateDict['fieldworkpcregfemur2landmarksstep'][5])
        resources_status = self._pluginUpdater.checkSuccessfulResourceUpdate(self._pluginUpdater._pluginUpdateDict['fieldworkpcregfemur2landmarksstep'][6])
        syntax_status = self._pluginUpdater.checkModuleSyntax(self._pluginUpdater._pluginUpdateDict['fieldworkpcregfemur2landmarksstep'][0])
        indentation_status = self._pluginUpdater.checkSuccessfulIndentationUpdate(self._pluginUpdater._pluginUpdateDict['fieldworkpcregfemur2landmarksstep'][7])

        self.assertEqual([init_status, resources_status, syntax_status, indentation_status], [False, False, False, False])

    @unittest.skip('Not currently working, possibly out of date to current implmentation')
    def test_plugin_3(self):
        test3 = self.testPlugins['loadstlstep']
        self._pluginUpdater._directory = test3.path.replace('updater_test', 'updater_test_updated_plugins')

        plugin_resources_update, resourcesDir = self._pluginUpdater.checkResourcesUpdate(os.path.join(test3.path, 'loadstlstep'), [])
        plugin_init_update = self._pluginUpdater.checkPluginInitContents(os.path.join(test3.path, 'loadstlstep', '__init__.py'))
        plugin_tabbed_indentation, tabbed_modules = self._pluginUpdater.checkTabbedIndentation(test3.path)
        if plugin_tabbed_indentation:
            self._pluginUpdater.fixTabbedIndentation('loadstlstep', tabbed_modules, True)
        plugin_syntax_update = self._pluginUpdater.checkModuleSyntax(test3.path)
        self._pluginUpdater.deleteTempFiles(tabbed_modules)

        resourcesDir = resourcesDir.replace('updater_test', 'updater_test_updated_plugins')
        new_tabbed_modules = []
        for module in tabbed_modules:
            module = module.replace('updater_test', 'updater_test_updated_plugins')
            new_tabbed_modules += [module]
        tabbed_modules = new_tabbed_modules

        self._pluginUpdater.pluginUpdateDict('loadstlstep', plugin_init_update, plugin_resources_update, plugin_syntax_update, \
                                                    plugin_tabbed_indentation, os.path.join(os.path.join(copy_dir, 'loadstlstep-master', 'mapclientplugins'), 'loadstlstep', '__init__.py'), resourcesDir, tabbed_modules)

        self.assertEqual([plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation], [True, False, False, False])

        self.updatePlugin('loadstlstep')
        init_status = self._pluginUpdater.checkSuccessfulInitUpdate(self._pluginUpdater._pluginUpdateDict['loadstlstep'][5])
        self.assertEqual(init_status, False)

    @unittest.skip('Not currently working, possibly out of date to current implmentation')
    def test_plugin_4(self):
        test4 = self.testPlugins['mayaviviewerstep']
        self._pluginUpdater._directory = test4.path.replace('updater_test', 'updater_test_updated_plugins')

        plugin_resources_update, resourcesDir = self._pluginUpdater.checkResourcesUpdate(os.path.join(test4.path, 'mayaviviewerstep'), [])
        plugin_init_update = self._pluginUpdater.checkPluginInitContents(os.path.join(test4.path, 'mayaviviewerstep', '__init__.py'))
        plugin_tabbed_indentation, tabbed_modules = self._pluginUpdater.checkTabbedIndentation(test4.path)
        if plugin_tabbed_indentation:
            self._pluginUpdater.fixTabbedIndentation('mayaviviewerstep', tabbed_modules, True)
        plugin_syntax_update = self._pluginUpdater.checkModuleSyntax(test4.path)
        self._pluginUpdater.deleteTempFiles(tabbed_modules)

        resourcesDir = resourcesDir.replace('updater_test', 'updater_test_updated_plugins')
        new_tabbed_modules = []
        for module in tabbed_modules:
            module = module.replace('updater_test', 'updater_test_updated_plugins')
            new_tabbed_modules += [module]
        tabbed_modules = new_tabbed_modules

        self._pluginUpdater.pluginUpdateDict('mayaviviewerstep', plugin_init_update, plugin_resources_update, plugin_syntax_update, \
                                                    plugin_tabbed_indentation, os.path.join(os.path.join(copy_dir, 'mayaviviewerstep-master', 'mapclientplugins'), 'mayaviviewerstep', '__init__.py'), resourcesDir, tabbed_modules)

        self.assertEqual([plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation], [True, False, True, True])

        self.updatePlugin('mayaviviewerstep')
        init_status = self._pluginUpdater.checkSuccessfulInitUpdate(self._pluginUpdater._pluginUpdateDict['mayaviviewerstep'][5])
        syntax_status = self._pluginUpdater.checkModuleSyntax(self._pluginUpdater._pluginUpdateDict['mayaviviewerstep'][0])
        indentation_status = self._pluginUpdater.checkSuccessfulIndentationUpdate(self._pluginUpdater._pluginUpdateDict['mayaviviewerstep'][7])

        self.assertEqual([init_status, syntax_status, indentation_status], [False, False, False])

    @unittest.skip('Not currently working, possibly out of date to current implmentation')
    def test_plugin_5(self):
        test5 = self.testPlugins['pelvislandmarkshjcpredictionstep']
        self._pluginUpdater._directory = test5.path.replace('updater_test', 'updater_test_updated_plugins')

        plugin_resources_update, resourcesDir = self._pluginUpdater.checkResourcesUpdate(os.path.join(test5.path, 'pelvislandmarkshjcpredictionstep'), [])
        plugin_init_update = self._pluginUpdater.checkPluginInitContents(os.path.join(test5.path, 'pelvislandmarkshjcpredictionstep', '__init__.py'))
        plugin_tabbed_indentation, tabbed_modules = self._pluginUpdater.checkTabbedIndentation(test5.path)
        if plugin_tabbed_indentation:
            self._pluginUpdater.fixTabbedIndentation('pelvislandmarkshjcpredictionstep', tabbed_modules, True)
        plugin_syntax_update = self._pluginUpdater.checkModuleSyntax(test5.path)
        self._pluginUpdater.deleteTempFiles(tabbed_modules)

        resourcesDir = resourcesDir.replace('updater_test', 'updater_test_updated_plugins')
        new_tabbed_modules = []
        for module in tabbed_modules:
            module = module.replace('updater_test', 'updater_test_updated_plugins')
            new_tabbed_modules += [module]
        tabbed_modules = new_tabbed_modules

        self._pluginUpdater.pluginUpdateDict('pelvislandmarkshjcpredictionstep', plugin_init_update, plugin_resources_update, plugin_syntax_update, \
                                                    plugin_tabbed_indentation, os.path.join(os.path.join(copy_dir, 'pelvislandmarkshjcpredictionstep-master', 'mapclientplugins'), 'pelvislandmarkshjcpredictionstep', '__init__.py'), resourcesDir, tabbed_modules)

        self.assertEqual([plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation], [True, False, True, True])

        self.updatePlugin('pelvislandmarkshjcpredictionstep')
        init_status = self._pluginUpdater.checkSuccessfulInitUpdate(self._pluginUpdater._pluginUpdateDict['pelvislandmarkshjcpredictionstep'][5])
        syntax_status = self._pluginUpdater.checkModuleSyntax(self._pluginUpdater._pluginUpdateDict['pelvislandmarkshjcpredictionstep'][0])
        indentation_status = self._pluginUpdater.checkSuccessfulIndentationUpdate(self._pluginUpdater._pluginUpdateDict['pelvislandmarkshjcpredictionstep'][7])

        self.assertEqual([init_status, syntax_status, indentation_status], [False, False, False])

    @unittest.skip('Not currently working, possibly out of date to current implmentation')
    def test_plugin_6(self):
        test6 = self.testPlugins['stringsource2step']
        self._pluginUpdater._directory = test6.path.replace('updater_test', 'updater_test_updated_plugins')

        plugin_resources_update, resourcesDir = self._pluginUpdater.checkResourcesUpdate(os.path.join(test6.path, 'stringsource2step'), ['resources_rc'])
        plugin_init_update = self._pluginUpdater.checkPluginInitContents(os.path.join(test6.path, 'stringsource2step', '__init__.py'))
        plugin_tabbed_indentation, tabbed_modules = self._pluginUpdater.checkTabbedIndentation(test6.path)
        if plugin_tabbed_indentation:
            self._pluginUpdater.fixTabbedIndentation('stringsource2step', tabbed_modules, True)
        plugin_syntax_update = self._pluginUpdater.checkModuleSyntax(test6.path)
        self._pluginUpdater.deleteTempFiles(tabbed_modules)

#         resourcesDir = resourcesDir.replace('updater_test', 'updater_test_updated_plugins')
        new_tabbed_modules = []
        for module in tabbed_modules:
            module = module.replace('updater_test', 'updater_test_updated_plugins')
            new_tabbed_modules += [module]
        tabbed_modules = new_tabbed_modules

        self._pluginUpdater.pluginUpdateDict('stringsource2step', plugin_init_update, plugin_resources_update, plugin_syntax_update, \
                                                    plugin_tabbed_indentation, os.path.join(os.path.join(copy_dir, 'stringsource2step-master', 'mapclientplugins'), 'stringsource2step', '__init__.py'), resourcesDir, tabbed_modules)

        self.assertEqual([plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation], [True, True, True, False])

        self.updatePlugin('stringsource2step')
        init_status = self._pluginUpdater.checkSuccessfulInitUpdate(self._pluginUpdater._pluginUpdateDict['stringsource2step'][5])
        resources_status = self._pluginUpdater.checkSuccessfulResourceUpdate(self._pluginUpdater._pluginUpdateDict['stringsource2step'][6])
        syntax_status = self._pluginUpdater.checkModuleSyntax(self._pluginUpdater._pluginUpdateDict['stringsource2step'][0])

        self.assertEqual([init_status, resources_status, syntax_status], [False, False, False])

    @unittest.skip('Not currently working, possibly out of date to current implmentation')
    def test_plugin_7(self):
        test7 = self.testPlugins['transformmodeltoimagespacestep']
        self._pluginUpdater._directory = test7.path.replace('updater_test', 'updater_test_updated_plugins')

        plugin_resources_update, resourcesDir = self._pluginUpdater.checkResourcesUpdate(os.path.join(test7.path, 'transformmodeltoimagespacestep'), [])
        plugin_init_update = self._pluginUpdater.checkPluginInitContents(os.path.join(test7.path, 'transformmodeltoimagespacestep', '__init__.py'))
        plugin_tabbed_indentation, tabbed_modules = self._pluginUpdater.checkTabbedIndentation(test7.path)
        if plugin_tabbed_indentation:
            self._pluginUpdater.fixTabbedIndentation('transformmodeltoimagespacestep', tabbed_modules, True)
        plugin_syntax_update = self._pluginUpdater.checkModuleSyntax(test7.path)
        self._pluginUpdater.deleteTempFiles(tabbed_modules)

        resourceDir = resourcesDir.replace('updater_test', 'updater_test_updated_plugins')
        new_tabbed_modules = []
        for module in tabbed_modules:
            module = module.replace('updater_test', 'updater_test_updated_plugins')
            new_tabbed_modules += [module]
        tabbed_modules = new_tabbed_modules

        self._pluginUpdater.pluginUpdateDict('transformmodeltoimagespacestep', plugin_init_update, plugin_resources_update, plugin_syntax_update, \
                                                    plugin_tabbed_indentation, os.path.join(os.path.join(copy_dir, 'transformmodeltoimagespacestep-master', 'mapclientplugins'), 'transformmodeltoimagespacestep', '__init__.py'), resourcesDir, tabbed_modules)

        self.assertEqual([plugin_init_update, plugin_resources_update, plugin_syntax_update, plugin_tabbed_indentation], [True, False, True, False])

        self.updatePlugin('transformmodeltoimagespacestep')
        init_status = self._pluginUpdater.checkSuccessfulInitUpdate(self._pluginUpdater._pluginUpdateDict['transformmodeltoimagespacestep'][5])
        syntax_status = self._pluginUpdater.checkModuleSyntax(self._pluginUpdater._pluginUpdateDict['transformmodeltoimagespacestep'][0])

        self.assertEqual([init_status, syntax_status], [False, False])

    def tearDown(self):
        for plugin in os.listdir(copy_dir):
            shutil.rmtree(os.path.join(copy_dir, plugin))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
