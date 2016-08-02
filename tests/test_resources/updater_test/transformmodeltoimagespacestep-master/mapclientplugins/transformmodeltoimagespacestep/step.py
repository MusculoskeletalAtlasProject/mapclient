
"""
MAP Client Plugin Step
"""
import os

from PySide import QtGui
from PySide import QtCore

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.transformmodeltoimagespacestep.configuredialog import ConfigureDialog

from gias.musculoskeletal import fw_segmentation_tools as fst

class TransformModeltoImageSpaceStep(WorkflowStepMountPoint):
    """
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    """

    def __init__(self, location):
        super(TransformModeltoImageSpaceStep, self).__init__('Transform Model to Image Space', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = 'Registration'
        # Add any other initialisation code here:
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'ju#fieldworkmodeldict'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#giasscandict'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodeldict'))
        self._config = {}
        self._config['identifier'] = ''
        self._config['Mirror'] = 'False'
        self._config['Z Shift'] = 'False'

        self._scan = None
        self._inputModelDict = None
        self._outputModelDict = None

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        if self._config['Mirror']=='False':
            ns = False
        elif self._config['Mirror']=='True':
            ns = True
    
        if self._config['Z Shift']=='False':
            zs = False
        elif self._config['Z Shift']=='True':
            zs = True

        self._outputModelDict = {}
        for name, gf in self._inputModelDict.items():
            self._outputModelDict[name] = fst.makeImageSpaceGF(self._scan, gf, negSpacing=ns, zShift=zs)

        self._doneExecution()

    def setPortData(self, index, dataIn):
        """
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        """
        if index == 1:
            if len(dataIn)>1:
                raise ValueError, 'only one image supported.'

            self._scan = dataIn.values()[0] # ju#giasscandict
        else:
            self._inputModelDict = dataIn # ju#fieldworkmodeldict

    def getPortData(self, index):
        """
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        """
        return self._outputModelDict

    def configure(self):
        """
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        """
        dlg = ConfigureDialog()
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)
        
        if dlg.exec_():
            self._config = dlg.getConfig()
        
        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        """
        The identifier is a string that must be unique within a workflow.
        """
        return self._config['identifier']

    def setIdentifier(self, identifier):
        """
        The framework will set the identifier for this step when it is loaded.
        """
        self._config['identifier'] = identifier

    def serialize(self, location):
        """
        Add code to serialize this step to disk.  The filename should
        use the step identifier (received from getIdentifier()) to keep it
        unique within the workflow.  The suggested name for the file on
        disk is:
            filename = getIdentifier() + '.conf'
        """
        configuration_file = os.path.join(location, self.getIdentifier() + '.conf')
        conf = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        conf.beginGroup('config')
        conf.setValue('identifier', self._config['identifier'])
        conf.setValue('Mirror', self._config['Mirror'])
        conf.setValue('Z Shift', self._config['Z Shift'])
        conf.endGroup()


    def deserialize(self, location):
        """
        Add code to deserialize this step from disk.  As with the serialize 
        method the filename should use the step identifier.  Obviously the 
        filename used here should be the same as the one used by the
        serialize method.
        """
        configuration_file = os.path.join(location, self.getIdentifier() + '.conf')
        conf = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        conf.beginGroup('config')
        self._config['identifier'] = conf.value('identifier', '')
        self._config['Mirror'] = conf.value('Mirror', 'True')
        self._config['Z Shift'] = conf.value('Z Shift', 'True')
        conf.endGroup()

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()


