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

IMPORT_STRING = '''
\'\'\'
MAP Client Plugin Step
\'\'\'
{json_import}{qtgui_import}from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
'''

CLASS_STRING = '''

class {step_object_name}Step(WorkflowStepMountPoint):
    \'\'\'
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    \'\'\'
'''

INIT_METHOD_STRING = '''
    def __init__(self, location):
        super({step_object_name}Step, self).__init__('{step_name}', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = '{step_category}'
        # Add any other initialisation code here:
'''

CONFIGURE_METHOD_STRING = '''
    def configure(self):
        \'\'\'
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        \'\'\'
'''

IDENTIFIER_METHOD_STRING = '''
    def getIdentifier(self):
        \'\'\'
        The identifier is a string that must be unique within a workflow.
        \'\'\'
        {getidentifiercontent}

    def setIdentifier(self, identifier):
        \'\'\'
        The framework will set the identifier for this step when it is loaded.
        \'\'\'
        {setidentifiercontent}
'''

GETIDENTIFIER_DEFAULT_CONTENT_STRING = 'return \'{step_object_name}\' # TODO: The string must be replaced with the step\'s unique identifier'
SETIDENTIFIER_DEFAULT_CONTENT_STRING = 'pass # TODO: Must actually set the step\'s identifier here'
GETIDENTIFIER_IDENTIFER_CONTENT_STRING = 'return self._config[\'identifier\']'
SETIDENTIFIER_IDENTIFER_CONTENT_STRING = 'self._config[\'identifier\'] = identifier'

SERIALIZE_METHOD_STRING = '''
    def serialize(self):
        \'\'\'
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        \'\'\'
        {serializecontent}

    def deserialize(self, string):
        \'\'\'
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.
        \'\'\'
        {deserializecontent}

'''

SERIALIZE_DEFAULT_CONTENT_STRING = 'pass'
DESERIALIZE_DEFAULT_CONTENT_STRING = 'pass'
SERIALIZE_IDENTIFIER_CONTENT_STRING = '''return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)
'''

DESERIALIZE_IDENTIFIER_CONTENT_STRING = '''self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()
'''

CONFIGURE_DIALOG_STRING = '''

from PySide import QtGui
from {package_name}.ui_configuredialog import Ui_ConfigureDialog

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''

class ConfigureDialog(QtGui.QDialog):
    \'\'\'
    Configure dialog to present the user with the options to configure this step.
    \'\'\'

    def __init__(self, parent=None):
        \'\'\'
        Constructor
        \'\'\'
        QtGui.QDialog.__init__(self, parent)

        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)
'''

CONFIGURE_DIALOG_INIT_ADDITIONS = '''
        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None

        self._makeConnections()
'''

CONFIGURE_DIALOG_MAKE_CONNECTIONS_METHOD = '''
    def _makeConnections(self):
        self._ui.lineEdit0.textChanged.connect(self.validate)
'''

CONFIGURE_DIALOG_ACCEPT_METHOD = '''
    def accept(self):
        \'\'\'
        Override the accept method so that we can confirm saving an
        invalid configuration.
        \'\'\'
        result = QtGui.QMessageBox.Yes
        if not self.validate():
            result = QtGui.QMessageBox.warning(self, 'Invalid Configuration',
                'This configuration is invalid.  Unpredictable behaviour may result if you choose \\\'Yes\\\', are you sure you want to save this configuration?)',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if result == QtGui.QMessageBox.Yes:
            QtGui.QDialog.accept(self)
'''

CONFIGURE_DIALOG_DEFAULT_VALIDATE_METHOD = '''
    def validate(self):
        \'\'\'
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        \'\'\'
        return False
'''

CONFIGURE_DIALOG_IDENTIFIER_VALIDATE_METHOD = '''
    def validate(self):
        \'\'\'
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        \'\'\'
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        value = self.identifierOccursCount(self._ui.lineEdit0.text())
        valid = (value == 0) or (value == 1 and self._previousIdentifier == self._ui.lineEdit0.text())
        if valid:
            self._ui.lineEdit0.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.lineEdit0.setStyleSheet(INVALID_STYLE_SHEET)

        return valid
'''

PACKAGE_INIT_STRING = '''
\'\'\'
MAP Client Plugin
\'\'\'
__version__ = '0.1.0'
__author__ = '{author_name}'

import os, sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    # Using __file__ will not work if py2exe is used,
    # Possible problem of OSX10.6 also.
    sys.path.insert(1, current_dir)

# import class that derives itself from the step mountpoint.
from {package_name} import step

( _, tail ) = os.path.split(current_dir)
print("Plugin '{{0}}' version {{1}} by {{2}} loaded".format(tail, __version__, __author__))

'''

STEP_PACKAGE_INIT_STRING = '''
\'\'\'
MAP Client Plugin
\'\'\'

__version__ = '0.1.0'
__author__ = '{author_name}'
__stepname__ = '{step_name}'
__location__ = '{plugin_location}'

# import class that derives itself from the step mountpoint.
from {package_name} import step

'''

RESOURCE_FILE_STRING = '''
<RCC>
  <qresource prefix="{step_package_name}">
    <file>images/{image_filename}</file>
  </qresource>
</RCC>
'''


CONFIGURE_DIALOG_LINE = '''
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
'''

CONFIGURE_DIALOG_UI = '''<?xml version="1.0" encoding="UTF-8"?>
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
   <string>ConfigureDialog</string>
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
'''


SETUP_PY_TEMPLATE = """\
from setuptools import setup, find_packages
import sys, os

# The dependencies variable is used by MAP Client to
# determine if further downloads are required.  Please
# list all dependencies here.
dependencies = [] # Insert plugin dependencies here

setup(name=%(name)r,
      version=%(version)r,
      description=%(description)r,
      long_description="",
      classifiers=[],
      author=%(author)r,
      author_email=%(author_email)r,
      url=%(url)r,
      license=%(license)r,
      packages=find_packages(exclude=['ez_setup',]),
      namespace_packages=%(namespace_packages)r,
      include_package_data=True,
      zip_safe=False,
      install_requires=dependencies,
      )
"""


NAMESPACE_INIT = """\
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
"""
