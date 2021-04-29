"""
Created on Jun 24, 2015

@author: hsorby
"""
from PySide2 import QtCore, QtWidgets, QtGui

from mapclient.tools.mapicon.ui_mapicondialog import Ui_MAPIconDialog
import os.path


class MAPIconDialog(QtWidgets.QDialog):

    def __init__(self, location, parent=None):
        super(MAPIconDialog, self).__init__(parent)
        self._ui = Ui_MAPIconDialog()
        self._ui.setupUi(self)

        self._location = location

        self._makeConnections()

    def createIcon(self):
        if self._ui.lineEditCombinedIcon.text():
            self._ui.labelIconPicture.pixmap().save(self._ui.lineEditCombinedIcon.text())

    def _constructImage(self, icon, background):
        icon_image = QtGui.QImage(icon)
        background_image = QtGui.QImage(background)
        painter = QtGui.QPainter(background_image)

        painter.drawImage(QtCore.QPoint(0, 0), icon_image)
        painter.end()

        return background_image

    def _displayIcon(self):
        icon_files = self._getIconFiles()
        if all(icon_files):
            image = self._constructImage(icon_files[0], icon_files[1])
            self._ui.labelIconPicture.setPixmap(QtGui.QPixmap.fromImage(image).scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation))

    def _getIconFiles(self):
        return [self._ui.lineEditStepIcon.text(),
                self._ui.lineEditBackgroundIcon.text()]

    def _makeConnections(self):
        self._ui.pushButtonStepIcon.clicked.connect(self._fileChooser)
        self._ui.pushButtonBackgroundIcon.clicked.connect(self._fileChooser)
        self._ui.pushButtonCombinedIcon.clicked.connect(self._fileChooser)

        self._ui.lineEditStepIcon.textChanged.connect(self._displayIcon)
        self._ui.lineEditBackgroundIcon.textChanged.connect(self._displayIcon)

    def _fileChooser(self):
        sender = self.sender()
        if sender == self._ui.pushButtonCombinedIcon:
            icon, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption='Choose Icon File', dir=self._location)
        else:
            icon, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Choose Icon File', dir=self._location, options=QtGui.QFileDialog.ReadOnly)

        if len(icon) > 0:
            self._location = os.path.dirname(icon)
            if sender == self._ui.pushButtonStepIcon:
                self._ui.lineEditStepIcon.setText(icon)
            elif sender == self._ui.pushButtonBackgroundIcon:
                self._ui.lineEditBackgroundIcon.setText(icon)
            elif sender == self._ui.pushButtonCombinedIcon:
                self._ui.lineEditCombinedIcon.setText(icon)
