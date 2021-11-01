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
import sys

from mapclient.core import pluginframework
from mapclient.core.annotations import USES_ANNOTATIONS, PROVIDES_ANNOTATIONS, PORT_ANNOTATION, USES_ANNOTATION, PROVIDES_ANNOTATION, PROVIDES_LIST_OF_ANNOTATION, \
    USES_LIST_OF_ANNOTATION


class WorkflowStepPort(object):
    """
    Describes the location and properties of a port for a workflow step.
    """
    def __init__(self):
        self.subj = {}
        self.pred = {}
        self.obj = {}

    def addProperty(self, rdftriple):
        if rdftriple[0] in self.subj:
            self.subj[rdftriple[0]].append(rdftriple)
        else:
            self.subj[rdftriple[0]] = [rdftriple]

        if rdftriple[1] in self.pred:
            self.pred[rdftriple[1]].append(rdftriple)
        else:
            self.pred[rdftriple[1]] = [rdftriple]

        if rdftriple[2] in self.obj:
            self.obj[rdftriple[2]].append(rdftriple)
        else:
            self.obj[rdftriple[2]] = [rdftriple]

    def getTriplesForObj(self, obj):
        if obj in self.obj:
            return self.obj[obj]

        return []
#        return [triple[2] for triple in self.obj[obj]]

    def hasUses(self):
        for uses_annotation in USES_ANNOTATIONS:
            if uses_annotation in self.pred:
                return True

        return False

    def hasProvides(self):
        for provides_annotation in PROVIDES_ANNOTATIONS:
            if provides_annotation in self.pred:
                return True

        return False

    def getTriplesForPred(self, pred):
        if pred in self.pred:
            return self.pred[pred]

        return []

    def index(self):
        index = -1
        if 'http://physiomeproject.org/workflow/1.0/rdf-schema#index' in self.pred:
            indexList = self.pred['http://physiomeproject.org/workflow/1.0/rdf-schema#index']
            index = indexList[0][2]

        return index

    def _test_for_possible_connection(self, mineProvides, theirsUses):
        for mine in mineProvides:
            for theirs in theirsUses:
                if mine[2] == theirs[2]:
                    return True

        return False

    def canConnect(self, other):
        if PORT_ANNOTATION in self.subj and PORT_ANNOTATION in other.subj:
            myPorts = self.subj[PORT_ANNOTATION]
            theirPorts = other.subj[PORT_ANNOTATION]

            mineProvides = [triple for triple in myPorts if PROVIDES_ANNOTATION == triple[1]]
            theirsUses = [triple for triple in theirPorts if USES_ANNOTATION == triple[1]]
            if self._test_for_possible_connection(mineProvides, theirsUses):
                return True

            mineProvides = [triple for triple in myPorts if PROVIDES_LIST_OF_ANNOTATION == triple[1]]
            theirsUses = [triple for triple in theirPorts if USES_LIST_OF_ANNOTATION == triple[1]]
            if self._test_for_possible_connection(mineProvides, theirsUses):
                return True

        return False


"""
Plugins can inherit this mount point to add a workflow step.

A plugin that registers this mount point must:
  - Pass the name of the step into the base class on init.
  - Implement a function 'configure(self)'
  - Implement a function 'setIdentifier(self, identifier)'
  - Implement a function 'getIdentifier(self)'
  - Implement a function 'string serialize(self)'
  - Implement a function 'deserialize(self, string)'


A plugin that registers this mount point could have:
  - An attribute _icon that is a QImage icon for a visual representation of the step
  - An attribute _category that is a string representation of the step's category
  
"""


def _workflow_step_init(self, name, location, parent=None):
    self._parent = parent
    self._name = name
    self._location = location
    self._main_window = None
    self._category = 'General'
    self._ports = []
    self._icon = None
    self._configured = False
    self._configuredObserver = None
    self._doneExecution = None
    self._setCurrentWidget = None
    self._identifierOccursCount = None


def _workflow_step_setLocation(self, location):
    self._location = location


def _workflow_step_getLocation(self):
    return self._location


def _workflow_step_execute(self, dataIn=None):
    self._doneExecution()


def _workflow_step_getPortData(self, index):
    return None


def _workflow_step_setPortData(self, index, dataIn):
    pass


def _workflow_step_setMainWindow(self, main_window):
    self._main_window = main_window


def _workflow_step_get_source_uri(self):
    if hasattr(self, '__module__'):
        module = self.__module__
        module_sep = module.split('.')
        module_sep = module_sep[:2]
        package = '.'.join(module_sep)
        import importlib
        p = importlib.import_module(package)
        if hasattr(p, '__location__'):
            return p.__location__

    return None


def _workflow_step_registerDoneExecution(self, observer):
    self._doneExecution = observer


def _workflow_step_registerOnExecuteEntry(self, observer, setCurrentUndoRedoStackObserver=None):
    self._setCurrentWidget = observer
    self._setCurrentUndoRedoStack = setCurrentUndoRedoStackObserver


def _workflow_step_registerConfiguredObserver(self, observer):
    self._configuredObserver = observer


def _workflow_step_registerIdentifierOccursCount(self, observer):
    self._identifierOccursCount = observer


def _workflow_step_configure(self, location):
    raise NotImplementedError


def _workflow_step_getIdentifier(self):
    raise NotImplementedError


def _workflow_step_setIdentifier(self):
    raise NotImplementedError


def _workflow_step_serialize(self):
    raise NotImplementedError


def _workflow_step_deserialize(self, string):
    raise NotImplementedError


def _workflow_step_isConfigured(self):
    return self._configured


def _workflow_step_addPort(self, triple):
    port = WorkflowStepPort()
    if isinstance(triple, list):
        for t in triple:
            port.addProperty(t)
    else:
        port.addProperty(triple)
    port.addProperty(('http://physiomeproject.org/workflow/1.0/rdf-schema#port', 'http://physiomeproject.org/workflow/1.0/rdf-schema#index', len(self._ports)))
    self._ports.append(port)


def _workflow_step_getName(self):
    if hasattr(self, '_name'):
        return self._name

    return self.__class__.__name__


def _workflow_step_get_icon(self):
    return self._icon


attr_dict = {}
attr_dict['__init__'] = _workflow_step_init
attr_dict['setLocation'] = _workflow_step_setLocation
attr_dict['getLocation'] = _workflow_step_getLocation
attr_dict['execute'] = _workflow_step_execute
attr_dict['getPortData'] = _workflow_step_getPortData
attr_dict['setPortData'] = _workflow_step_setPortData
attr_dict['setMainWindow'] = _workflow_step_setMainWindow
attr_dict['registerDoneExecution'] = _workflow_step_registerDoneExecution
attr_dict['registerOnExecuteEntry'] = _workflow_step_registerOnExecuteEntry
attr_dict['configure'] = _workflow_step_configure
attr_dict['isConfigured'] = _workflow_step_isConfigured
attr_dict['registerIdentifierOccursCount'] = _workflow_step_registerIdentifierOccursCount
attr_dict['registerConfiguredObserver'] = _workflow_step_registerConfiguredObserver
attr_dict['addPort'] = _workflow_step_addPort
attr_dict['getName'] = _workflow_step_getName
attr_dict['deserialize'] = _workflow_step_deserialize
attr_dict['serialize'] = _workflow_step_serialize
attr_dict['getSourceURI'] = _workflow_step_get_source_uri
attr_dict['getIcon'] = _workflow_step_get_icon

WorkflowStepMountPoint = pluginframework.MetaPluginMountPoint('WorkflowStepMountPoint', (object,), attr_dict)


def workflowStepFactory(step_name, location):
    for step in WorkflowStepMountPoint.getPlugins(location):
        if step_name == step.getName():
            return step

    raise ValueError('Failed to find/create a step named: ' + step_name)


def removeWorkflowStep(step_module):
    """
    takes a module name (as a string) and removes all references
     - from sys.modules
     - from WorkflowStepMountPoint class
    """
    for key in list(sys.modules.keys()):
        if step_module in key:
            del sys.modules[key]

    for cls in WorkflowStepMountPoint.plugins[:]:
        if cls and step_module in cls.__module__:
            index = WorkflowStepMountPoint.plugins.index(cls)
            WorkflowStepMountPoint.plugins.pop(index)
