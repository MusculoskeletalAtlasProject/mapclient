"""
Created on Feb 25, 2015

@author: hsorby
"""
import os.path

from PySide import QtGui

from mapclient.view.managers.options.ui.ui_optionsdialog import Ui_OptionsDialog
from mapclient.core.checks import WizardToolChecks, VirtualEnvChecks, VCSChecks
from mapclient.view.syntaxhighlighter import SyntaxHighlighter
from mapclient.settings.definitions import VIRTUAL_ENVIRONMENT_STRING, \
    WIZARD_TOOL_STRING, PMR_TOOL_STRING


class  OptionsDialog(QtGui.QDialog):
    """
    Options dialog for setting global options
    """

    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)
        self._ui = Ui_OptionsDialog()
        self._ui.setupUi(self)
        self._ui.lineEditGitExecutable.setEnabled(False)
        self._ui.pushButtonGitExecutable.setEnabled(False)

        self._createVenvMethod = None

        self._highlighter = SyntaxHighlighter(self._ui.plainTextEditToolTestOutput.document())

        self._makeConnections()

        self._venv = False
        self._wizard_tool = False
        self._vcs = False

        self._location = ''
        self._original_options = {}

    def _makeConnections(self):
        self._ui.pushButtonPySideRCC.clicked.connect(self._pySideRCCButtonClicked)
        self._ui.pushButtonPySideUIC.clicked.connect(self._pySideUICButtonClicked)
        self._ui.pushButtonVirtualEnvironmentPath.clicked.connect(self._venvPathButtonClicked)
        self._ui.pushButtonCreate.clicked.connect(self._venvCreateButtonClicked)
        self._ui.pushButtonGitExecutable.clicked.connect(self._gitExecutableButtonClicked)
        self._ui.pushButtonRunChecks.clicked.connect(self._testTools)
        self._ui.checkBoxUseExternalGit.clicked.connect(self._useExternalGitClicked)

    def _updateUi(self):
        self._ui.lineEditGitExecutable.setEnabled(self._ui.checkBoxUseExternalGit.isChecked())
        self._ui.pushButtonGitExecutable.setEnabled(self._ui.checkBoxUseExternalGit.isChecked())

    def _pySideRCCButtonClicked(self):
        rcc_program, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Select PySide Resource Compiler', dir=self._location)
        if rcc_program:
            self._ui.lineEditPySideRCC.setText(rcc_program)
            self._location = os.path.dirname(rcc_program)
            self._testTools()

    def _pySideUICButtonClicked(self):
        uic_program, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Select PySide User Interface Compiler', dir=self._location)
        if uic_program:
            self._ui.lineEditPySideUIC.setText(uic_program)
            self._location = os.path.dirname(uic_program)
            self._testTools()

    def _venvPathButtonClicked(self):
        venv_path = QtGui.QFileDialog.getExistingDirectory(self, caption='Select Virtual Environment Path', dir=self._location)
        if venv_path:
            self._ui.lineEditVirtualEnvironmentPath.setText(venv_path)
            self._location = venv_path
            self._testTools()

    def _venvCreateButtonClicked(self):
        if self._createVenvMethod is not None:
            virtualenv_path = self._ui.lineEditVirtualEnvironmentPath.text()
            if not self._createVenvMethod(virtualenv_path):
                QtGui.QMessageBox.warning("Failed to create virtual environment at '{0}'".format(virtualenv_path))

            self._testTools()

    def _useExternalGitClicked(self):
        self._updateUi()

    def setCreateVenvMethod(self, method):
        self._createVenvMethod = method

    def _gitExecutableButtonClicked(self):
        git_program, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Select Git Executable', dir=self._location)
        if git_program:
            self._ui.lineEditGitExecutable.setText(git_program)
            self._location = os.path.dirname(git_program)
            self._testTools()

    def _testToolsOld(self):
        options = self.save()
        checks_wizard = WizardToolChecks(options)
        checks_wizard.doCheck()
        checks_venv = VirtualEnvChecks(options)
        checks_venv.doCheck()
        checks_vcs = VCSChecks(options)
        checks_vcs.doCheck()
        self._ui.plainTextEditToolTestOutput.setPlainText(checks_wizard.report())
        self._ui.plainTextEditToolTestOutput.appendPlainText(checks_venv.report())
        self._ui.plainTextEditToolTestOutput.appendPlainText(checks_vcs.report())

    def _testTools(self):
        options = self.save()
        self._ui.plainTextEditToolTestOutput.setPlainText('')
        checks_venv = VirtualEnvChecks(options)
        self._venv, output = self._handleCheck(checks_venv, VIRTUAL_ENVIRONMENT_STRING)
        self._ui.plainTextEditToolTestOutput.appendPlainText(output)  # labelCheckOutput.setText(output)
        checks_wizard = WizardToolChecks(options)
        self._wizard_tool, output = self._handleCheck(checks_wizard, WIZARD_TOOL_STRING)
        self._ui.plainTextEditToolTestOutput.appendPlainText(output)  # labelCheckOutput.setText(output)
        checks_vcs = VCSChecks(options)
        self._vcs, output = self._handleCheck(checks_vcs, PMR_TOOL_STRING)
        self._ui.plainTextEditToolTestOutput.appendPlainText(output)  # labelCheckOutput.setText(output)
#         self._ui.labelCheckTitle.setText('All Checks Complete')

    def _handleCheck(self, check, title):
        output = ''  # self._ui.plainTextEditScreen.document().toPlainText()
        result = check.doCheck()
#         self._ui.labelCheckTitle.setText(title)
        if result:
            output += 'Success: {0}'.format(title)
        else:
            output += 'Failure: {0}\n'.format(title)
            output += check.report()

        return result, output

    def setCurrentTab(self, tab_index):
        self._ui.tabWidget.setCurrentIndex(tab_index)

    def reject(self, *args, **kwargs):
        self._testTools()
        return QtGui.QDialog.reject(self, *args, **kwargs)

    def accept(self, *args, **kwargs):
        self._testTools()
        return QtGui.QDialog.accept(self, *args, **kwargs)

    def checkedOk(self, tool):
        if tool == WIZARD_TOOL_STRING:
            return self._wizard_tool
        elif tool == VIRTUAL_ENVIRONMENT_STRING:
            return self._venv
        elif tool == PMR_TOOL_STRING:
            return self._vcs

        return False

    def load(self, options):
        self._original_options = options
        step_name_option = self._ui.checkBoxShowStepNames.objectName()
        check_tools_option = self._ui.checkBoxCheckToolsOnStartup.objectName()
        use_external_git_option = self._ui.checkBoxUseExternalGit.objectName()
        pysidercc_option = self._ui.lineEditPySideRCC.objectName()
        pysideuic_option = self._ui.lineEditPySideUIC.objectName()
        venv_path_option = self._ui.lineEditVirtualEnvironmentPath.objectName()
        vcs_option = self._ui.lineEditGitExecutable.objectName()
        if step_name_option in options:
            self._ui.checkBoxShowStepNames.setChecked(options[step_name_option])
        if check_tools_option in options:
            self._ui.checkBoxCheckToolsOnStartup.setChecked(options[check_tools_option])
        if use_external_git_option:
            self._ui.checkBoxUseExternalGit.setChecked(options[use_external_git_option])
        if pysidercc_option in options:
            self._ui.lineEditPySideRCC.setText(options[pysidercc_option])
        if pysideuic_option in options:
            self._ui.lineEditPySideUIC.setText(options[pysideuic_option])
        if venv_path_option in options:
            self._ui.lineEditVirtualEnvironmentPath.setText(options[venv_path_option])
        if vcs_option in options:
            self._ui.lineEditGitExecutable.setText(options[vcs_option])

        self._updateUi()
        self._testTools()

    def save(self):
        options = {}
        options[self._ui.checkBoxShowStepNames.objectName()] = self._ui.checkBoxShowStepNames.isChecked()
        options[self._ui.checkBoxCheckToolsOnStartup.objectName()] = self._ui.checkBoxCheckToolsOnStartup.isChecked()
        options[self._ui.checkBoxUseExternalGit.objectName()] = self._ui.checkBoxUseExternalGit.isChecked()
        options[self._ui.lineEditPySideRCC.objectName()] = self._ui.lineEditPySideRCC.text()
        options[self._ui.lineEditPySideUIC.objectName()] = self._ui.lineEditPySideUIC.text()
        options[self._ui.lineEditVirtualEnvironmentPath.objectName()] = self._ui.lineEditVirtualEnvironmentPath.text()
        options[self._ui.lineEditGitExecutable.objectName()] = self._ui.lineEditGitExecutable.text()

        return options

    def isModified(self):
        return not self._original_options == self.save()


