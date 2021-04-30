"""
Created on Jul 1, 2015

@author: hsorby
"""
from PySide2 import QtCore, QtWidgets

from mapclient.view.dialogs.checkstatus.ui.ui_checkstatusdialog import Ui_CheckStatusDialog
from mapclient.core.checks import WizardToolChecks, VirtualEnvChecks, VCSChecks
from mapclient.view.syntaxhighlighter import SyntaxHighlighter
from mapclient.settings.definitions import WIZARD_TOOL_STRING, \
    VIRTUAL_ENVIRONMENT_STRING, PMR_TOOL_STRING


class CheckStatusDialog(QtWidgets.QDialog):

    def __init__(self, options, parent=None):
        super(CheckStatusDialog, self).__init__(parent)
        self._ui = Ui_CheckStatusDialog()
        self._ui.setupUi(self)
        self._ui.labelCheckTitle.setText('')

        self._highlighter = SyntaxHighlighter(self._ui.plainTextEditScreen.document())

        self._options = options
        self._wizard_tool = False
        self._venv = False
        self._vcs = False

    def showEvent(self, *args, **kwargs):
        print("running checks again.")
        QtCore.QTimer.singleShot(0, self._runChecks)
        return QtWidgets.QDialog.showEvent(self, *args, **kwargs)

    def checkedOk(self, tool):
        if tool == WIZARD_TOOL_STRING:
            return self._wizard_tool
        elif tool == VIRTUAL_ENVIRONMENT_STRING:
            return self._venv
        elif tool == PMR_TOOL_STRING:
            return self._vcs

        return False

    def _runChecks(self):
        options = self._options
        checks_venv = VirtualEnvChecks(options)
        self._venv = self._handleCheck(checks_venv, VIRTUAL_ENVIRONMENT_STRING)
        checks_wizard = WizardToolChecks(options)
        self._wizard_tool = self._handleCheck(checks_wizard, WIZARD_TOOL_STRING)
        checks_vcs = VCSChecks(options)
        self._vcs = self._handleCheck(checks_vcs, PMR_TOOL_STRING)
        self._ui.labelCheckTitle.setText('All Checks Complete')

    def _handleCheck(self, check, title):
        output = ''  # self._ui.plainTextEditScreen.document().toPlainText()
        result = check.doCheck()
        self._ui.labelCheckTitle.setText(title)
        if result:
            output += 'Success: {0}\n'.format(title)
        else:
            output += 'Failure: {0}\n'.format(title)
            output += check.report() + '\n'
        self._ui.plainTextEditScreen.appendPlainText(output)  # labelCheckOutput.setText(output)

        return result

