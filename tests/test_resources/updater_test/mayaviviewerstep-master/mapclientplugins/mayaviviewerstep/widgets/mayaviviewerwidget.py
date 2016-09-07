"""
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
"""
import os
os.environ['ETS_TOOLKIT'] = 'qt4'

from PySide.QtGui import QDialog, QFileDialog, QDialogButtonBox, QAbstractItemView, QTableWidgetItem
from PySide.QtCore import Qt

from mapclientplugins.mayaviviewerstep.widgets.ui_mayaviviewerwidget import Ui_Dialog
from traits.api import HasTraits, Instance, on_trait_change, \
    Int, Dict

# from mayaviviewerobjects import colours, MayaviViewerObjectsContainer
from mappluginutils.mayaviviewer.mayaviviewerobjects import colours, MayaviViewerObjectsContainer


class MayaviViewerWidget(QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """

    GFD = [10,10]
    displayGFNodes = True
    defaultColor = colours['bone']
    objectTableHeaderColumns = {'visible':0, 'type':1}
    mergeGFVertices = False
    backgroundColour = (0.0,0.0,0.0)

    def __init__(self, viewerObjects, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

        # self._view = self._ui.MayaviScene.visualisation.view
        self._scene = self._ui.MayaviScene.visualisation.scene
        self._scene.background = self.backgroundColour

        if isinstance(viewerObjects, MayaviViewerObjectsContainer):
            self._objects = viewerObjects       # models, point clouds, tri-mesh, measurements etc to be rendered {name:(type, object)}
        else:
            raise TypeError, 'viewerObject must be a MayaviViewerObjects instance'

        self._makeConnections()
        self._initialiseObjectTable()
        self._refresh()

        self.selectedObjectName = None

        # self.testPlot()
        # self.drawObjects()

    def _makeConnections(self):
        self._ui.tableWidget.itemClicked.connect(self._tableItemClicked)
        self._ui.tableWidget.itemChanged.connect(self._visibleBoxChanged)
        self._ui.screenshotSaveButton.clicked.connect(self._saveScreenShot)
        self._ui.slicePlaneRadioX.toggled.connect(self._slicePlaneXToggled)
        self._ui.slicePlaneRadioY.toggled.connect(self._slicePlaneYToggled)
        self._ui.slicePlaneRadioZ.toggled.connect(self._slicePlaneZToggled)
        self._ui.closeButton.clicked.connect(self._close)

    def _initialiseObjectTable(self):

        self._ui.tableWidget.setRowCount(self._objects.getNumberOfObjects())
        self._ui.tableWidget.verticalHeader().setVisible(False)
        self._ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        
        row = 0
        for name in self._objects.getObjectNames():
            obj = self._objects.getObject(name)
            self._addObjectToTable(row, name, obj)
            row += 1
            print row, name

        self._ui.tableWidget.resizeColumnToContents(self.objectTableHeaderColumns['visible'])
        self._ui.tableWidget.resizeColumnToContents(self.objectTableHeaderColumns['type'])

    def _addObjectToTable(self, row, name, obj):
        typeName = obj.typeName
        print(typeName)
        print(name)
        tableItem = QTableWidgetItem(name)
        tableItem.setCheckState(Qt.Checked)
        self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['visible'], tableItem)
        self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['type'], QTableWidgetItem(typeName))

    def _tableItemClicked(self):
        selectedRow = self._ui.tableWidget.currentRow()
        self.selectedObjectName = self._ui.tableWidget.item(selectedRow, self.objectTableHeaderColumns['visible']).text()
        self._populateScalarsDropDown(self.selectedObjectName)
        print(selectedRow)
        print(self.selectedObjectName)

        obj = self._objects.getObject(self.selectedObjectName)
        # enable/disable image plane toggles if gias scan is selected
        if obj.typeName=='giasscan':
            self._ui.slicePlaneRadioX.setEnabled(True)
            self._ui.slicePlaneRadioY.setEnabled(True)
            self._ui.slicePlaneRadioZ.setEnabled(True)
        else:
            self._ui.slicePlaneRadioX.setEnabled(False)
            self._ui.slicePlaneRadioY.setEnabled(False)
            self._ui.slicePlaneRadioZ.setEnabled(False)


    def _visibleBoxChanged(self, tableItem):
        # get name of object selected
        # name = self._getSelectedObjectName()

        # checked changed item is actually the checkbox
        if tableItem.column()==self.objectTableHeaderColumns['visible']:
            # get visible status
            name = tableItem.text()
            visible = tableItem.checkState().name=='Checked'

            print('visibleboxchanged name', name)
            print('visibleboxchanged visible', visible)

            # toggle visibility
            obj = self._objects.getObject(name)
            print(obj.name)
            if obj.sceneObject:
                print('changing existing visibility')
                obj.setVisibility(visible)
            else:
                print('drawing new')
                obj.draw(self._scene)

    def _populateScalarsDropDown(self, objectName):
        pass

    def _scalarSelectionChanged(self):
        name = self._getSelectedObjectName()
        scalarName = self._getSelectedScalarName()
        self._objects.getObject(name).updateScalar(scalarName, self._scene)

    def _getSelectedObjectName(self):
        return self.selectedObjectName

    def _getSelectedScalarName(self):
        return 'none'

    def drawObjects(self):
        for name in self._objects.getObjectNames():
            self._objects.getObject(name).draw(self._scene)

    def _close(self):
        for name in self._objects.getObjectNames():
            self._objects.getObject(name).remove()

        self._objects._objects = {}
        self._objects == None

        # for r in xrange(self._ui.tableWidget.rowCount()):
        #     self._ui.tableWidget.removeRow(r)

    def _refresh(self):
        for r in xrange(self._ui.tableWidget.rowCount()):
            tableItem = self._ui.tableWidget.item(r, self.objectTableHeaderColumns['visible'])
            name = tableItem.text()
            visible = tableItem.checkState().name=='Checked'
            obj = self._objects.getObject(name)
            print(obj.name)
            if obj.sceneObject:
                print('changing existing visibility')
                obj.setVisibility(visible)
            else:
                print('drawing new')
                obj.draw(self._scene)

    def _saveScreenShot(self):
        filename = self._ui.screenshotFilenameLineEdit.text()
        width = int(self._ui.screenshotPixelXLineEdit.text())
        height = int(self._ui.screenshotPixelYLineEdit.text())
        self._scene.mlab.savefig( filename, size=( width, height ) )

    def _slicePlaneXToggled(self, checked):
        name = self._getSelectedObjectName()
        obj = self._objects.getObject(name)
        if checked:
            obj.changeSlicePlane('x_axes')

    def _slicePlaneYToggled(self, checked):
        name = self._getSelectedObjectName()
        obj = self._objects.getObject(name)
        if checked:
            obj.changeSlicePlane('y_axes')

    def _slicePlaneZToggled(self, checked):
        name = self._getSelectedObjectName()
        obj = self._objects.getObject(name)
        if checked:
            obj.changeSlicePlane('z_axes')


    #================================================================#
    @on_trait_change('scene.activated')
    def testPlot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.
        print('trait_changed')

        # We can do normal mlab calls on the embedded scene.
        self._scene.mlab.test_points3d()


    # def _saveImage_fired( self ):
    #     self.scene.mlab.savefig( str(self.saveImageFilename), size=( int(self.saveImageWidth), int(self.saveImageLength) ) )
        