

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
        self._previousLocation = ''

        self._make_connections()

    def _make_connections(self):
        self._ui.lineEditDirectoryLocation.textChanged.connect(self.validate)
        self._ui.pushButtonDirectoryChooser.clicked.connect(self._directory_chooser_clicked)

    def _directory_chooser_clicked(self):
        location = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory', self._previousLocation)

        if location:
            self._previousLocation = location
            self._ui.lineEditDirectoryLocation.setText(os.path.relpath(location, self._workflow_location))

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
        directory_valid = os.path.isdir(os.path.join(self._workflow_location, self._ui.lineEditDirectoryLocation.text()))

        self._ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(directory_valid)
        self._ui.lineEditDirectoryLocation.setStyleSheet(DEFAULT_STYLE_SHEET if directory_valid else INVALID_STYLE_SHEET)

        return directory_valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.
        """
        config = {}
        config['Directory'] = self._ui.lineEditDirectoryLocation.text()
        return config

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.
        """
        self._ui.lineEditDirectoryLocation.setText(config['Directory'])

