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
import datetime
import logging
import os

from mapclient.core.utils import qt_tool_wrapper
from mapclient.settings import info
from mapclient.settings.definitions import PYSIDE_UIC_EXE, PYSIDE_RCC_EXE, USE_EXTERNAL_UIC, USE_EXTERNAL_RCC
from mapclient.tools.pluginwizard.skeletonstrings import (
    APACHE_LICENSE,
    CLASS_STRING,
    CONFIGURE_DIALOG_ACCEPT_METHOD,
    CONFIGURE_DIALOG_DEFAULT_VALIDATE_METHOD,
    CONFIGURE_DIALOG_IDENTIFIER_VALIDATE_METHOD,
    CONFIGURE_DIALOG_INIT_ADDITIONS,
    CONFIGURE_DIALOG_LINE,
    CONFIGURE_DIALOG_MAKE_CONNECTIONS_METHOD,
    CONFIGURE_DIALOG_STRING,
    CONFIGURE_DIALOG_UI,
    CONFIGURE_METHOD_STRING,
    DESERIALIZE_DEFAULT_CONTENT_STRING,
    DESERIALIZE_IDENTIFIER_CONTENT_STRING,
    GETIDENTIFIER_DEFAULT_CONTENT_STRING,
    GETIDENTIFIER_IDENTIFER_CONTENT_STRING,
    IDENTIFIER_METHOD_STRING,
    IMPORT_STRING,
    INIT_METHOD_STRING,
    NAMESPACE_INIT,
    README_TEMPLATE,
    RESOURCE_FILE_STRING,
    SERIALIZE_DEFAULT_CONTENT_STRING,
    SERIALIZE_IDENTIFIER_CONTENT_STRING,
    SERIALIZE_METHOD_STRING,
    SETIDENTIFIER_DEFAULT_CONTENT_STRING,
    SETIDENTIFIER_IDENTIFER_CONTENT_STRING,
    SETUP_PY_TEMPLATE,
    STEP_PACKAGE_INIT_STRING,
)

logger = logging.getLogger(__name__)

QT_RESOURCE_FILENAME = 'resources.qrc'
PYTHON_QT_RESOURCE_FILENAME = 'resources_rc.py'
IMAGES_DIRECTORY = 'images'
CONFIG_DIALOG_FILE = 'configuredialog.py'
QT_CONFDIALOG_UI_FILENAME = 'configuredialog.ui'
PYTHON_QT_CONFDIALOG_UI_FILENAME = 'ui_configuredialog.py'

PLUGIN_NAMESPACE = 'mapclientplugins'


class Skeleton(object):
    """
    This class uses the skeleton options to write the
    skeleton code to disk.
    """

    def __init__(self, options, qt_tool_options):
        self._options = options
        self._qt_tool_options = qt_tool_options

    def _writeSetup(self, target_dir):
        """
        Write the setup file, for integration with setuptools.
        """
        target_file = os.path.join(target_dir, 'setup.py')
        with open(target_file, 'w') as f:
            f.write(SETUP_PY_TEMPLATE % dict(
                description='',
                name=self._options.getFullPackageName(),
                package_name=self._options.getPackageName(),
                author=self._options.getAuthorName(),
                author_email='',
                url='',
                plugin_namespace=PLUGIN_NAMESPACE,
                namespace_packages=[PLUGIN_NAMESPACE],
            ))

        readme_file = os.path.join(target_dir, 'README.rst')
        requirements_file = os.path.join(target_dir, 'requirements.txt')
        license_file = os.path.join(target_dir, 'LICENSE')
        with open(readme_file, 'w') as f:
            step_name = self._options.getName()  # .decode('utf-8')
            f.write(README_TEMPLATE.format(
                name=step_name,
                underline='=' * len(step_name)
            ))
        with open(requirements_file, 'w'):
            pass
        with open(license_file, 'w') as f:
            now = datetime.datetime.now()
            f.write(APACHE_LICENSE.format(yyyy=now.year,
                                          name_of_copyright_owner=self._options.getAuthorName()))

    @staticmethod
    def _writeNamespaceInit(target_dir):
        """
        Write the namespace declaration init file.
        """
        target_file = os.path.join(target_dir, '__init__.py')
        f = open(target_file, 'w')
        f.write(NAMESPACE_INIT)
        f.close()

    @staticmethod
    def _generateExecuteMethod():
        method_string = """
    def execute(self):
        \"\"\"
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        \"\"\"
        # Put your execute step code here before calling the '_doneExecution' method.
        self._doneExecution()
"""

        return method_string

    @staticmethod
    def _generateSetPortDataMethod(ports):
        """
        Generates the set port data method string.  Returns an empty
        string if this step has no uses ports.
        """
        method_string = ''
        uses_total = 0
        for current_port in ports:
            if current_port[0].endswith('uses'):
                uses_total += 1

        if uses_total > 0:
            method_string += """
    def setPortData(self, index, dataIn):
        \"\"\"
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.

        :param index: Index of the port to return.
        :param dataIn: The data to set for the port at the given index.
        \"\"\"
"""
            uses_count = 0
            for index, current_port in enumerate(ports):
                if current_port[0].endswith('uses'):
                    uses_count += 1
                    if uses_total == 1:
                        method_string += '        self._portData{0} = dataIn # {1}\n'.format(index, current_port[1])
                    else:
                        if uses_count == 1:
                            method_string += """        if index == {0}:
            self._portData{0} = dataIn # {1}
""".format(index, current_port[1])
                        else:
                            method_string += """        elif index == {0}:
            self._portData{0} = dataIn # {1}
""".format(index, current_port[1])

        return method_string

    @staticmethod
    def _generateGetPortDataMethod(ports):
        """
        Generate the get port data method string.  Returns the empty
        string if this step has no provides ports.
        """
        method_string = ''
        provides_total = 0
        for current_port in ports:
            if current_port[0].endswith('provides'):
                provides_total += 1

        if provides_total > 0:
            method_string += """
    def getPortData(self, index):
        \"\"\"
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.

        :param index: Index of the port to return.
        \"\"\"
"""
            provides_count = 0
            for index, current_port in enumerate(ports):
                if current_port[0].endswith('provides'):
                    provides_count += 1
                    if provides_total == 1:
                        method_string += '        return self._portData{0} # {1}\n'.format(index, current_port[1])
                    else:
                        if provides_count == 1:
                            method_string += """        if index == {0}:
            return self._portData{0} # {1}
""".format(index, current_port[1])
                        else:
                            method_string += """        elif index == {0}:
            return self._portData{0} # {1}
""".format(index, current_port[1])

        return method_string

    def _generateConfigureMethod(self):
        method_string = CONFIGURE_METHOD_STRING
        if self._options.configCount() > 0:
            method_string += """        dlg = ConfigureDialog(self._main_window)
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()
"""
        else:
            method_string += '        pass\n'

        return method_string

    def _generateImportStatements(self):
        qtgui_import = ''
        json_import = ''
        icon = self._options.getIcon()
        if icon:
            qtgui_import = 'from PySide2 import QtGui\n\n'
        if self._options.configCount() > 0:
            json_import = 'import json\n\n'

        import_string = IMPORT_STRING.format(json_import=json_import, qtgui_import=qtgui_import)
        import_string += 'from mapclientplugins.{package_name}.configuredialog import ConfigureDialog\n'.format(package_name=self._options.getPackageName())

        return import_string

    def _writeStep(self, step_dir):
        """
        Write the step file subject to the options set in the __init__ method.
        """
        object_name = self._options.getName().replace(' ', '')
        init_string = INIT_METHOD_STRING.format(step_object_name=object_name, step_name=self._options.getName(), step_category=self._options.getCategory())
        icon = self._options.getIcon()
        if icon:
            image_filename = self._options.getImageFile()
            icon_string = '        self._icon =  QtGui.QImage(\':/{step_package_name}/' + IMAGES_DIRECTORY + '/{image_filename}\')\n'
            init_string += icon_string.format(step_package_name=self._options.getPackageName(), image_filename=image_filename)
        port_index = 0
        ports = []
        init_string += """        # Ports:
"""
        while port_index < self._options.portCount():
            current_port = self._options.getPort(port_index)
            init_string += """        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      '{0}',
                      '{1}'))\n""".format(current_port[0], current_port[1])
            port_index += 1
            ports.append(current_port)

        init_string += '        # Port data:\n'
        for index, current_port in enumerate(ports):
            init_string += '        self._portData{0} = None # {1}\n'.format(index, current_port[1])

        if self._options.hasIdentifierConfig():
            id_method_string = IDENTIFIER_METHOD_STRING.format(getidentifiercontent=GETIDENTIFIER_IDENTIFER_CONTENT_STRING,
                                                               setidentifiercontent=SETIDENTIFIER_IDENTIFER_CONTENT_STRING)
        else:
            id_method_string = IDENTIFIER_METHOD_STRING.format(getidentifiercontent=GETIDENTIFIER_DEFAULT_CONTENT_STRING.format(step_object_name=object_name),
                                                               setidentifiercontent=SETIDENTIFIER_DEFAULT_CONTENT_STRING)

        if self._options.configCount() > 0:
            init_string += '        # Config:\n'
            init_string += '        self._config = {}\n'
            config_index = 0
            while config_index < self._options.configCount():
                config = self._options.getConfig(config_index)
                init_string += '        self._config[\'{0}\'] = \'{1}\'\n'.format(config[0], config[1])
                config_index += 1

            # init_string += '\n'

        if self._options.hasIdentifierConfig():
            serialize_method_string = SERIALIZE_METHOD_STRING.format(serializecontent=SERIALIZE_IDENTIFIER_CONTENT_STRING, deserializecontent=DESERIALIZE_IDENTIFIER_CONTENT_STRING)
        else:
            serialize_method_string = SERIALIZE_METHOD_STRING.format(serializecontent=SERIALIZE_DEFAULT_CONTENT_STRING, deserializecontent=DESERIALIZE_DEFAULT_CONTENT_STRING)

        step_file = os.path.join(step_dir, 'step.py')
        with open(step_file, 'w') as f:
            f.write(self._generateImportStatements())
            f.write(CLASS_STRING.format(step_object_name=object_name, step_name=self._options.getName()))
            f.write(init_string)
            f.write(self._generateExecuteMethod())
            f.write(self._generateSetPortDataMethod(ports))
            f.write(self._generateGetPortDataMethod(ports))
            f.write(self._generateConfigureMethod())
            f.write(id_method_string)
            f.write(serialize_method_string)

    def _writeStepPackageInit(self, init_dir):
        """
        Write the step package __init__ file.  If a resource file
        is present then load the module in here. Displays the author name,
        plugin name and plugin location.
        """
        init_file = os.path.join(init_dir, '__init__.py')
        f = open(init_file, 'w')
        f.write(STEP_PACKAGE_INIT_STRING.format(
            step_name=self._options.getName(),
            package_name=self._options.getFullPackageName(),
            author_name=self._options.getAuthorName(),
            plugin_location=self._options.getPluginLocation(),
            version=info.VERSION_STRING)
        )
        icon = self._options.getIcon()
        if icon:
            (package, _) = os.path.splitext(PYTHON_QT_RESOURCE_FILENAME)
            f.write('# Import the resource file when the module is loaded,\n')
            f.write('# this enables the framework to use the step icon.\n')
            f.write('from . import ' + package)
        f.close()

    def _createStepIcon(self, step_dir):
        """
        The step icon requires the creation of directories, resources
        and files if an image file has been specified.

        The image file in the options is assumed to exist.
        """
        icon = self._options.getIcon()
        if icon:
            # Create directories
            qt_dir = os.path.join(step_dir, 'qt')
            if not os.path.exists(qt_dir):
                os.mkdir(qt_dir)
            images_dir = os.path.join(qt_dir, IMAGES_DIRECTORY)
            if not os.path.exists(images_dir):
                os.mkdir(images_dir)

            image_filename = self._options.getImageFile()
            # Copy image file
            icon.save(os.path.join(images_dir, image_filename))

            resource_file = os.path.join(qt_dir, QT_RESOURCE_FILENAME)
            with open(resource_file, 'w') as f:
                f.write(RESOURCE_FILE_STRING.format(step_package_name=self._options.getPackageName(),
                                                    image_filename=image_filename))

            py_file = os.path.join(step_dir, PYTHON_QT_RESOURCE_FILENAME)
            if self._qt_tool_options[USE_EXTERNAL_RCC]:
                return_code, msg = qt_tool_wrapper(self._qt_tool_options[PYSIDE_RCC_EXE], ['-g', 'python', '-o', py_file, resource_file], True)
            else:
                return_code, msg = qt_tool_wrapper("rcc", ['-g', 'python', '-o', py_file, resource_file])

            if return_code != 0:
                raise Exception('Error: {}\nFailed to generate Python resource file using the PySide resource compiler.'.format(msg))

    def _createConfigDialog(self, step_dir):
        """
        The Config dialog requires the existence of the qt directory in the
        step directory.

        Assume the program pyside-uic is available from the shell.
        """
        config_count = self._options.configCount()
        if config_count > 0:
            qt_dir = os.path.join(step_dir, 'qt')
            if not os.path.exists(qt_dir):
                os.mkdir(qt_dir)

            widgets_string = ''
            set_config_string = """
    def setConfig(self, config):
        \"\"\"
        Set the current value of the configuration for the dialog.{additional_comment}
        \"\"\"{previous_identifier}
"""
            get_config_string = """
    def getConfig(self):
        \"\"\"
        Get the current value of the configuration from the dialog.{additional_comment}
        \"\"\"{previous_identifier}
        config = {{}}
"""
            if self._options.hasIdentifierConfig():
                set_config_string = set_config_string.format(
                    additional_comment='  Also\n'
                                       '        set the _previousIdentifier value so that we can check uniqueness of the\n'
                                       '        identifier over the whole of the workflow.',
                    previous_identifier='\n        self._previousIdentifier = config[\'identifier\']')
                get_config_string = get_config_string.format(
                    additional_comment='  Also\n'
                                       '        set the _previousIdentifier value so that we can check uniqueness of the\n'
                                       '        identifier over the whole of the workflow.',
                    previous_identifier='\n        self._previousIdentifier = self._ui.lineEdit0.text()')
            else:
                set_config_string = set_config_string.format(additional_comment='', previous_identifier='')
                get_config_string = get_config_string.format(additional_comment='', previous_identifier='')

            row_index = 0
            while row_index < self._options.configCount():
                label = self._options.getConfig(row_index)[0]
                widgets_string += CONFIGURE_DIALOG_LINE.format(row=row_index, label=label + ':  ')
                config = self._options.getConfig(row_index)
                set_config_string += '        self._ui.lineEdit{0}.setText(config[\'{1}\'])\n'.format(row_index, config[0])
                get_config_string += '        config[\'{1}\'] = self._ui.lineEdit{0}.text()\n'.format(row_index, config[0])
                row_index += 1

            set_config_string += '\n'
            get_config_string += '        return config\n'

            ui_file = os.path.join(qt_dir, QT_CONFDIALOG_UI_FILENAME)
            with open(ui_file, 'w') as fui:
                fui.write(CONFIGURE_DIALOG_UI.format(widgets_string))

            py_file = os.path.join(step_dir, PYTHON_QT_CONFDIALOG_UI_FILENAME)
            if self._qt_tool_options[USE_EXTERNAL_UIC]:
                return_code, msg = qt_tool_wrapper(self._qt_tool_options[PYSIDE_UIC_EXE], ['-g', 'python', '--from-imports', '-o', py_file, ui_file], True)
            else:
                return_code, msg = qt_tool_wrapper("uic", ['-g', 'python', '--from-imports', '-o', py_file, ui_file])

            if return_code != 0:
                raise Exception('Error: {}\nFailed to generate Python resource file using the PySide resource compiler.'.format(msg))

            dialog_file = os.path.join(step_dir, CONFIG_DIALOG_FILE)
            with open(dialog_file, 'w') as f:
                f.write(CONFIGURE_DIALOG_STRING.format(package_name=self._options.getFullPackageName()))
                if self._options.hasIdentifierConfig():
                    f.write(CONFIGURE_DIALOG_INIT_ADDITIONS)
                    f.write(CONFIGURE_DIALOG_MAKE_CONNECTIONS_METHOD)
                    f.write(CONFIGURE_DIALOG_ACCEPT_METHOD)
                    f.write(CONFIGURE_DIALOG_IDENTIFIER_VALIDATE_METHOD)
                else:
                    f.write(CONFIGURE_DIALOG_DEFAULT_VALIDATE_METHOD)
                f.write(get_config_string)
                f.write(set_config_string)

    def getPackageDirectory(self):
        out_dir = self._options.getOutputDirectory()
        package_full_name = self._options.getFullPackageName()

        package_dir = os.path.join(out_dir, package_full_name)
        return package_dir

    def write(self):
        """
        Write out the step using the options set on initialisation, assumes the output
        directory is writable otherwise an exception will be raised.
        """

        out_dir = self._options.getOutputDirectory()
        package_name = self._options.getPackageName()
        package_full_name = self._options.getFullPackageName()

        package_dir = os.path.join(out_dir, package_full_name)
        namespace_dir = os.path.join(package_dir, PLUGIN_NAMESPACE)
        step_package_dir = os.path.join(namespace_dir, package_name)

        # Make directories
        os.mkdir(package_dir)
        os.mkdir(namespace_dir)
        os.mkdir(step_package_dir)

        self._writeSetup(package_dir)
        self._writeNamespaceInit(namespace_dir)

        # Write step package init file
        self._writeStepPackageInit(step_package_dir)

        # Write out the step file
        self._writeStep(step_package_dir)

        # Prepare step icon
        self._createStepIcon(step_package_dir)

        # Prepare config dialog
        self._createConfigDialog(step_package_dir)


DEFAULT_AUTHOR_NAME = 'Xxxx Yyyyy'
DEFAULT_CATEGORY = 'General'


class SkeletonOptions(object):
    """
    This class hold all the options for the skeleton plugin code.
    """

    def __init__(self):
        self._name = ''
        self._packageName = ''
        self._pluginLocation = ''
        self._imageFile = ''
        self._icon = None
        self._outputDirectory = ''
        self._ports = []
        self._configs = []
        self._identifierConfig = False
        self._category = DEFAULT_CATEGORY
        self._authorName = DEFAULT_AUTHOR_NAME

    def getName(self):
        return self._name

    def getPluginLocation(self):
        return self._pluginLocation

    def setPluginLocation(self, plugin_location):
        self._pluginLocation = plugin_location

    def setName(self, name):
        self._name = name

    def getPackageName(self):
        return self._packageName

    def setPackageName(self, package_name):
        self._packageName = package_name

    def getFullPackageName(self):
        return PLUGIN_NAMESPACE + '.' + self._packageName

    def getImageFile(self):
        return self._imageFile

    def setImageFile(self, image_file):
        self._imageFile = image_file

    def getIcon(self):
        return self._icon

    def setIcon(self, icon):
        self._icon = icon

    def getOutputDirectory(self):
        return self._outputDirectory

    def setOutputDirectory(self, output_directory):
        self._outputDirectory = output_directory

    def portCount(self):
        return len(self._ports)

    def getPort(self, index):
        return self._ports[index]

    def addPort(self, predicate, port_object):
        self._ports.append([predicate, port_object])

    def configCount(self):
        return len(self._configs)

    def getConfig(self, index):
        return self._configs[index]

    def addConfig(self, label, value):
        if label == 'identifier':
            self._identifierConfig = True
        self._configs.append([label, value])

    def hasIdentifierConfig(self):
        return self._identifierConfig

    def getAuthorName(self):
        return self._authorName

    def setAuthorName(self, author_name):
        if not author_name:
            author_name = DEFAULT_AUTHOR_NAME

        self._authorName = author_name

    def getCategory(self):
        return self._category

    def setCategory(self, category):
        if not category:
            category = DEFAULT_CATEGORY

        self._category = category
