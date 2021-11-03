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

IMPORT_STRING = """
\"\"\"
MAP Client Plugin Step
\"\"\"
{json_import}{qtgui_import}from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
"""

CLASS_STRING = """

class {step_object_name}Step(WorkflowStepMountPoint):
    \"\"\"
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    \"\"\"
"""

INIT_METHOD_STRING = """
    def __init__(self, location):
        super({step_object_name}Step, self).__init__('{step_name}', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = '{step_category}'
        # Add any other initialisation code here:
"""

CONFIGURE_METHOD_STRING = """
    def configure(self):
        \"\"\"
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        \"\"\"
"""

IDENTIFIER_METHOD_STRING = """
    def getIdentifier(self):
        \"\"\"
        The identifier is a string that must be unique within a workflow.
        \"\"\"
        {getidentifiercontent}

    def setIdentifier(self, identifier):
        \"\"\"
        The framework will set the identifier for this step when it is loaded.
        \"\"\"
        {setidentifiercontent}
"""

GETIDENTIFIER_DEFAULT_CONTENT_STRING = 'return \'{step_object_name}\' # TODO: The string must be replaced with the step\'s unique identifier'
SETIDENTIFIER_DEFAULT_CONTENT_STRING = 'pass # TODO: Must actually set the step\'s identifier here'
GETIDENTIFIER_IDENTIFER_CONTENT_STRING = 'return self._config[\'identifier\']'
SETIDENTIFIER_IDENTIFER_CONTENT_STRING = 'self._config[\'identifier\'] = identifier'

SERIALIZE_METHOD_STRING = """
    def serialize(self):
        \"\"\"
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        \"\"\"
        {serializecontent}

    def deserialize(self, string):
        \"\"\"
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.

        :param string: JSON representation of the configuration in a string.
        \"\"\"
        {deserializecontent}

"""

SERIALIZE_DEFAULT_CONTENT_STRING = 'pass'
DESERIALIZE_DEFAULT_CONTENT_STRING = 'pass'
SERIALIZE_IDENTIFIER_CONTENT_STRING = """return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)"""

DESERIALIZE_IDENTIFIER_CONTENT_STRING = """self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()
"""

CONFIGURE_DIALOG_STRING = """

from PySide2 import QtWidgets
from {package_name}.ui_configuredialog import Ui_ConfigureDialog

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''


class ConfigureDialog(QtWidgets.QDialog):
    \"\"\"
    Configure dialog to present the user with the options to configure this step.
    \"\"\"

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)
"""

CONFIGURE_DIALOG_INIT_ADDITIONS = """
        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._makeConnections()
"""

CONFIGURE_DIALOG_MAKE_CONNECTIONS_METHOD = """
    def _makeConnections(self):
        self._ui.lineEdit0.textChanged.connect(self.validate)
"""

CONFIGURE_DIALOG_ACCEPT_METHOD = """
    def accept(self):
        \"\"\"
        Override the accept method so that we can confirm saving an
        invalid configuration.
        \"\"\"
        result = QtWidgets.QMessageBox.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(self, 'Invalid Configuration',
                'This configuration is invalid.  Unpredictable behaviour may result if you choose \\\'Yes\\\', are you sure you want to save this configuration?)',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            QtWidgets.QDialog.accept(self)
"""

CONFIGURE_DIALOG_DEFAULT_VALIDATE_METHOD = """
    def validate(self):
        \"\"\"
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        \"\"\"
        return False
"""

CONFIGURE_DIALOG_IDENTIFIER_VALIDATE_METHOD = """
    def validate(self):
        \"\"\"
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        \"\"\"
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        value = self.identifierOccursCount(self._ui.lineEdit0.text())
        valid = (value == 0) or (value == 1 and self._previousIdentifier == self._ui.lineEdit0.text())
        if valid:
            self._ui.lineEdit0.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.lineEdit0.setStyleSheet(INVALID_STYLE_SHEET)

        return valid
"""

STEP_PACKAGE_INIT_STRING = """
\"\"\"
MAP Client Plugin - Generated from MAP Client v{version}
\"\"\"

__version__ = '0.1.0'
__author__ = '{author_name}'
__stepname__ = '{step_name}'
__location__ = '{plugin_location}'

# import class that derives itself from the step mountpoint.
from {package_name} import step

"""

RESOURCE_FILE_STRING = """
<RCC>
  <qresource prefix="{step_package_name}">
    <file>images/{image_filename}</file>
  </qresource>
</RCC>
"""


CONFIGURE_DIALOG_LINE = """
      <item row="{row}" column="0">
       <widget class="QLabel" name="label{row}">
        <property name="text">
         <string>{label}</string>
        </property>
       </widget>
      </item>
      <item row="{row}" column="1">
       <widget class="QLineEdit" name="lineEdit{row}"/>
      </item>
"""

CONFIGURE_DIALOG_UI = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>ConfigureDialog</class>
 <widget class="QDialog" name="ConfigureDialog">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>418</width>
    <height>303</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Configure Step</string>
  </property>
  <layout class="QGridLayout" name="gridLayout">
   <item row="0" column="0">
    <widget class="QGroupBox" name="configGroupBox">
     <property name="title">
      <string/>
     </property>
     <layout class="QFormLayout" name="formLayout">{0}     </layout>
    </widget>
   </item>
   <item row="1" column="0">
    <widget class="QDialogButtonBox" name="buttonBox">
     <property name="orientation">
      <enum>Qt::Horizontal</enum>
     </property>
     <property name="standardButtons">
      <set>QDialogButtonBox::Cancel|QDialogButtonBox::Ok</set>
     </property>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections>
  <connection>
   <sender>buttonBox</sender>
   <signal>accepted()</signal>
   <receiver>ConfigureDialog</receiver>
   <slot>accept()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>248</x>
     <y>254</y>
    </hint>
    <hint type="destinationlabel">
     <x>157</x>
     <y>274</y>
    </hint>
   </hints>
  </connection>
  <connection>
   <sender>buttonBox</sender>
   <signal>rejected()</signal>
   <receiver>ConfigureDialog</receiver>
   <slot>reject()</slot>
   <hints>
    <hint type="sourcelabel">
     <x>316</x>
     <y>260</y>
    </hint>
    <hint type="destinationlabel">
     <x>286</x>
     <y>274</y>
    </hint>
   </hints>
  </connection>
 </connections>
</ui>
"""


README_TEMPLATE = """\
{name}
{underline}

The {name} step is a plugin for the MAP Client application.

"""


SETUP_PY_TEMPLATE = """\
import codecs
import io
import os
import re

from setuptools import setup, find_packages

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))


def read(*parts):
    with codecs.open(os.path.join(SETUP_DIR, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\\"]([^'\\"]*)['\\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# List all of your Python package dependencies in the
# requirements.txt file


def readfile(filename, split=False):
    with io.open(filename, encoding="utf-8") as stream:
        if split:
            return stream.read().split("\\n")
        return stream.read()


readme = readfile("README.rst", split=True)[3:]  # skip title
# For requirements not hosted on PyPi place listings
# into the 'requirements.txt' file.
requires = ['PySide2']  # minimal requirements listing
source_license = readfile("LICENSE")


setup(
    name=%(name)r,
    version=find_version(%(plugin_namespace)r, %(package_name)r, '__init__.py'),
    description=%(description)r,
    long_description='\\n'.join(readme) + source_license,
    long_description_content_type='text/x-rst',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
    ],
    author=%(author)r,
    author_email=%(author_email)r,
    url=%(url)r,
    packages=find_packages(exclude=['ez_setup', ]),
    namespace_packages=%(namespace_packages)r,
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
"""


NAMESPACE_INIT = """\
__import__('pkg_resources').declare_namespace(__name__)
"""


APACHE_LICENSE = """\

   Copyright {yyyy} {name_of_copyright_owner}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
