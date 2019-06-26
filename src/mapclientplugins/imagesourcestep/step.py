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
import re
import imghdr

from PySide2 import QtWidgets, QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.imagesourcestep.widgets.configuredialog import ConfigureDialog, ConfigureDialogState

from mapclient.tools.pmr.pmrtool import PMRTool
from mapclient.tools.pmr.settings.general import PMR


def try_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [try_int(c) for c in re.split('([0-9]+)', s)]


class ImageSourceData(object):

    name = 'ImageSourceData'

    def __init__(self, identifier, location, image_type):
        self._identifier = identifier
        self._location = location
        self._image_type = image_type

    def identifier(self):
        return self._identifier

    def location(self):
        """
        Return a location relative to the workflow directory.
        :return: relative path
        """
        return self._location

    def image_files(self):
        images = []
        location = self._location
        if os.path.isdir(location):
            for item in sorted(os.listdir(location), key=alphanum_key):
                image_candidate = os.path.join(location, item)
                if imghdr.what(image_candidate):
                    images.append(image_candidate)
        elif os.path.exists(location):
            if imghdr.what(location):
                images.append(location)

        return images

    def image_type(self):
        return self._image_type


class ImageSourceStep(WorkflowStepMountPoint):
    """
    A step that satisfies the step plugin duck.
    
    It describes the location of an image/a set of images.
    It can be used as an image source.
    """
    def __init__(self, location):
        super(ImageSourceStep, self).__init__('Image Source', location)
        self._icon = QtGui.QImage(':/imagesource/icons/landscapeimages.png')
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#images'))
        self._configured = False
        self._category = 'Source'
        self._state = ConfigureDialogState()

    def configure(self):
        d = ConfigureDialog(self._state, QtWidgets.QApplication.activeWindow().current_widget())
        d.setWorkflowLocation(self._location)
        d.setModal(True)
        if d.exec_():
            self._state = d.getState()
            # When a PMR location is given we need to translate that into a
            # local path for passing into the ImageSourceData class
            local_dir = self._state.location()
            pmr_location = self._state.pmrLocation()
            if pmr_location and not len(local_dir):
                # Get login details:
                local_dir = self._location
                if not os.path.exists(local_dir):
                    os.mkdir(local_dir)

                self._state.setLocation(local_dir)
                d.setState(self._state)

            if pmr_location and os.path.exists(local_dir):
                pmr_info = PMR()
                pmr_tool = PMRTool(pmr_info)
                pmr_tool.cloneWorkspace(pmr_location, local_dir)

            self._configured = d.validate()
            if self._configuredObserver is not None:
                self._configuredObserver()

    def getIdentifier(self):
        return self._state.identifier()

    def setIdentifier(self, identifier):
        self._state.setIdentifier(identifier)

    def serialize(self):
        return self._state.serialize()

    def deserialize(self, string):
        self._state.deserialize(string)
        d = ConfigureDialog(self._state)
        d.setWorkflowLocation(self._location)
        self._configured = d.validate()

    def getPortData(self, index):
        return ImageSourceData(self._state.identifier(),
                               os.path.join(self._location, self._state.location()),
                               self._state.imageType())
