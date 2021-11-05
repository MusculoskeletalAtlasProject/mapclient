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

"""
Module to contain a list of definitions for things like fixed strings.
This may be used for places where a string is defined in two separate places,
for instance in a Qt ui file and here.  This is intended to make things easier to
keep the strings the same, obviously it doesn't help with the side-effects of
changing the string.
"""

# Options related strings
OPTIONS_SETTINGS_TAG = 'Options'
SHOW_STEP_NAMES = 'checkBoxShowStepNames'
DONT_CREATE_VIRTUAL_ENV = 'checkBoxDontCreateVirtualEnvironment'
PYSIDE_UIC_EXE = 'lineEditPySideUIC'
PYSIDE_RCC_EXE = 'lineEditPySideRCC'
VIRTUAL_ENV_PATH = 'lineEditVirtualEnvironmentPath'
GIT_EXE = 'lineEditGitExecutable'
VIRTUAL_ENV_SETUP_ATTEMPTED = 'venvSetupAttempted'
CHECK_TOOLS_ON_STARTUP = 'checkBoxCheckToolsOnStartup'
USE_EXTERNAL_GIT = 'checkBoxUseExternalGit'
USE_EXTERNAL_RCC = 'checkBoxUseExternalPySideRCC'
USE_EXTERNAL_UIC = 'checkBoxUseExternalPySideUIC'

WIZARD_TOOL_STRING = 'Wizard Tool'
VIRTUAL_ENVIRONMENT_STRING = 'Virtual Environment'
PMR_TOOL_STRING = 'PMR Tool'

PLUGINS_PACKAGE_NAME = 'mapclientplugins'
PLUGINS_PTH = PLUGINS_PACKAGE_NAME + '.pth'
MAIN_MODULE = '__init__'

# Options for previous locations
PREVIOUS_PW_WRITE_STEP_LOCATION = 'previous_write_step_location'
PREVIOUS_PW_ICON_LOCATION = 'previous_icon_location'

UNSET_FLAG = '<unset>'
INTERNAL_EXE = '<internal>'

INTERNAL_WORKFLOWS_DIR = 'MAPClient-Workflows'
INTERNAL_WORKFLOWS_ZIP = 'internal_workflows.zip'
INTERNAL_WORKFLOWS_AVAILABLE = 'internal_workflows_available'
INTERNAL_WORKFLOW_DIR = 'lineEditInternalWorkflowDirectory'
PREVIOUS_WORKFLOW = 'lineEditPreviousWorkflowDirectory'
AUTOLOAD_PREVIOUS_WORKFLOW = 'checkBoxAutoloadPreviousWorkflow'
FROZEN_PROVENANCE_INFO_FILE = 'provenance_info.json'
