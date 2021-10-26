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
import os, sys, logging, subprocess, py_compile, string
from mapclient.settings.general import get_log_directory

logger = logging.getLogger(__name__)

MAPCLIENT_PLUGIN_LOCATIONS = {'autosegmentationstep':['Automatic Segmenter', 'https://github.com/mapclient-plugins/autosegmentationstep/archive/master.zip'],
                              'fieldworkexportstlsurfacestep':['Fieldwork Export STL Surface', 'https://github.com/mapclient-plugins/fieldworkexportstlsurfacestep/archive/master.zip'],
                              'fieldworkfemurmeasurementstep':['Fieldwork Femur Measurements', 'https://github.com/mapclient-plugins/fieldworkfemurmeasurementstep/archive/master.zip'],
                              'fieldworkhostmeshfittingstep':['Fieldwork Host Mesh Fitting', 'https://github.com/mapclient-plugins/fieldworkhostmeshfittingstep/archive/master.zip'],
                              'fieldworkmeshfittingstep':['Fieldwork Mesh Fitting', 'https://github.com/mapclient-plugins/fieldworkmeshfittingstep/archive/master.zip'],
                              'fieldworkmodeldictmakerstep':['Fieldwork Model Dict Maker', 'https://github.com/mapclient-plugins/fieldworkmodeldictmakerstep/archive/master.zip'],
                              'fieldworkmodelevaluationstep':['Fieldwork Model Evaluation', 'https://github.com/mapclient-plugins/fieldworkmodelevaluationstep/archive/master.zip'], 
                              'fieldworkmodellandmarkstep':['Fieldwork Model Landmarker', 'https://github.com/mapclient-plugins/fieldworkmodellandmarkstep/archive/master.zip'],
                              'fieldworkmodelselectorstep':['Fieldwork Model Selector', 'https://github.com/mapclient-plugins/fieldworkmodelselectorstep/archive/master.zip'],
                              'fieldworkmodelserialiserstep':['Fieldwork Model Serialiser', 'https://github.com/mapclient-plugins/fieldworkmodelserialiserstep/archive/master.zip'],
                              'fieldworkmodelsourcestep':['Fieldwork Model Source', 'https://github.com/mapclient-plugins/fieldworkmodelsourcestep/archive/master.zip'],
                              'fieldworkmodeltransformationstep':['Fieldwork Model Transformation', 'https://github.com/mapclient-plugins/fieldworkmodeltransformationstep/archive/master.zip'],
                              'fieldworkpcmeshfittingstep':['Fieldwork PC Mesh Fitting', 'https://github.com/mapclient-plugins/fieldworkpcmeshfittingstep/archive/master.zip'],
                              'fieldworkpcregfemur2landmarksstep':['Fieldwork PC-Reg Femur 2 Landmarks', 'https://github.com/mapclient-plugins/fieldworkpcregfemur2landmarksstep/archive/master.zip'],
                              'fieldworkpcregpelvis2landmarksstep':['Fieldwork PC-Reg Pelvis 2 Landmarks', 'https://github.com/mapclient-plugins/fieldworkpcregpelvis2landmarksstep/archive/master.zip'],
                              'fittinglogentrymakerstep':['FittingLogEntryMaker', 'https://github.com/mapclient-plugins/fittinglogentrymakerstep/archive/master.zip'],
                              'giaspcsourcestep':['GIAS PC Source', 'https://github.com/mapclient-plugins/giaspcsourcestep/archive/master.zip'],
                              'landmarksjoinerstep':['Landmarks Joiner', 'https://github.com/mapclient-plugins/landmarksjoinerstep/archive/master.zip'],
                              'loadstlstep':['Load STL', 'https://github.com/mapclient-plugins/loadstlstep/archive/master.zip'],
                              'loadvrmlstep':['Load VRML', 'https://github.com/mapclient-plugins/loadvrmlstep/archive/master.zip'],
                              'matplotlibstaticplotterstep':['Static Data Plotter', 'https://github.com/mapclient-plugins/matplotlibstaticplotterstep/archive/master.zip'],
                              'mayaviviewerstep':['Mayavi 3D Model Viewer', 'https://github.com/mapclient-plugins/mayaviviewerstep/archive/master.zip'],
                              'mocapdataviewerstep':['MOCAP Data Viewer', 'https://github.com/mapclient-plugins/mocapdataviewerstep/archive/master.zip'],
                              'pelvislandmarkshjcpredictionstep':['Pelvis Landmark HJC Prediction', 'https://github.com/mapclient-plugins/pelvislandmarkshjcpredictionstep/archive/master.zip'],
                              'pointclouddictmakerstep':['points Cloud Dict Maker', 'https://github.com/mapclient-plugins/pointclouddictmakerstep/archive/master.zip'],
                              'pointwiserigidregistrationstep':['Point-wise Rigid Registration', 'https://github.com/mapclient-plugins/pointwiserigidregistrationstep/archive/master.zip'],
                              'segmentationstep':['Segmentation', 'https://github.com/mapclient-plugins/segmentationstep/archive/master.zip'],
                              'stringsource2step':['String Source 2', 'https://github.com/mapclient-plugins/stringsource2step/archive/master.zip'],
                              'textwriterstep':['TextWriter', 'https://github.com/mapclient-plugins/textwriterstep/archive/master.zip'],
                              'transformmodeltoimagespacestep':['Transform Model to Image Space', 'https://github.com/mapclient-plugins/transformmodeltoimagespacestep/archive/master.zip'],
                              'trcframeselectorstep':['TRC Frame Selector', 'https://github.com/mapclient-plugins/trcframeselectorstep/archive/master.zip'],
                              'trcsourcestep':['TRC Source', 'https://github.com/mapclient-plugins/trcsourcestep/archive/master.zip'],
                              'zincdatasourcestep':['Zinc Data Source', 'https://github.com/mapclient-plugins/zincdatasourcestep/archive/master.zip'],
                              'zincmodelsourcestep':['Zinc Model Source', 'https://github.com/mapclient-plugins/zincmodelsourcestep/archive/master.zip']}

class PluginUpdater:
    
    def __init__(self, parent=None):
        self._pluginUpdateDict = {}
        self._dependenciesUpdateDict = {}
        self._directory = ''
        self._successful_plugin_update = {'init_update_success':False, 'resources_update_success':False, 'syntax_update_success':False, 'indentation_update_sucess':False}
        self._2to3Location = self.locate2to3Script()
        
    def analyseDependencies(self, dependencies, directories):
        pass
    
    def updateInitContents(self, plugin, directory):
        if plugin in MAPCLIENT_PLUGIN_LOCATIONS:
            with open(directory, 'r') as oldInitFile:
                contents = oldInitFile.readlines()
            with open(directory, 'w') as newInitFile:
                for line in contents:
                    newInitFile.write(line)
                    if '__author__' in line:
                        newInitFile.write('__stepname__ = \'' + MAPCLIENT_PLUGIN_LOCATIONS[plugin][0] + '\'' + '\n')
                        newInitFile.write('__location__ = \'' + MAPCLIENT_PLUGIN_LOCATIONS[plugin][1] + '\'' + '\n\n')
            
        fail_init = self.checkSuccessfulInitUpdate(self._pluginUpdateDict[plugin][5])
        if not fail_init:
            logger.info('__init__.py file for ' + plugin + ' updated successfully.')
            self._successful_plugin_update['init_update_success'] = True
        else:
            logger.debug('There was a problem updating the ' + plugin + ' __init__.py file.')
            
    def checkSuccessfulInitUpdate(self, directory):
        return self.checkPluginInitContents(directory)

    def updateResourcesFile(self, plugin, directories):
        for directory in directories:
            filename = directory.split('\\')[-1]
            with open(directory, 'r') as oldResourceFile:
                contents = oldResourceFile.readlines()
            with open(directory, 'w') as newResourceFile:
                for line in contents:
                    if 'qt_resource_data = ' in line or 'qt_resource_name = ' in line or 'qt_resource_struct = ' in line:
                        line = line.split(' = ')
                        line = line[0] + ' = b' + line[1]
                    newResourceFile.write(line)
            
            fail_resource = self.checkSuccessfulResourceUpdate(directory)
            if not fail_resource:
                logger.info(filename + ' file for \'' + plugin + '\' updated successfully.')
                self._successful_plugin_update['resources_update_success'] = True
            else:
                logger.debug('There was a problem updating the \'' + plugin + '\'' + filename + ' file.')

    def checkSuccessfulResourceUpdate(self, directory):
        return self.checkResourcesFileContents(directory)
        
            
    def locatePyvenvScript(self):
        # Windows
        if os.path.isfile(os.path.join(sys.exec_prefix, 'Tools', 'scripts', 'pyvenv.py')):
            return os.path.join(sys.exec_prefix, 'Tools', 'scripts', 'pyvenv.py')
        # Linux and Mac
        elif os.path.isfile(os.path.join(sys.exec_prefix, 'bin', 'pyvenv.py')):
            return os.path.join(sys.exec_prefix, 'bin', 'pyvenv.py')
        elif os.path.isfile(os.path.join(sys.exec_prefix, 'local', 'bin', 'pyvenv.py')):
            return os.path.join(sys.exec_prefix, 'local', 'bin', 'pyvenv.py')
        else:
            return ''
        
    def locate2to3Script(self):
        # Windows
        if os.path.isfile(os.path.join(sys.exec_prefix, 'Tools', 'scripts', '2to3.py')):
            return os.path.join(sys.exec_prefix, 'Tools', 'scripts', '2to3.py')
        # Linux and Mac
        elif os.path.isfile(os.path.join(sys.exec_prefix, 'bin', '2to3.py')):
            return os.path.join(sys.exec_prefix, 'bin', '2to3.py')
        elif os.path.isfile(os.path.join(sys.exec_prefix, 'local', 'bin', '2to3.py')):
            return os.path.join(sys.exec_prefix, 'local', 'bin', '2to3.py')
        else:
            return ''
            
    def set2to3Dir(self, location):
        if location:
            self._2to3Location = location
        
    def get2to3Dir(self):
        return self._2to3Location
    
    def updateSyntax(self, plugin, directory):
        # find 2to3 for the system
        dir_2to3 = self.get2to3Dir()
        with open(os.path.join(get_log_directory(), 'syntax_update_report_' + plugin + '.log'), 'w') as file_out:
            try:
                subprocess.check_call(['python', dir_2to3, '--output-dir=' + directory, '-W', '-v', '-n', '-w', directory], stdout = file_out, stderr = file_out)
                logger.info('Syntax update for \'' + plugin + '\' successful.')
                self._successful_plugin_update['syntax_update_success'] = True
            except Exception as e:                            
                logger.warning('Syntax update for \'' + plugin + '\' unsuccessful.')
                logger.warning('Reason: ' + e)
    
    def fixTabbedIndentation(self, plugin, directories, temp_file):
        for moduleDir in directories:
            with open(moduleDir, 'r') as module:
                contents = module.readlines()
            if temp_file:
                moduleDir = moduleDir[:-3] + '_temp.py'
            with open(moduleDir, 'w') as newModule:
                for line in contents:
                    new_line = ''
                    whitespace = line[:len(line) - len(line.lstrip())]
                    if '\t' in whitespace:
                        whitespace = whitespace.replace('\t', '    ')
                    new_line += whitespace + line[len(line) - len(line.lstrip()):]
                    newModule.write(new_line)
        
        if not temp_file:            
            fail_indentation = self.checkSuccessfulIndentationUpdate(directories)
            if not fail_indentation:
                logger.info('Indentation for \'' + plugin + '\' updated successfully.')
                self._successful_plugin_update['indentation_update_sucess'] = True
            else:
                logger.debug('There was a problem updating the \'' + plugin + '\' plugin indentation.')
    
    def checkPluginInitContents(self, directory):
        with open(directory, 'r') as init_file:
            contents = init_file.read()
        if not ('__stepname__' in contents and '__location__' in contents):
            return True
        return False

    def checkResourcesUpdate(self, directory, resource_files):
        resource_updates = False
        requires_update = []
        directories = []
        for filename in resource_files:
            for dirpath, _, filenames in os.walk(directory):
                if filename + '.py' in filenames:
                    directories += [os.path.join(dirpath, filename + '.py')]
                    requires_update += [self.checkResourcesFileContents(os.path.join(dirpath, filename + '.py'))]
                    if not requires_update:
                        directories.pop()
        if True in requires_update:
            resource_updates = True
        return resource_updates, directories
        
    def checkResourcesFileContents(self, resources_path):
        with open(resources_path, 'r') as resourcesFile:
                    content = resourcesFile.readlines()
                    for line in content:
                        if 'qt_resource_data = ' in line:
                            line_content = line.split(' = ')
                            data = line_content[1]
                            if data[0] != 'b' and sys.version_info >= (3, 0):
                                return True
        return False

    def pluginUpdateDict(self, modname, update_init, update_resources, update_syntax, update_indentation, initDir, resourcesDir, tabbed_modules):
        self._pluginUpdateDict[modname] = [self._directory, update_init, update_resources, update_syntax, update_indentation, initDir, resourcesDir, tabbed_modules]
    
    def getAllModulesDirsInTree(self, directory):
        moduleDirs = []
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if '.py' == filename[-3:]:
                    moduleDirs += [os.path.join(dirpath, filename)]
        return moduleDirs
    
    def checkModuleSyntax(self, directory):
        moduleDirs = self.getAllModulesDirsInTree(directory)
        for module in moduleDirs:
            try:
                py_compile.compile(module, doraise = True)
            except Exception as e:
                if e.exc_type_name == 'SyntaxError' and sys.version_info >= (3, 0):
                    return True
        return False                
        
    def checkTabbedIndentation(self, directory):
        modules_to_update = []        
        moduleDirs = self.getAllModulesDirsInTree(directory)
        for module in moduleDirs:
            update_required = self.analyseModuleIndentation(module)
            if update_required:
                modules_to_update += [module]            
        if modules_to_update:
            return True, modules_to_update
        else:
            return False, modules_to_update
            
    def checkSuccessfulIndentationUpdate(self, directories):
        for directory in directories:
            fail_update = self.analyseModuleIndentation(directory)
            if fail_update:
                return True
        return False
            
    def analyseModuleIndentation(self, directory):
        with open(directory, 'r') as module:
                contents = module.readlines()
                for line in contents:
                    for char in line:
                        if char not in string.whitespace:
                            break
                        if char == '\t':
                            return True
        return False
        
    def deleteTempFiles(self, modules):
        for module in modules:
            module = module[:-3] + '_temp.py'
            os.remove(module)

