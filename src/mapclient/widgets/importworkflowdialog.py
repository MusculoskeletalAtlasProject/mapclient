'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
from PySide import QtGui
from mapclient.widgets.ui_importworkflowdialog import Ui_ImportWorkflowDialog
from mapclient.tools.pmr.pmrworkflowwidget import PMRWorkflowWidget
from mapclient.tools.pmr.pmrtool import workflow_search_string

class ImportWorkflowDialog(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self, previousLocation, parent=None):
        '''
        Constructor
        '''
        super(ImportWorkflowDialog, self).__init__(parent)
        self._ui = Ui_ImportWorkflowDialog()
        self._ui.setupUi(self)
        self._setupPMRWidget()

        self._previousLocation = previousLocation

        self._makeConnections()

    def _makeConnections(self):
        self._ui.pushButtonLocation.clicked.connect(self._setDestination)

    def _setupPMRWidget(self):
        self._pmr_widget = PMRWorkflowWidget(self)
        self._pmr_widget.setExport(False)
        self._pmr_widget.setImport(False)
        self._pmr_widget.setSearchDomain(workflow_search_string)
        layout = self.layout()
        # Save a little time by setting the layout disabled while
        # the layout is being de-constructed and constructed again.
        layout.setEnabled(False)
        # Remove the existing items in the layout
        existing_items = []
        for index in range(layout.count(), 0, -1):
            existing_items.append(layout.takeAt(index - 1))

        # Put all the items into the layout in the desired order
        layout.addWidget(self._pmr_widget)
        existing_items.reverse()
        for item in existing_items:
            layout.addItem(item)
        layout.setEnabled(True)

    def destinationDir(self):
        return self._ui.lineEditLocation.text()

    def workspaceUrl(self):
        return self._pmr_widget.workspaceUrl()

    def _setDestination(self):
        workflowDir = QtGui.QFileDialog.getExistingDirectory(self, caption='Select Workflow Directory', directory=self._previousLocation)
        if workflowDir:
            self._ui.lineEditLocation.setText(workflowDir)


