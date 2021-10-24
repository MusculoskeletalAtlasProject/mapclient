"""
Created on Feb 25, 2015

@author: hsorby
"""
import os.path

from PySide2 import QtWidgets

from mapclient.view.managers.options.ui.ui_optionsdialog import Ui_OptionsDialog

from mapclient.core.checks import WizardToolChecks, VCSChecks
from mapclient.view.syntaxhighlighter import SyntaxHighlighter
from mapclient.settings.definitions import VIRTUAL_ENVIRONMENT_STRING, \
    WIZARD_TOOL_STRING, PMR_TOOL_STRING, INTERNAL_WORKFLOWS_AVAILABLE


class OptionsDialog(QtWidgets.QDialog):
    """
    Options dialog for setting global options
    """

    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)
        self._ui = Ui_OptionsDialog()
        self._ui.setupUi(self)
        self._ui.lineEditGitExecutable.setEnabled(False)
        self._ui.pushButtonGitExecutable.setEnabled(False)

        self._highlighter = SyntaxHighlighter(self._ui.plainTextEditToolTestOutput.document())

        self._make_connections()

        self._wizard_tool = False
        self._vcs = False

        self._location = ''
        self._original_options = {}

    def _make_connections(self):
        self._ui.pushButtonPySideRCC.clicked.connect(self._pyside_rcc_button_clicked)
        self._ui.pushButtonGitExecutable.clicked.connect(self._git_executable_button_clicked)
        self._ui.pushButtonPySideRCC.clicked.connect(self._pyside_rcc_button_clicked)
        self._ui.pushButtonPySideUIC.clicked.connect(self._pyside_uic_button_clicked)
        self._ui.pushButtonRunChecks.clicked.connect(self._test_tools)
        self._ui.checkBoxUseExternalGit.clicked.connect(self._use_external_star_clicked)
        self._ui.checkBoxUseExternalPySideRCC.clicked.connect(self._use_external_star_clicked)
        self._ui.checkBoxUseExternalPySideUIC.clicked.connect(self._use_external_star_clicked)
        self._ui.pushButtonInternalWorkflowDirectory.clicked.connect(self._internal_workflow_directory_button_clicked)

    def _update_ui(self):
        self._ui.lineEditGitExecutable.setEnabled(self._ui.checkBoxUseExternalGit.isChecked())
        self._ui.pushButtonGitExecutable.setEnabled(self._ui.checkBoxUseExternalGit.isChecked())
        self._ui.lineEditPySideRCC.setEnabled(self._ui.checkBoxUseExternalPySideRCC.isChecked())
        self._ui.pushButtonPySideRCC.setEnabled(self._ui.checkBoxUseExternalPySideRCC.isChecked())
        self._ui.lineEditPySideUIC.setEnabled(self._ui.checkBoxUseExternalPySideUIC.isChecked())
        self._ui.pushButtonPySideUIC.setEnabled(self._ui.checkBoxUseExternalPySideUIC.isChecked())
        if INTERNAL_WORKFLOWS_AVAILABLE in self._original_options:
            self._ui.groupBoxInternalWorkflowDirectory.setVisible(self._original_options[INTERNAL_WORKFLOWS_AVAILABLE])

    def _internal_workflow_directory_button_clicked(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Select internal workflow directory',
                                                               dir=self._location)
        if directory:
            self._ui.lineEditInternalWorkflowDirectory.setText(directory)
            self._location = directory

    def _pyside_rcc_button_clicked(self):
        rcc_program, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Select PySide Resource Compiler',
                                                               dir=self._location)
        if rcc_program:
            self._ui.lineEditPySideRCC.setText(rcc_program)
            self._location = os.path.dirname(rcc_program)
            self._test_tools()

    def _pyside_uic_button_clicked(self):
        uic_program, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Select PySide User Interface Compiler',
                                                               dir=self._location)
        if uic_program:
            self._ui.lineEditPySideUIC.setText(uic_program)
            self._location = os.path.dirname(uic_program)
            self._test_tools()

    def _git_executable_button_clicked(self):
        git_program, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Select Git Executable',
                                                               dir=self._location)
        if git_program:
            self._ui.lineEditGitExecutable.setText(git_program)
            self._location = os.path.dirname(git_program)
            self._test_tools()

    def _use_external_star_clicked(self):
        self._update_ui()

    def _test_tools(self):
        options = self.save()
        self._ui.plainTextEditToolTestOutput.setPlainText('')
        checks_wizard = WizardToolChecks(options)
        self._wizard_tool, output = self._handle_check(checks_wizard, WIZARD_TOOL_STRING)
        self._ui.plainTextEditToolTestOutput.appendPlainText(output)  # labelCheckOutput.setText(output)
        checks_vcs = VCSChecks(options)
        self._vcs, output = self._handle_check(checks_vcs, PMR_TOOL_STRING)
        self._ui.plainTextEditToolTestOutput.appendPlainText(output)  # labelCheckOutput.setText(output)

    @staticmethod
    def _handle_check(check, title):
        output = ''  # self._ui.plainTextEditScreen.document().toPlainText()
        result = check.doCheck()
        if result:
            output += 'Success: {0}'.format(title)
        else:
            output += 'Failure: {0}\n'.format(title)
            output += check.report()

        return result, output

    def setCurrentTab(self, tab_index):
        self._ui.tabWidget.setCurrentIndex(tab_index)

    def reject(self, *args, **kwargs):
        self._test_tools()
        return QtWidgets.QDialog.reject(self, *args, **kwargs)

    def accept(self, *args, **kwargs):
        self._test_tools()
        return QtWidgets.QDialog.accept(self, *args, **kwargs)

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
        use_external_rcc_option = self._ui.checkBoxUseExternalPySideRCC.objectName()
        use_external_uic_option = self._ui.checkBoxUseExternalPySideUIC.objectName()
        pysidercc_option = self._ui.lineEditPySideRCC.objectName()
        pysideuic_option = self._ui.lineEditPySideUIC.objectName()
        vcs_option = self._ui.lineEditGitExecutable.objectName()
        internal_directory_option = self._ui.lineEditInternalWorkflowDirectory.objectName()
        if step_name_option in options:
            self._ui.checkBoxShowStepNames.setChecked(options[step_name_option])
        if check_tools_option in options:
            self._ui.checkBoxCheckToolsOnStartup.setChecked(options[check_tools_option])
        if use_external_git_option:
            self._ui.checkBoxUseExternalGit.setChecked(options[use_external_git_option])
        if use_external_rcc_option in options:
            self._ui.checkBoxUseExternalPySideRCC.setChecked(options[use_external_rcc_option])
        if use_external_uic_option in options:
            self._ui.checkBoxUseExternalPySideUIC.setChecked(options[use_external_uic_option])
        if pysidercc_option in options:
            self._ui.lineEditPySideRCC.setText(options[pysidercc_option])
        if pysideuic_option in options:
            self._ui.lineEditPySideUIC.setText(options[pysideuic_option])
        if vcs_option in options:
            self._ui.lineEditGitExecutable.setText(options[vcs_option])
        if internal_directory_option in options:
            self._ui.lineEditInternalWorkflowDirectory.setText(options[internal_directory_option])

        self._update_ui()
        self._test_tools()

    def save(self):
        options = {self._ui.checkBoxShowStepNames.objectName(): self._ui.checkBoxShowStepNames.isChecked(),
                   self._ui.checkBoxCheckToolsOnStartup.objectName(): self._ui.checkBoxCheckToolsOnStartup.isChecked(),
                   self._ui.checkBoxUseExternalGit.objectName(): self._ui.checkBoxUseExternalGit.isChecked(),
                   self._ui.checkBoxUseExternalPySideRCC.objectName(): self._ui.checkBoxUseExternalPySideRCC.isChecked(),
                   self._ui.checkBoxUseExternalPySideUIC.objectName(): self._ui.checkBoxUseExternalPySideUIC.isChecked(),
                   self._ui.lineEditPySideRCC.objectName(): self._ui.lineEditPySideRCC.text(),
                   self._ui.lineEditPySideUIC.objectName(): self._ui.lineEditPySideUIC.text(),
                   self._ui.lineEditGitExecutable.objectName(): self._ui.lineEditGitExecutable.text(),
                   self._ui.lineEditInternalWorkflowDirectory.objectName(): self._ui.lineEditInternalWorkflowDirectory.text()}

        return options

    def isModified(self):
        return not self._original_options == self.save()
