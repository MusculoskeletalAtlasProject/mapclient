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
from PySide.QtGui import QDoubleValidator, QIntValidator
from PySide.QtCore import Qt

from mapclientplugins.pelvislandmarkshjcpredictionstep.ui_hjcpredictionviewerwidget import Ui_Dialog
from traits.api import HasTraits, Instance, on_trait_change, \
    Int, Dict

from mappluginutils.mayaviviewer import MayaviViewerObjectsContainer, MayaviViewerLandmark, colours
import numpy as np


class MayaviHJCPredictionViewerWidget(QDialog):
    """
    Configure dialog to present the user with the options to configure this step.
    """
    defaultColor = colours['bone']
    objectTableHeaderColumns = {'landmarks':0}
    backgroundColour = (0.0,0.0,0.0)
    _landmarkRenderArgs = {'mode':'sphere', 'scale_factor':5.0, 'color':(0,1,0)}
    _hjcRenderArgs = {'mode':'sphere', 'scale_factor':10.0, 'color':(1,0,0)}

    def __init__(self, landmarks, config, predictFunc, predMethods, popClasses, parent=None):
        QDialog.__init__(self, parent)
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

        self._scene = self._ui.MayaviScene.visualisation.scene
        self._scene.background = self.backgroundColour

        self.selectedObjectName = None
        self._landmarks = landmarks
        self._landmarkNames = sorted(self._landmarks.keys())
        self._predictFunc = predictFunc
        self._predMethods = predMethods
        self._popClasses = popClasses
        self._config = config

        # print 'init...', self._config

        ### FIX FROM HERE ###
        # create self._objects
        self._initViewerObjects()
        self._setupGui()
        self._makeConnections()
        self._initialiseObjectTable()
        self._initialiseSettings()
        self._refresh()

        # self.testPlot()
        # self.drawObjects()
        print('finished init...', self._config)

    def _initViewerObjects(self):
        self._objects = MayaviViewerObjectsContainer()
        for ln in self._landmarkNames:
            self._objects.addObject(ln, MayaviViewerLandmark(ln, self._landmarks[ln],
                                                             renderArgs=self._landmarkRenderArgs)
                                    )
        
        hjcl = self._objects.getObject('HJC_left')
        hjcl.setRenderArgs(self._hjcRenderArgs)
        hjcr = self._objects.getObject('HJC_right')
        hjcr.setRenderArgs(self._hjcRenderArgs)
        # self._objects.addObject('HJC_left', MayaviViewerLandmark('HJC_left', [0,0,0], renderArgs=self._hjcRenderArgs))
        # self._objects.addObject('HJC_right', MayaviViewerLandmark('HJC_right', [0,0,0], renderArgs=self._hjcRenderArgs))

    def _setupGui(self):
        self._ui.screenshotPixelXLineEdit.setValidator(QIntValidator())
        self._ui.screenshotPixelYLineEdit.setValidator(QIntValidator())
        for l in self._landmarkNames:
            self._ui.comboBoxLASIS.addItem(l)
            self._ui.comboBoxRASIS.addItem(l)
            self._ui.comboBoxLPSIS.addItem(l)
            self._ui.comboBoxRPSIS.addItem(l)
            self._ui.comboBoxPS.addItem(l)

        for m in self._predMethods:
            self._ui.comboBoxPredMethod.addItem(m)

        for p in self._popClasses:
            self._ui.comboBoxPopClass.addItem(p)

    def _makeConnections(self):
        self._ui.tableWidget.itemClicked.connect(self._tableItemClicked)
        self._ui.tableWidget.itemChanged.connect(self._visibleBoxChanged)
        self._ui.screenshotSaveButton.clicked.connect(self._saveScreenShot)
        self._ui.predictButton.clicked.connect(self._predict)
        self._ui.resetButton.clicked.connect(self._reset)
        self._ui.abortButton.clicked.connect(self._abort)
        self._ui.acceptButton.clicked.connect(self._accept)

        self._ui.comboBoxPredMethod.activated.connect(self._updateConfigPredMethod)
        self._ui.comboBoxPopClass.activated.connect(self._updateConfigPopClass)
        self._ui.comboBoxLASIS.activated.connect(self._updateConfigLASIS)
        self._ui.comboBoxRASIS.activated.connect(self._updateConfigRASIS)
        self._ui.comboBoxLPSIS.activated.connect(self._updateConfigLPSIS)
        self._ui.comboBoxRPSIS.activated.connect(self._updateConfigRPSIS)
        self._ui.comboBoxPS.activated.connect(self._updateConfigPS)

    def _initialiseSettings(self):
        self._ui.comboBoxPredMethod.setCurrentIndex(self._predMethods.index(self._config['Prediction Method']))
        self._ui.comboBoxPopClass.setCurrentIndex(self._popClasses.index(self._config['Population Class']))
        if self._config['LASIS'] in self._landmarkNames:
            self._ui.comboBoxLASIS.setCurrentIndex(self._landmarkNames.index(self._config['LASIS']))
        else:
            self._ui.comboBoxLASIS.setCurrentIndex(0)

        if self._config['RASIS'] in self._landmarkNames:
            self._ui.comboBoxRASIS.setCurrentIndex(self._landmarkNames.index(self._config['RASIS']))
        else:
            self._ui.comboBoxRASIS.setCurrentIndex(0)

        if self._config['LPSIS'] in self._landmarkNames:
            self._ui.comboBoxLPSIS.setCurrentIndex(self._landmarkNames.index(self._config['LPSIS']))
        else:
            self._ui.comboBoxLPSIS.setCurrentIndex(0)

        if self._config['RPSIS'] in self._landmarkNames:
            self._ui.comboBoxRPSIS.setCurrentIndex(self._landmarkNames.index(self._config['RPSIS']))
        else:
            self._ui.comboBoxRPSIS.setCurrentIndex(0)

        if self._config['PS'] in self._landmarkNames:
            self._ui.comboBoxPS.setCurrentIndex(self._landmarkNames.index(self._config['PS']))
        else:
            self._ui.comboBoxPS.setCurrentIndex(0)

    def _initialiseObjectTable(self):
        self._ui.tableWidget.setRowCount(self._objects.getNumberOfObjects())
        self._ui.tableWidget.verticalHeader().setVisible(False)
        self._ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        
        r = 0
        for ln in self._landmarkNames:
            self._addObjectToTable(r, ln, self._objects.getObject(ln))
            r += 1

        hjclTableItem = self._ui.tableWidget.item(self._landmarkNames.index('HJC_left'),
                                                  self.objectTableHeaderColumns['landmarks'])
        hjclTableItem.setCheckState(Qt.Unchecked)
        hjcrTableItem = self._ui.tableWidget.item(self._landmarkNames.index('HJC_right'),
                                                  self.objectTableHeaderColumns['landmarks'])
        hjcrTableItem.setCheckState(Qt.Unchecked)

        self._ui.tableWidget.resizeColumnToContents(self.objectTableHeaderColumns['landmarks'])

    def _addObjectToTable(self, row, name, obj, checked=True):
        typeName = obj.typeName
        print('adding to table: %s (%s)'%(name, typeName))
        tableItem = QTableWidgetItem(name)
        if checked:
            tableItem.setCheckState(Qt.Checked)
        else:
            tableItem.setCheckState(Qt.Unchecked)

        self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['landmarks'], tableItem)
        # self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['type'], QTableWidgetItem(typeName))

    def _tableItemClicked(self):
        selectedRow = self._ui.tableWidget.currentRow()
        self.selectedObjectName = self._ui.tableWidget.item(
                                    selectedRow,
                                    self.objectTableHeaderColumns['landmarks']
                                    ).text()
        print(selectedRow)
        print(self.selectedObjectName)

    def _visibleBoxChanged(self, tableItem):
        # get name of object selected
        # name = self._getSelectedObjectName()

        # checked changed item is actually the checkbox
        if tableItem.column()==self.objectTableHeaderColumns['landmarks']:
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

    def _getSelectedObjectName(self):
        return self.selectedObjectName

    def _getSelectedScalarName(self):
        return 'none'

    def drawObjects(self):
        for name in self._objects.getObjectNames():
            self._objects.getObject(name).draw(self._scene)

    def _updateConfigPredMethod(self):
        self._config['Prediction Method'] = self._ui.comboBoxPredMethod.currentText()

    def _updateConfigPopClass(self):
        self._config['Population Class'] = self._ui.comboBoxPopClass.currentText()

    def _updateConfigLASIS(self):
        self._config['LASIS'] = self._ui.comboBoxLASIS.currentText()

    def _updateConfigRASIS(self):
        self._config['RASIS'] = self._ui.comboBoxRASIS.currentText()

    def _updateConfigLPSIS(self):
        self._config['LPSIS'] = self._ui.comboBoxLPSIS.currentText()

    def _updateConfigRPSIS(self):
        self._config['RPSIS'] = self._ui.comboBoxRPSIS.currentText()

    def _updateConfigPS(self):
        self._config['PS'] = self._ui.comboBoxPS.currentText()

    def _predict(self):
        self._predictFunc()

        # update predicted HJCs
        hjclObj = self._objects.getObject('HJC_left')
        hjclObj.updateGeometry(self._landmarks['HJC_left'], self._scene)
        hjclTableItem = self._ui.tableWidget.item(self._landmarkNames.index('HJC_left'),
                                                  self.objectTableHeaderColumns['landmarks'])
        hjclTableItem.setCheckState(Qt.Checked)

        hjcrObj = self._objects.getObject('HJC_right')
        hjcrObj.updateGeometry(self._landmarks['HJC_right'], self._scene)
        hjcrTableItem = self._ui.tableWidget.item(self._landmarkNames.index('HJC_right'),
                                                  self.objectTableHeaderColumns['landmarks'])
        hjcrTableItem.setCheckState(Qt.Checked)

    def _reset(self):
        # delete viewer table row
        # self._ui.tableWidget.removeRow(2)
        # reset registered datacloud
        hjclObj = self._objects.getObject('HJC_left')
        hjclObj.updateGeometry(np.array([0,0,0]), self._scene)
        hjclTableItem = self._ui.tableWidget.item(self._landmarkNames.index('HJC_left'),
                                                  self.objectTableHeaderColumns['landmarks'])
        hjclTableItem.setCheckState(Qt.Unchecked)

        hjcrObj = self._objects.getObject('HJC_right')
        hjcrObj.updateGeometry(np.array([0,0,0]), self._scene)
        hjcrTableItem = self._ui.tableWidget.item(self._landmarkNames.index('HJC_right'),
                                                  self.objectTableHeaderColumns['landmarks'])
        hjcrTableItem.setCheckState(Qt.Unchecked)

    def _accept(self):
        self._close()

    def _abort(self):
        self._reset()
        del self._landmarks['HJC_left']
        del self._landmarks['HJC_right']
        self._close()

    def _close(self):
        for name in self._objects.getObjectNames():
            self._objects.getObject(name).remove()

        self._objects._objects = {}
        self._objects == None

        # for r in xrange(self._ui.tableWidget.rowCount()):
        #     self._ui.tableWidget.removeRow(r)

    def _refresh(self):
        for r in xrange(self._ui.tableWidget.rowCount()):
            tableItem = self._ui.tableWidget.item(r, self.objectTableHeaderColumns['landmarks'])
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
