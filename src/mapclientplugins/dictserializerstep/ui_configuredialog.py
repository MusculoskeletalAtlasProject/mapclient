# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mapclientplugins/dictserializerstep/qt/configuredialog.ui',
# licensing of 'src/mapclientplugins/dictserializerstep/qt/configuredialog.ui' applies.
#
# Created: Wed Jun 26 14:51:29 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        ConfigureDialog.setObjectName("ConfigureDialog")
        ConfigureDialog.resize(418, 303)
        self.gridLayout = QtWidgets.QGridLayout(ConfigureDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.configGroupBox = QtWidgets.QGroupBox(ConfigureDialog)
        self.configGroupBox.setTitle("")
        self.configGroupBox.setObjectName("configGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.label0 = QtWidgets.QLabel(self.configGroupBox)
        self.label0.setObjectName("label0")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label0)
        self.lineEditIdentifier = QtWidgets.QLineEdit(self.configGroupBox)
        self.lineEditIdentifier.setObjectName("lineEditIdentifier")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditIdentifier)
        self.checkBoxDefaultLocation = QtWidgets.QCheckBox(self.configGroupBox)
        self.checkBoxDefaultLocation.setChecked(True)
        self.checkBoxDefaultLocation.setObjectName("checkBoxDefaultLocation")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.checkBoxDefaultLocation)
        self.label0_2 = QtWidgets.QLabel(self.configGroupBox)
        self.label0_2.setObjectName("label0_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label0_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEditOutputLocation = QtWidgets.QLineEdit(self.configGroupBox)
        self.lineEditOutputLocation.setObjectName("lineEditOutputLocation")
        self.horizontalLayout.addWidget(self.lineEditOutputLocation)
        self.pushButtonOutputLocation = QtWidgets.QPushButton(self.configGroupBox)
        self.pushButtonOutputLocation.setObjectName("pushButtonOutputLocation")
        self.horizontalLayout.addWidget(self.pushButtonOutputLocation)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.gridLayout.addWidget(self.configGroupBox, 1, 0, 1, 1)

        self.retranslateUi(ConfigureDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ConfigureDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ConfigureDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigureDialog)

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QtWidgets.QApplication.translate("ConfigureDialog", "ConfigureDialog", None, -1))
        self.label0.setText(QtWidgets.QApplication.translate("ConfigureDialog", "identifier:  ", None, -1))
        self.checkBoxDefaultLocation.setText(QtWidgets.QApplication.translate("ConfigureDialog", "Use output default location", None, -1))
        self.label0_2.setText(QtWidgets.QApplication.translate("ConfigureDialog", "Output:  ", None, -1))
        self.pushButtonOutputLocation.setText(QtWidgets.QApplication.translate("ConfigureDialog", "...", None, -1))

