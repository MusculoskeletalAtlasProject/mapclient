

from PySide import QtGui
from mapclientplugins.dictserializerstep.ui_configuredialog import Ui_ConfigureDialog
import os.path

INVALID_STYLE_SHEET = 'background-color: rgba(239, 0, 0, 50)'
DEFAULT_STYLE_SHEET = ''

class ConfigureDialog(QtGui.QDialog):
    '''
    Configure dialog to present the user with the options to configure this step.
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self, parent)
        
        self._ui = Ui_ConfigureDialog()
        self._ui.setupUi(self)

        # Keep track of the previous identifier so that we can track changes
        # and know how many occurrences of the current identifier there should
        # be.
        self._previousIdentifier = ''
        # Set a place holder for a callable that will get set from the step.
        # We will use this method to decide whether the identifier is unique.
        self.identifierOccursCount = None
        self._previousLocation = ''

        self._makeConnections()

    def _makeConnections(self):
        self._ui.lineEditIdentifier.textChanged.connect(self.validate)
        self._ui.lineEditOutputLocation.textChanged.connect(self.validate)
        self._ui.checkBoxDefaultLocation.clicked.connect(self.validate)
        self._ui.pushButtonOutputLocation.clicked.connect(self._outputLocationButtonClicked)

    def _outputLocationButtonClicked(self):
        location, _ = QtGui.QFileDialog.getSaveFileName(self, caption='Choose Output File', dir=self._previousLocation)
        if location:
            self._previousLocation = os.path.dirname(location)
            self._ui.lineEditOutputLocation.setText(location)
    
    def accept(self):
        '''
        Override the accept method so that we can confirm saving an
        invalid configuration.
        '''
        result = QtGui.QMessageBox.Yes
        if not self.validate():
            result = QtGui.QMessageBox.warning(self, 'Invalid Configuration',
                'This configuration is invalid.  Unpredictable behaviour may result if you choose \'Yes\', are you sure you want to save this configuration?)',
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if result == QtGui.QMessageBox.Yes:
            QtGui.QDialog.accept(self)

    def validate(self):
        '''
        Validate the configuration dialog fields.  For any field that is not valid
        set the style sheet to the INVALID_STYLE_SHEET.  Return the outcome of the 
        overall validity of the configuration.
        '''
        # Determine if the current identifier is unique throughout the workflow
        # The identifierOccursCount method is part of the interface to the workflow framework.
        
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
        
        value = self.identifierOccursCount(self._ui.lineEditIdentifier.text())
        valid = (value == 0) or (value == 1 and self._previousIdentifier == self._ui.lineEditIdentifier.text())
        if valid:
            self._ui.lineEditIdentifier.setStyleSheet(DEFAULT_STYLE_SHEET)
        else:
            self._ui.lineEditIdentifier.setStyleSheet(INVALID_STYLE_SHEET)

        return valid and (default_location or output_location_valid)

    def getConfig(self):
        '''
        Get the current value of the configuration from the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        '''
        self._previousIdentifier = self._ui.lineEditIdentifier.text()
        config = {}
        config['identifier'] = self._ui.lineEditIdentifier.text()
        config['output'] = self._ui.lineEditOutputLocation.text()
        config['default'] = self._ui.checkBoxDefaultLocation.isChecked()
        return config

    def setConfig(self, config):
        '''
        Set the current value of the configuration for the dialog.  Also
        set the _previousIdentifier value so that we can check uniqueness of the
        identifier over the whole of the workflow.
        '''
        self._previousIdentifier = config['identifier']
        self._ui.lineEditIdentifier.setText(config['identifier'])
        self._ui.lineEditOutputLocation.setText(config['output'])
        self._ui.checkBoxDefaultLocation.setChecked(config['default'])

