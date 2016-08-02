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
os.environ['ETS_TOOLKIT'] = 'qt4'
import random
import string
from PySide import QtCore, QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint

import numpy as np
from mapclientplugins.mayaviviewerstep.mayaviviewerdata import StepState
from mapclientplugins.mayaviviewerstep.widgets.configuredialog import ConfigureDialog
from mapclientplugins.mayaviviewerstep.widgets.mayaviviewerwidget import MayaviViewerWidget

# from mappluginutils.mayaviviewer
from mappluginutils.mayaviviewer.mayaviviewerobjects import MayaviViewerObjectsContainer
from mappluginutils.mayaviviewer.mayaviviewerfieldworkmodel import MayaviViewerFieldworkModel
from mappluginutils.mayaviviewer.mayaviviewergiasscan import MayaviViewerGiasScan
from mappluginutils.mayaviviewer.mayaviviewerdatapoints import MayaviViewerDataPoints
from mappluginutils.mayaviviewer import mayaviviewerfieldworkmeasurements as MVFM

class MayaviViewerStep(WorkflowStepMountPoint):
    """
    Step for displaying 3D objects using mayavi.
    """
    
    def __init__(self, location):
        super(MayaviViewerStep, self).__init__('Mayavi 3D Model Viewer', location)
        self._category = 'Visualisation'
        self._state = StepState()
        # self._icon = QtGui.QImage(':/zincmodelsource/images/zinc_model_icon.png')   # change this
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodeldict'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmeasurementdict'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#pointcloud'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#giasscandict'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#simplemeshdict'))
        self._widget = None
        self._configured = False

        self._addObjectMethods = [self._addFieldworkModels,
                                  self._addFieldworkMeasurements,
                                  self._addPointClouds,
                                  self._addImages,
                                  self._addSimplemeshes,
                                  ]
        self.objectContainer = MayaviViewerObjectsContainer()

    def configure(self):
        d = ConfigureDialog(self._state)
        d.setModal(True)
        if d.exec_():
            self._state = d.getState()
            self.serialize(self._location)
            
        self._configured = d.validate()
        if self._configured and self._configuredObserver:
            self._configuredObserver()
    
    def getIdentifier(self):
        return self._state._identifier
     
    def setIdentifier(self, identifier):
        self._state._identifier = identifier
     
    def serialize(self, location):
        configuration_file = os.path.join(location, getConfigFilename(self._state._identifier))
        s = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        s.beginGroup('state')
        s.setValue('identifier', self._state._identifier)
        s.setValue('discretisation', self._state._discretisation)
        s.setValue('displaynodes', self._state._displayNodes)
        s.setValue('renderargs', self._state._renderArgs)
        s.endGroup()
     
    def deserialize(self, location):
        configuration_file = os.path.join(location, getConfigFilename(self._state._identifier))
        s = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        s.beginGroup('state')
        self._state._identifier = s.value('identifier', '')
        self._state._discretisation = s.value('discretisation', '')
        if s.value('displaynodes', '')=='True':
            self._state._displayNodes = True
        else:
            self._state._displayNodes = False
        self._state._renderArgs = s.value('renderargs', '{}')
        s.endGroup()
        d = ConfigureDialog(self._state)
        self._configured = d.validate()
        pass
 
    def setPortData(self, index, dataIn):
        if not isinstance(dataIn, dict):
            raise TypeError, 'mayaviviewerstep expects a dictionary as input'

        self._addObjectMethods[index](dataIn)

    def execute(self):
        print 'launching MayaviViewerStep'
        # if not self._widget:
        self._widget = MayaviViewerWidget(self.objectContainer)
        self._widget._ui.closeButton.clicked.connect(self._doneExecution)
        self._widget.setModal(True)

        self._setCurrentWidget(self._widget)

    def _addFieldworkModels(self, D):
        for name, model in D.items():
            name = name+'#'+'FWModel'
            renderArgs = eval(self._state._renderArgs)
            obj = MayaviViewerFieldworkModel(name, model, [8,8], evaluator=None,
                                             renderArgs=renderArgs, fields=None,
                                             fieldName=None, PC=None)
            self.objectContainer.addObject(name, obj)

    def _addFieldworkMeasurements(self, D):
        for name, M in D.items():
            name = name+'#'+'FWMeasure'
            renderArgs = eval(self._state._renderArgs)

            # a bit hacky yea
            if 'femur' in name.lower():
                print 'ADDING MEASUREMENT', name
                obj = MVFM.MayaviViewerFemurMeasurements(name, M)
                self.objectContainer.addObject(name, obj)
        
    def _addPointClouds(self, D):
        for name, P in D.items():
            name = name+'#'+'DC'
            renderArgs = eval(self._state._renderArgs)
            obj = MayaviViewerDataPoints(name, P, renderArgs={'mode':'point', 'color':(0,1,0)})
            self.objectContainer.addObject(name, obj)
 
    def _addImages(self, D):
        for name, S in D.items():
            name = name+'#'+'IM'
            renderArgs = eval(self._state._renderArgs)
            obj = MayaviViewerGiasScan(name, S, renderArgs=renderArgs)
            self.objectContainer.addObject(name, obj)

        
    def _addSimplemeshes(self, D):
        pass
        # for name, S in D.items():
        #     renderArgs = eval(self._state._renderArgs)
        #     obj = MayaviViewerSimpleMesh(name, model, renderArgs=renderArgs)
        #     self.objectContainer.addObject(name, obj)

def getConfigFilename(identifier):
    return identifier + '.conf'

def generateIdentifier(char_set=string.ascii_uppercase + string.digits):
    return ''.join(random.sample(char_set*6,6))