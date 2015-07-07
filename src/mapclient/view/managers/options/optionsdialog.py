'''
Created on Feb 25, 2015

@author: hsorby
'''
import os.path

from PySide import QtGui

from mapclient.view.managers.options.ui.ui_optionsdialog import Ui_OptionsDialog
from mapclient.core.checks import WizardToolChecks, VirtualEnvChecks, VCSChecks
from mapclient.view.syntaxhighlighter import SyntaxHighlighter

class  OptionsDialog(QtGui.QDialog):
    '''
    Options dialog for setting global options
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(OptionsDialog, self).__init__(parent)
        self._ui = Ui_OptionsDialog()
        self._ui.setupUi(self)

        self._highlighter = SyntaxHighlighter(self._ui.plainTextEditToolTestOutput.document())

        self._makeConnections()

        self._location = ''
        self._original_options = {}

    def _makeConnections(self):
        self._ui.pushButtonPySideRCC.clicked.connect(self._pySideRCCButtonClicked)
        self._ui.pushButtonPySideUIC.clicked.connect(self._pySideUICButtonClicked)
        self._ui.pushButtonVirtualEnvironmentPath.clicked.connect(self._venvButtonClicked)
        self._ui.pushButtonGitExecutable.clicked.connect(self._gitExecutableButtonClicked)
        self._ui.pushButtonRunChecks.clicked.connect(self._testTools)

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

    def _venvButtonClicked(self):
        venv_path = QtGui.QFileDialog.getExistingDirectory(self, caption='Select Virtual Environment Path', dir=self._location)
        if venv_path:
            self._ui.lineEditVirtualEnvironmentPath.setText(venv_path)
            self._location = venv_path
            self._testTools()

    def _gitExecutableButtonClicked(self):
        git_program, _ = QtGui.QFileDialog.getOpenFileName(self, caption='Select Git Executable', dir=self._location)
        if git_program:
            self._ui.lineEditGitExecutable.setText(git_program)
            self._location = os.path.dirname(git_program)
            self._testTools()

    def _testTools(self):
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

    def load(self, options):
        self._original_options = options
        step_name_option = self._ui.checkBoxShowStepNames.objectName()
        pysidercc_option = self._ui.lineEditPySideRCC.objectName()
        pysideuic_option = self._ui.lineEditPySideUIC.objectName()
        venv_path_option = self._ui.lineEditVirtualEnvironmentPath.objectName()
        vcs_option = self._ui.lineEditGitExecutable.objectName()
        if step_name_option in options:
            self._ui.checkBoxShowStepNames.setChecked(options[step_name_option])
        if pysidercc_option in options:
            self._ui.lineEditPySideRCC.setText(options[pysidercc_option])
        if pysideuic_option in options:
            self._ui.lineEditPySideUIC.setText(options[pysideuic_option])
        if venv_path_option in options:
            self._ui.lineEditVirtualEnvironmentPath.setText(options[venv_path_option])
        if vcs_option in options:
            self._ui.lineEditGitExecutable.setText(options[vcs_option])

    def save(self):
        options = {}
        options[self._ui.checkBoxShowStepNames.objectName()] = self._ui.checkBoxShowStepNames.isChecked()
        options[self._ui.lineEditPySideRCC.objectName()] = self._ui.lineEditPySideRCC.text()
        options[self._ui.lineEditPySideUIC.objectName()] = self._ui.lineEditPySideUIC.text()
        options[self._ui.lineEditVirtualEnvironmentPath.objectName()] = self._ui.lineEditVirtualEnvironmentPath.text()
        options[self._ui.lineEditGitExecutable.objectName()] = self._ui.lineEditGitExecutable.text()

        return options

    def isModified(self):
        return not self._original_options == self.save()


