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
import os

from PySide2 import QtGui, QtWidgets

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint

from mapclientplugins.pointcloudserializerstep.widgets.configuredialog import ConfigureDialog, ConfigureDialogState


def get_config_filename(identifier):
    return identifier + '.conf'


class PointCloudSerializerStep(WorkflowStepMountPoint):
    """
    A step satisfies the step plugin duck.
    
    It stores point cloud data.
    It can be used as a point cloud data store.
    """
    def __init__(self, location):
        super(PointCloudSerializerStep, self).__init__('Point Cloud Serializer', location)
        self._configured = True
        self._icon = QtGui.QImage(':/pointcloudserializer/images/pointcloudserializer.png')
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#pointcloud'))
        self._state = ConfigureDialogState()
        self._category = 'Sink'
        self._dataIn = None

    def configure(self):
        d = ConfigureDialog(self._state, QtWidgets.QApplication.activeWindow().current_widget())
        d.set_workflow_location(self._location)
        d.validate()

        d.setModal(True)
        if d.exec_():
            self._state = d.getState()

        self._configured = d.validate()
        if self._configured and self._configuredObserver != None:
            self._configuredObserver()

    def getIdentifier(self):
        return self._identifier

    def setIdentifier(self, identifier):
        self._identifier = identifier

    def serialize(self):
        return self._state.serialize()

    def deserialize(self, string):
        self._state.deserialize(string)
        d = ConfigureDialog(self._state)
        d.set_workflow_location(self._location)
        self._configured = d.validate()

    def setPortData(self, portId, dataIn):
        self._dataIn = dataIn

    def execute(self):
        if self._dataIn:
            if self._state._ui.checkBoxDefaultLocation.isChecked():
                output_directory = os.path.join(self._location, self._identifier)
                file_name = os.path.join(output_directory, 'pointcloud.txt')
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)

            else:
                file_name = self._state._ui.lineEditOutputLocation.text()

                if not os.path.isabs(file_name):
                    file_name = os.path.join(self._workflow_location, file_name)

            with open(file_name, 'w') as f:
                for i, pt in enumerate(self._dataIn):
                    f.write(str(i + 1) + '\t' + str(pt[0]) + '\t' + str(pt[1]) + '\t' + str(pt[2]) + '\n')

        self._doneExecution()

