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
from packaging import version

from PySide6 import QtCore

from mapclient.core.metrics import metrics_logger
from mapclient.settings import info
from mapclient.core.workflow.workflowscene import WorkflowScene
from mapclient.core.workflow.workflowsteps import WorkflowSteps, \
    WorkflowStepsFilter
from mapclient.core.workflow.workflowerror import WorkflowError
from mapclient.core.workflow.workflowrdf import serializeWorkflowAnnotation
from mapclient.settings.general import get_configuration_file, \
    DISPLAY_FULL_PATH, get_configuration, is_workflow_in_use, mark_workflow_in_use, mark_workflow_ready_for_use

logger = logging.getLogger(__name__)

_PREVIOUS_LOCATION_STRING = 'previousLocation'


def _get_workflow_configuration(location):
    return QtCore.QSettings(_get_workflow_configuration_absolute_filename(location), QtCore.QSettings.Format.IniFormat)


def _get_workflow_requirements(location):
    return {}


def _get_workflow_requirements_absolute_filename(location):
    return os.path.join(location, info.DEFAULT_WORKFLOW_REQUIREMENTS_FILENAME)


def _get_workflow_configuration_absolute_filename(location):
    return os.path.join(location, info.DEFAULT_WORKFLOW_PROJECT_FILENAME)


def _get_workflow_meta_absolute_filename(location):
    return os.path.join(location, info.DEFAULT_WORKFLOW_ANNOTATION_FILENAME)


class WorkflowManager(object):
    """
    This class manages (models?) the workflow.
    """

    def __init__(self, parent):
        self.name = 'WorkflowManager'
        self._parent = parent
        self._location = ''
        self._conf_filename = None
        self._previousLocation = None
        self._saveStateIndex = 0
        self._currentStateIndex = 0

        self._title = None

        self._scene = WorkflowScene(self)
        self._steps = WorkflowSteps(self)
        self._filtered_steps = WorkflowStepsFilter()
        self._filtered_steps.setSourceModel(self._steps)

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

    def set_location(self, location):
        self._location = location
        return self._scene.updateWorkflowLocation(location)

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
        self._filtered_steps.sort(1, QtCore.Qt.SortOrder.AscendingOrder)

    def undoStackIndexChanged(self, index):
        self._currentStateIndex = index

    def identifierOccursCount(self, identifier):
        return self._scene.identifierOccursCount(identifier)

    def register_finished_workflow_callback(self, callback):
        self._scene.register_finished_workflow_callback(callback)

    def execute(self):
        metrics_logger.workflow_executed(self.title())
        self._scene.execute()

    def abort_execution(self):
        self._scene.abort_execution()

    def set_workflow_direction(self, direction):
        self._scene.set_workflow_direction(direction)

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

    def _check_requirements(self):
        requirements_file = _get_workflow_requirements_absolute_filename(self._location)

    @staticmethod
    def _check_workflow_location(location, new=False):
        if location is None:
            raise WorkflowError('No location given to create new Workflow.')

        if not os.path.exists(location):
            raise WorkflowError(f'Location {location} does not exist.')

        if not os.path.isdir(location):
            raise WorkflowError(f'Location {location} is not a directory.')

        wf = _get_workflow_configuration(location)
        if wf.contains('version'):
            workflow_version = wf.value('version')
            if version.parse(workflow_version) > version.parse('0.20.0'):
                if wf.value('id') != info.DEFAULT_WORKFLOW_PROJECT_IDENTIFIER:
                    raise WorkflowError(f'Location {location} does not have a valid workflow configuration file.')
        else:
            if not new:
                raise WorkflowError(f'Location {location} does not have a valid workflow configuration file.')

    def load_workflow_virtually(self, location):
        self._check_workflow_location(location)

        return _get_workflow_configuration(location)

    @staticmethod
    def create_empty_workflow(location):
        wf = _get_workflow_configuration(location)
        wf.setValue('version', info.VERSION_STRING)
        wf.setValue('id', info.DEFAULT_WORKFLOW_PROJECT_IDENTIFIER)
        return wf

    def new(self, location):
        """
        Create a new workflow at the given location.  The location is a directory, it must exist
        it will not be created.  A file is created in the directory at 'location' which holds
        information describing the workflow.
        """
        self._check_workflow_location(location, new=True)
        self.set_location(location)
        self.create_empty_workflow(location)
        self._scene.clear()

    def exists(self, location):
        """
        Determines whether a workflow exists in the given location.
        Returns True if a valid workflow exists, False otherwise.
        """
        try:
            self._check_workflow_location(location)
        except WorkflowError:
            return False

        return True

    @staticmethod
    def is_restricted(location):
        try:
            WorkflowManager._check_workflow_location(location)
        except WorkflowError:
            return False

        return is_workflow_in_use(location)

    def load(self, location, scene_rect=QtCore.QRectF(0, 0, 640, 480)):
        """
        Open a workflow from the given location.
        :param location:
        :param scene_rect: Rectangle of the scene rect to load the workflow into.
        """
        if os.path.isfile(location):
            location = os.path.dirname(location)

        self._check_workflow_location(location)

        wf = _get_workflow_configuration(location)

        workflow_version = version.parse(wf.value('version'))
        application_version = version.parse(info.VERSION_STRING)
        if not _compatible_versions(workflow_version, application_version):
            pass  # should already have thrown an exception

        self.set_location(location)
        if self._scene.is_loadable(wf):
            if mark_workflow_in_use(location):
                self._scene.load_state(wf, scene_rect)
            else:
                logger.warning('Workflow is already in use.')
                raise WorkflowError('Workflow is already in use.')
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

            if self._scene.is_loadable(wf):
                if mark_workflow_in_use(location):
                    self._scene.load_state(wf, scene_rect)
                else:
                    logger.warning('Workflow is already in use.')
                    raise WorkflowError('Workflow is already in use.')
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
        wf = _get_workflow_configuration(self._location)

        if 'version' not in wf.allKeys():
            wf.setValue('version', info.VERSION_STRING)
        if 'id' not in wf.allKeys():
            wf.setValue('id', info.DEFAULT_WORKFLOW_PROJECT_IDENTIFIER)
        workflow_version = version.parse(wf.value('version'))
        application_version = version.parse(info.VERSION_STRING)
        if workflow_version < application_version:
            wf.setValue('version', info.VERSION_STRING)

        self._scene.saveState(wf)
        self._saveStateIndex = self._currentStateIndex
        af = _get_workflow_meta_absolute_filename(self._location)

        try:
            annotation = serializeWorkflowAnnotation().decode('utf-8')
        except AttributeError:
            annotation = serializeWorkflowAnnotation()

        with open(af, 'w') as f:
            f.write(annotation)
            self._scene.saveAnnotation(f)

    def close(self):
        """
        Close the current workflow
        """
        self.set_location('')
        mark_workflow_ready_for_use()
        self._saveStateIndex = self._currentStateIndex = 0

    def isWorkflowOpen(self):
        return True  # not self._location == None

    def isWorkflowPopulated(self):
        return self._scene.has_steps()

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


def _compatible_versions(workflow_version, application_version):
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

    if not workflow_version <= application_version:
        raise WorkflowError(
            'Workflow version is newer than MAP Client - '
            'workflow version: %s; application version: %s.' %
            (workflow_version, application_version)
        )

    return True
