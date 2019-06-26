# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mapclient/view/qt/importworkflowdialog.ui',
# licensing of 'src/mapclient/view/qt/importworkflowdialog.ui' applies.
#
# Created: Wed Jun 26 11:26:22 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ImportWorkflowDialog(object):
    def setupUi(self, ImportWorkflowDialog):
        ImportWorkflowDialog.setObjectName("ImportWorkflowDialog")
        ImportWorkflowDialog.resize(541, 523)
        self.verticalLayout = QtWidgets.QVBoxLayout(ImportWorkflowDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(ImportWorkflowDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditLocation = QtWidgets.QLineEdit(ImportWorkflowDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditLocation.sizePolicy().hasHeightForWidth())
        self.lineEditLocation.setSizePolicy(sizePolicy)
        self.lineEditLocation.setObjectName("lineEditLocation")
        self.horizontalLayout.addWidget(self.lineEditLocation)
        self.pushButtonLocation = QtWidgets.QPushButton(ImportWorkflowDialog)
        self.pushButtonLocation.setObjectName("pushButtonLocation")
        self.horizontalLayout.addWidget(self.pushButtonLocation)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBoxImport = QtWidgets.QDialogButtonBox(ImportWorkflowDialog)
        self.buttonBoxImport.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBoxImport.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBoxImport.setObjectName("buttonBoxImport")
        self.verticalLayout.addWidget(self.buttonBoxImport)

        self.retranslateUi(ImportWorkflowDialog)
        QtCore.QObject.connect(self.buttonBoxImport, QtCore.SIGNAL("accepted()"), ImportWorkflowDialog.accept)
        QtCore.QObject.connect(self.buttonBoxImport, QtCore.SIGNAL("rejected()"), ImportWorkflowDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportWorkflowDialog)

    def retranslateUi(self, ImportWorkflowDialog):
        ImportWorkflowDialog.setWindowTitle(QtWidgets.QApplication.translate("ImportWorkflowDialog", "Import Workflow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("ImportWorkflowDialog", "Destination:", None, -1))
        self.pushButtonLocation.setText(QtWidgets.QApplication.translate("ImportWorkflowDialog", "...", None, -1))

