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
import logging
from pkg_resources import parse_version

from PySide2 import QtCore, QtGui

from mapclient.settings import info
from mapclient.core.workflow.workflowscene import WorkflowScene
from mapclient.core.workflow.workflowsteps import WorkflowSteps, \
    WorkflowStepsFilter
from mapclient.core.workflow.workflowerror import WorkflowError
from mapclient.core.workflow.workflowrdf import serializeWorkflowAnnotation
from mapclient.settings.general import get_configuration_file, \
    DISPLAY_FULL_PATH, get_configuration

logger = logging.getLogger(__name__)

_PREVIOUS_LOCATION_STRING = 'previousLocation'


def _getWorkflowConfiguration(location):
    return QtCore.QSettings(_getWorkflowConfigurationAbsoluteFilename(location), QtCore.QSettings.IniFormat)


def _getWorkflowRequirements(location):
    return {}


def _getWorkflowRequirementsAbsoluteFilename(location):
    return os.path.join(location, info.DEFAULT_WORKFLOW_REQUIREMENTS_FILENAME)


def _getWorkflowConfigurationAbsoluteFilename(location):
    return os.path.join(location, info.DEFAULT_WORKFLOW_PROJECT_FILENAME)


def _getWorkflowMetaAbsoluteFilename(location):
    return os.path.join(location, info.DEFAULT_WORKFLOW_ANNOTATION_FILENAME)


class WorkflowManager(object):
    """
    This class manages (models?) the workflow.
    """

    def __init__(self, parent):
        self.name = 'WorkflowManager'
        self._parent = parent
#        self.widget = None
#        self.widgetIndex = -1
        self._location = ''
        self._conf_filename = None
        self._previousLocation = None
        self._saveStateIndex = 0
        self._currentStateIndex = 0

        self._title = None

        self._scene = WorkflowScene(self)
        self._steps = WorkflowSteps(self)
        self._filtered_steps = WorkflowStepsFilter()
#         self._filtered_steps = QtGui.QSortFilterProxyModel()
        self._filtered_steps.setSourceModel(self._steps)
#         self._filtered_steps.setFilterKeyColumn(-1)

    def title(self):
        self._title = info.APPLICATION_NAME
        if self._location:
            if get_configuration(DISPLAY_FULL_PATH):
                self._title = self._title + ' - ' + self._location
            else:
                self._title = self._title + ' - ' + os.path.basename(self._location)
        if self._saveStateIndex != self._currentStateIndex:
            self._title = self._title + ' *'

        return self._title

    def updateLocation(self, location):
        self._location = location
        return self._scene.updateWorkflowLocation(location)

    def setLocation(self, location):
        self._location = location

    def location(self):
        return self._location

    def setPreviousLocation(self, location):
        self._previousLocation = location

    def previousLocation(self):
        return self._previousLocation

    def scene(self):
        return self._scene

    def getStepModel(self):
        return self._steps

    def getFilteredStepModel(self):
        return self._filtered_steps

    def updateAvailableSteps(self):
        self._steps.reload()
        self._filtered_steps.sort(QtCore.Qt.AscendingOrder)

    def undoStackIndexChanged(self, index):
        self._currentStateIndex = index

    def identifierOccursCount(self, identifier):
        return self._scene.identifierOccursCount(identifier)

    def execute(self):
        self._scene.execute()

    def canExecute(self):
        return self._scene.canExecute()

    def registerDoneExecutionForAll(self, callback):
        self._scene.registerDoneExecutionForAll(callback)

    def isModified(self):
        return self._saveStateIndex != self._currentStateIndex

    def changeIdentifier(self, old_identifier, new_identifier):
        old_config = get_configuration_file(self._location, old_identifier)
        new_config = get_configuration_file(self._location, new_identifier)
        try:
            os.rename(old_config, new_config)
        except OSError:
            pass

    def _checkRequirements(self):
        requirements_file = _getWorkflowRequirementsAbsoluteFilename(self._location)

    def new(self, location):
        """
        Create a new workflow at the given location.  The location is a directory, it must exist
        it will not be created.  A file is created in the directory at 'location' which holds
        information describing the workflow.
        """
        if location is None:
            raise WorkflowError('No location given to create new Workflow.')

        if not os.path.exists(location):
            raise WorkflowError('Location %s does not exist.' % location)

        self._location = location
        wf = _getWorkflowConfiguration(location)
        wf.setValue('version', info.VERSION_STRING)
        self._scene.clear()

    def exists(self, location):
        """
        Determines whether a workflow exists in the given location.
        Returns True if a valid workflow exists, False otherwise.
        """
        if location is None:
            return False

        if not os.path.exists(location):
            return False

        wf = _getWorkflowConfiguration(location)
        if wf.contains('version'):
            return True

        return False

    def load(self, location):
        """
        Open a workflow from the given location.
        :param location:
        """
        if location is None:
            raise WorkflowError('No location given to open Workflow.')

        if not os.path.exists(location):
            raise WorkflowError('Given location %s does not exist' % location)

        if os.path.isfile(location):
            location = os.path.dirname(location)

        wf = _getWorkflowConfiguration(location)
        if not wf.contains('version'):
            raise WorkflowError('The given Workflow configuration file is not valid.')

        workflow_version = versionTuple(wf.value('version'))
        application_version = versionTuple(info.VERSION_STRING)
        if not compatibleVersions(workflow_version, application_version):
            pass  # should already have thrown an exception

        self._location = location
        if self._scene.isLoadable(wf):
            self._scene.loadState(wf)
        else:
            report = self._scene.doStepReport(wf)
            new_packages = False
            not_found = []
            for name in report:
                reason = report[name]
                if reason.startswith('Not Found'):
                    not_found.append(name)
                    logger.warning('Workflow not loadable due to missing plugin "{0}"'.format(name))
                elif reason.startswith('Broken'):
                    not_found.append(name)
                    logger.warning('Workflow not loadable due to broken plugin "{0}"'.format(name))
                elif reason.startswith('Found'):
                    pass
                else:
                    new_packages = True
                    self._parent.installPackage(reason)

            if self._scene.isLoadable(wf):
                self._scene.loadState(wf)
            elif new_packages:
                logger.warning('Unable to load workflow.  You may need to restart the application.')
                raise WorkflowError('The given Workflow configuration file was not loaded. '
                                    'You may need to restart the application to pick up newly installed Python modules')
            else:
                error_text = 'The given Workflow configuration file was not loaded. ' \
                             'A required plugin was not found (or had an error when loading).' \
                             '  The missing plugin(s) are: \n'
                for nf in not_found:
                    error_text += '\n    {0}'.format(nf)
                raise WorkflowError(error_text)

        self._saveStateIndex = self._currentStateIndex = 0

    def save(self):
        wf = _getWorkflowConfiguration(self._location)

        if 'version' not in wf.allKeys():
            wf.setValue('version', info.VERSION_STRING)
        workflow_version = versionTuple(wf.value('version'))
        application_version = versionTuple(info.VERSION_STRING)
        if workflow_version != application_version:
            wf.setValue('version', info.VERSION_STRING)

        self._scene.saveState(wf)
        self._saveStateIndex = self._currentStateIndex
        af = _getWorkflowMetaAbsoluteFilename(self._location)

        try:
            annotation = serializeWorkflowAnnotation().decode('utf-8')
        except AttributeError:
            annotation = serializeWorkflowAnnotation()

        with open(af, 'w') as f:
            f.write(annotation)
            self._scene.saveAnnotation(f)

#        self._title = info.APPLICATION_NAME + ' - ' + self._location

    def close(self):
        """
        Close the current workflow
        """
        self._location = ''
        self._saveStateIndex = self._currentStateIndex = 0
#        self._title = info.APPLICATION_NAME

    def isWorkflowOpen(self):
        return True  # not self._location == None

    def isWorkflowTracked(self):
        markers = ['.git', '.hg']
        for marker in markers:
            target = os.path.join(self._location, marker)
            logger.debug('checking isdir: %s', target)
            return os.path.isdir(target)
        return False

    def writeSettings(self, settings):
        settings.beginGroup(self.name)
        settings.setValue(_PREVIOUS_LOCATION_STRING, self._previousLocation)
        settings.endGroup()

    def readSettings(self, settings):
        settings.beginGroup(self.name)
        self._previousLocation = settings.value(_PREVIOUS_LOCATION_STRING, '')
        settings.endGroup()


def versionTuple(v):
    return tuple(map(int, (v.split("."))))


def compatibleVersions(workflow_version, application_version):
    """
    Method checks whether two versions are compatible or not.  Raises a
    WorkflowError exception if the two versions are not compatible.
    True if they are and False otherwise.
    The inputs are expected to be tuples of the version number:
    (major, minor, patch)
    """

    # Start with database of known compatible versions then check for
    # standard problems.
    if application_version == (0, 12, 0) and workflow_version == (0, 11, 3):
        return True

    if application_version == (0, 13, 0) and workflow_version == (0, 11, 3):
        return True

    if application_version == (0, 13, 0) and workflow_version == (0, 12, 0):
        return True

    if application_version == (0, 14, 0) and workflow_version == (0, 11, 3):
        return True

    if application_version == (0, 14, 0) and workflow_version == (0, 12, 0):
        return True

    if application_version == (0, 14, 0) and workflow_version == (0, 13, 0):
        return True

    # if not workflow_version[0:2] == application_version[0:2]:
    #     # compare first two elements of version (major, minor)
    #     raise WorkflowError(
    #         'Major/Minor version number mismatch - '
    #         'workflow version: %s; application version: %s.' %
    #             (workflow_version, application_version)
    #     )

    if not parse_version('.'.join(map(str,workflow_version))) <=\
       parse_version('.'.join(map(str,application_version))):
        raise WorkflowError(
            'Workflow version is newer than MAP Client - '
            'workflow version: %s; application version: %s.' %
                (workflow_version, application_version)
        )

    return True


