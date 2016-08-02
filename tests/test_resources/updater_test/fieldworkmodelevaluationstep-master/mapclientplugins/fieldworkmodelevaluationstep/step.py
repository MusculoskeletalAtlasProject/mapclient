
"""
MAP Client Plugin Step
"""
import os

from PySide import QtGui
from PySide import QtCore

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.fieldworkmodelevaluationstep.configuredialog import ConfigureDialog


class FieldworkModelEvaluationStep(WorkflowStepMountPoint):
    """
    Step for evaluating fieldwork models.
    """

    def __init__(self, location):
        super(FieldworkModelEvaluationStep, self).__init__('Fieldwork Model Evaluation', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = 'Fieldwork'
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/fieldworkmodelevaluationstep/images/fieldworkmodelevaluationicon.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodel'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#pointcloud'))
        self._config = {}
        self._config['identifier'] = ''
        self._config['discretisation'] = '[10,10]'
        self._config['node coordinates'] = 'False'
        self._config['elements'] = 'all'

        self.GF = None
        self.evalPoints = None

    def _parseElems(self):
        inputStr = self._config['elements']
        if inputStr=='all':
            elems = 'all'
        else:
            elems = []
            words = inputStr.split(',')
            for w in words:
                if '-' in w:
                    x0,x1 = w.split('-')
                    elems += range(int(x0), int(x1)+1)
                else:
                    elems.append(int(w))

        return elems

    def execute(self):
        """
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        """
        # Put your execute step code here before calling the '_doneExecution' method.
        if self._config['node coordinates']=='True':
            self.evalPoints = self.GF.get_all_point_coordinates()
        else:
            disc = eval(self._config['discretisation'])
            elems = self._parseElems()
            if isinstance(disc, float):
                if elems=='all':
                    self.evalPoints = self.GF.discretiseAllElementsRegularGeoD( self, disc,\
                                        geoCoords=True, unpack=True)[1]
                else:
                    X = []
                    for e in elems:
                        X.append(discretiseElementRegularGeoD( e, disc, geoCoords=True ))

                    self.evalPoints = np.vstack(X)
            else:
                if elems=='all':
                    self.evalPoints = self.GF.evaluate_geometric_field(disc).T
                else:
                    self.evalPoints = self.GF.evaluate_geometric_field_in_elements( disc,\
                        elems).T

        self._doneExecution()

    def setPortData(self, index, dataIn):
        """
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        """
        self.GF = dataIn # ju#fieldworkmodel

    def getPortData(self, index):
        """
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        """
        return self.evalPoints # ju#pointcoordinates

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
        conf.setValue('discretisation', self._config['discretisation'])
        conf.setValue('node coordinates', self._config['node coordinates'])
        conf.setValue('elements', self._config['elements'])
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
        self._config['discretisation'] = conf.value('discretisation', '[10,10]')
        self._config['node coordinates'] = conf.value('node coordinates', 'False')
        self._config['elements'] = conf.value('elements', 'all')
        conf.endGroup()

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()


