

from PySide2 import QtWidgets

from mapclientplugins.filechooserstep.ui_configuredialog import Ui_ConfigureDialog
import os

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''


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

        self._makeConnections()

    def _makeConnections(self):
        self._ui.lineEditFileLocation.textChanged.connect(self.validate)
        self._ui.pushButtonFileChooser.clicked.connect(self._fileChooserClicked)
        
    def _fileChooserClicked(self):
        # Second parameter returned is the filter chosen
        location, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select File Location', self._previousLocation)

        if location:
            self._previousLocation = location
            self._ui.lineEditFileLocation.setText(os.path.relpath(location, self._workflow_location))

    def setWorkflowLocation(self, location):
        self._workflow_location = location

    def accept(self):
        """
        Override the accept method so that we can confirm saving an
        invalid configuration.
        """
        result = QtWidgets.QMessageBox.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(self, 'Invalid Configuration',
                                                   'This configuration is invalid. '
                                                   ' Unpredictable behaviour may result if you choose \'Yes\','
                                                   ' are you sure you want to save this configuration?)',
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
        location_valid = self._ui.lineEditFileLocation.text() and \
            os.path.isfile(os.path.join(self._workflow_location, self._ui.lineEditFileLocation.text()))

        self._ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(location_valid)

        return location_valid

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        config = {}
        config['File'] = self._ui.lineEditFileLocation.text()
        if self._previousLocation:
            config['previous_location'] = os.path.relpath(self._previousLocation, self._workflow_location)
        else:
            config['previous_location'] = ''

        return config

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._ui.lineEditFileLocation.setText(config['File'])
        if 'previous_location' in config:
            self._previousLocation = os.path.join(self._workflow_location, config['previous_location'])

