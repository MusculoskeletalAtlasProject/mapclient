

from PySide2 import QtWidgets
from mapclientplugins.dictserializerstep.ui_configuredialog import Ui_ConfigureDialog
import os.path

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

        self._previousLocation = ''

        self._make_connections()

    def _make_connections(self):
        self._ui.lineEditOutputLocation.textChanged.connect(self.validate)
        self._ui.checkBoxDefaultLocation.clicked.connect(self.validate)
        self._ui.pushButtonOutputLocation.clicked.connect(self._output_location_button_clicked)

    def _output_location_button_clicked(self):
        location, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption='Choose Output File', dir=self._previousLocation)
        if location:
            self._previousLocation = os.path.dirname(location)
            self._ui.lineEditOutputLocation.setText(location)
    
    def accept(self):
        """
        Override the accept method so that we can confirm saving an
        invalid configuration.
        """
        result = QtWidgets.QMessageBox.Yes
        if not self.validate():
            result = QtWidgets.QMessageBox.warning(self, 'Invalid Configuration',
                                                   'This configuration is invalid.  '
                                                   'Unpredictable behaviour may result if you choose \'Yes\','
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
        sender = self.sender()
        output_directory_valid = False
        output_location_valid = False
        output_location = self._ui.lineEditOutputLocation.text()
        
        output_directory = os.path.dirname(output_location)
        output_file = os.path.basename(output_location)
        if os.path.isdir(output_directory):
            output_directory_valid = True
            
        if sender == self._ui.lineEditOutputLocation and output_directory_valid:
            self._ui.checkBoxDefaultLocation.setChecked(False)
            
        default_location = self._ui.checkBoxDefaultLocation.isChecked()
        if output_location and output_file and output_directory_valid:
            output_location_valid = True

        self._ui.lineEditOutputLocation.setStyleSheet(DEFAULT_STYLE_SHEET if output_location_valid else INVALID_STYLE_SHEET)

        return (default_location or output_location_valid)

    def getConfig(self):
        """
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        config = {'output': self._ui.lineEditOutputLocation.text(), 'default': self._ui.checkBoxDefaultLocation.isChecked()}
        return config

    def setConfig(self, config):
        """
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        """
        self._ui.lineEditOutputLocation.setText(config['output'])
        self._ui.checkBoxDefaultLocation.setChecked(config['default'])

