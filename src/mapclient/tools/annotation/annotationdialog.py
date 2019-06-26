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
import re

from PySide2 import QtWidgets

from mapclient.tools.annotation.ui_annotationdialog import Ui_AnnotationDialog
from mapclient.tools.annotation.annotationtool import AnnotationTool


class AnnotationDialog(QtWidgets.QDialog):
    """
    Dialog for annotating a directory.
    """

    def __init__(self, location, annotation_filename=None, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_AnnotationDialog()
        self._ui.setupUi(self)
        
        if len(location) > 0:
            self._ui.fileButton.hide()
            
        self._ui.locationLineEdit.setText(location)
        self._tool = AnnotationTool()
        self._annotation_filename = annotation_filename
        self._tool.deserialize(location, annotation_filename)
        
        self._ui.subjectComboBox.addItems(self._tool.getTerms())
        self._ui.predicateComboBox.addItems(self._tool.getTerms())
        self._ui.objectComboBox.addItems(self._tool.getTerms())
        
        for triple in self._tool.getTriples():
            self._addTriple(triple[0], triple[1], triple[2])
        
        self._makeConnections()
        
    def _makeConnections(self):
        self._ui.addButton.clicked.connect(self._addStatement)
        self._ui.removeButton.clicked.connect(self._removeStatement)
        self._ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self._accept)
        
    def _addTriple(self, subj, pred, obj):
        self._ui.annotationListWidget.addItem('[' + subj + ', ' + pred + ', ' + obj + ']')
    
    def _addStatement(self):
        subj = self._ui.subjectComboBox.currentText()
        pred = self._ui.predicateComboBox.currentText()
        obj = self._ui.objectComboBox.currentText()
        
        self._addTriple(subj, pred, obj)
    
    def _removeStatement(self):
        for index in self._ui.annotationListWidget.selectedIndexes():
            self._ui.annotationListWidget.takeItem(index.row())
    
    def _accept(self):
        triple_re = re.compile('\[(.*), (.*), (.*)\]')
        
        self._tool.clear()
        while self._ui.annotationListWidget.count() > 0:
            item = self._ui.annotationListWidget.takeItem(0)
            match = triple_re.match(item.text())
            if match:
                sbj = match.group(1)
                pred = match.group(2)
                obj = match.group(3)
                self._tool.addTriple(sbj, pred, obj)

        location = self._ui.locationLineEdit.text()
        self._tool.serialize(location, self._annotation_filename)        
        self.accept()
