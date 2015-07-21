
'''
MAP Client Plugin Step
'''
import os

import json


from PySide import QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.dictserializerstep.configuredialog import ConfigureDialog

DICT_OUTPUT_FILENAME = 'dict.json'

class DictSerializerStep(WorkflowStepMountPoint):
    '''
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    '''

    def __init__(self, location):
        super(DictSerializerStep, self).__init__('Dict Serializer', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = 'Sink'
        # Add any other initialisation code here:
        self._icon =  QtGui.QImage(':/dictserializerstep/images/data-sink.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#dict'))
        self._config = {}
        self._config['identifier'] = ''
        self._config['default'] = True
        self._config['output'] = ''
        self._data_in = None


    def execute(self):
        '''
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        '''
        # Put your execute step code here before calling the '_doneExecution' method.
        json_string = json.dumps(self._data_in, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        if self._config['default']:
            output_dir = os.path.join(self._location, self._config['identifier'])
            filename = os.path.join(output_dir, DICT_OUTPUT_FILENAME)
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
        else:
            filename = self._config['output']

        with open(filename, 'w') as f:
            f.write(json_string)

        self._doneExecution()

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''
        self._data_in = dataIn # http://physiomeproject.org/workflow/1.0/rdf-schema#dict

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog(QtGui.QApplication.activeWindow().currentWidget())
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)
        
        if dlg.exec_():
            self._config = dlg.getConfig()
        
        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._config['identifier']

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._config['identifier'] = identifier

    def serialize(self):
        '''
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        '''
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)


    def deserialize(self, string):
        '''
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.
        '''
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()


