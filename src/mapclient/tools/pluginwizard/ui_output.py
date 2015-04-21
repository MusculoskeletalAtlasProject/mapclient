# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/output.ui'
#
# Created: Fri Nov  1 11:58:22 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Output(object):
    def setupUi(self, Output):
        Output.setObjectName("Output")
        Output.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Output)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.directoryLabel = QtGui.QLabel(Output)
        self.directoryLabel.setObjectName("directoryLabel")
        self.horizontalLayout.addWidget(self.directoryLabel)
        self.directoryLineEdit = QtGui.QLineEdit(Output)
        self.directoryLineEdit.setObjectName("directoryLineEdit")
        self.horizontalLayout.addWidget(self.directoryLineEdit)
        self.directoryButton = QtGui.QPushButton(Output)
        self.directoryButton.setObjectName("directoryButton")
        self.horizontalLayout.addWidget(self.directoryButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 252, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Output)
        QtCore.QMetaObject.connectSlotsByName(Output)

    def retranslateUi(self, Output):
        Output.setWindowTitle(QtGui.QApplication.translate("Output", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.directoryLabel.setText(QtGui.QApplication.translate("Output", "Output directory:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.directoryLineEdit.setToolTip(QtGui.QApplication.translate("Output", "directory must exist and be writable", None, QtGui.QApplication.UnicodeUTF8))
        self.directoryButton.setText(QtGui.QApplication.translate("Output", "...", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
