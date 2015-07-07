# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/importworkflowdialog.ui'
#
# Created: Fri Sep  5 20:24:40 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ImportWorkflowDialog(object):
    def setupUi(self, ImportWorkflowDialog):
        ImportWorkflowDialog.setObjectName("ImportWorkflowDialog")
        ImportWorkflowDialog.resize(574, 389)
        self.verticalLayout = QtGui.QVBoxLayout(ImportWorkflowDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(ImportWorkflowDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditLocation = QtGui.QLineEdit(ImportWorkflowDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditLocation.sizePolicy().hasHeightForWidth())
        self.lineEditLocation.setSizePolicy(sizePolicy)
        self.lineEditLocation.setObjectName("lineEditLocation")
        self.horizontalLayout.addWidget(self.lineEditLocation)
        self.pushButtonLocation = QtGui.QPushButton(ImportWorkflowDialog)
        self.pushButtonLocation.setObjectName("pushButtonLocation")
        self.horizontalLayout.addWidget(self.pushButtonLocation)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBoxImport = QtGui.QDialogButtonBox(ImportWorkflowDialog)
        self.buttonBoxImport.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxImport.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBoxImport.setObjectName("buttonBoxImport")
        self.verticalLayout.addWidget(self.buttonBoxImport)

        self.retranslateUi(ImportWorkflowDialog)
        QtCore.QObject.connect(self.buttonBoxImport, QtCore.SIGNAL("accepted()"), ImportWorkflowDialog.accept)
        QtCore.QObject.connect(self.buttonBoxImport, QtCore.SIGNAL("rejected()"), ImportWorkflowDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportWorkflowDialog)

    def retranslateUi(self, ImportWorkflowDialog):
        ImportWorkflowDialog.setWindowTitle(QtGui.QApplication.translate("ImportWorkflowDialog", "Import Workflow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ImportWorkflowDialog", "Destination:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonLocation.setText(QtGui.QApplication.translate("ImportWorkflowDialog", "...", None, QtGui.QApplication.UnicodeUTF8))

