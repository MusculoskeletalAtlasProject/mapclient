

from PySide2 import QtWidgets
from mapclientplugins.directorychooserstep.ui_configuredialog import Ui_ConfigureDialog
import os.path

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''

CONFIGURATION_INVALID_TEXT = 'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\',' \
                             ' are you sure you want to save this configuration?)'


class ConfigureDialog(QtWidgets.QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)

        self._workflow_location = None
        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None
        self._previousLocation = ''

        self._make_connections()

    def _make_connections(self):
        self._ui.lineEdit0.textChanged.connect(self.validate)
        self._ui.lineEditDirectoryLocation.textChanged.connect(self.validate)
        self._ui.pushButtonDirectoryChooser.clicked.connect(self._directory_chooser_clicked)

    def _directory_chooser_clicked(self):
        location = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory', self._previousLocation)

        if location:
            self._previousLocation = location
            display_location = self._output_location(location)
            self._ui.lineEditDirectoryLocation.setText(display_location)

    def _output_location(self, location=None):
        if location is None:
            display_path = self._ui.lineEditDirectoryLocation.text()
        else:
            display_path = location
        if self._workflow_location and os.path.isabs(display_path):
            display_path = os.path.relpath(display_path, self._workflow_location)

        return display_path

    def setWorkflowLocation(self, location):
        self._workflow_location = location

    def accept(self):
        """
        Override the accept method so that we can confirm saving an
        invalid configuration.
        """
        result = QtWidgets.QMessageBox.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(self, 'Invalid Configuration', CONFIGURATION_INVALID_TEXT,
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            QtWidgets.QDialog.accept(self)

    def validate(self):
        """
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the
        overall validity of the configuration.
        """
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        value = self.identifierOccursCount(self._ui.lineEdit0.text())
        valid = (value == 0) or (value == 1 and self._previousIdentifier == self._ui.lineEdit0.text())
        if valid:
            self._ui.lineEdit0.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.lineEdit0.setStyleSheet(INVALID_STYLE_SHEET)

        dir_path = self._output_location()
        if self._workflow_location:
            dir_path = os.path.join(self._workflow_location, dir_path)
        directory_valid = os.path.isdir(dir_path) and len(dir_path) > 0

        return valid and directory_valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = self._ui.lineEdit0.text()
        return {'identifier': self._ui.lineEdit0.text(), 'Directory': self._output_location()}

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._previousIdentifier = config['identifier']
        self._ui.lineEdit0.setText(config['identifier'])
        self._ui.lineEditDirectoryLocation.setText(config['Directory'])

