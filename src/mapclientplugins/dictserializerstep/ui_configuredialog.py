# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/configuredialog.ui'
#
# Created: Thu Jun 25 09:17:51 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        ConfigureDialog.setObjectName("ConfigureDialog")
        ConfigureDialog.resize(418, 303)
        self.gridLayout = QtGui.QGridLayout(ConfigureDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.configGroupBox = QtGui.QGroupBox(ConfigureDialog)
        self.configGroupBox.setTitle("")
        self.configGroupBox.setObjectName("configGroupBox")
        self.formLayout = QtGui.QFormLayout(self.configGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.label0 = QtGui.QLabel(self.configGroupBox)
        self.label0.setObjectName("label0")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label0)
        self.lineEditIdentifier = QtGui.QLineEdit(self.configGroupBox)
        self.lineEditIdentifier.setObjectName("lineEditIdentifier")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEditIdentifier)
        self.checkBoxDefaultLocation = QtGui.QCheckBox(self.configGroupBox)
        self.checkBoxDefaultLocation.setChecked(True)
        self.checkBoxDefaultLocation.setObjectName("checkBoxDefaultLocation")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBoxDefaultLocation)
        self.label0_2 = QtGui.QLabel(self.configGroupBox)
        self.label0_2.setObjectName("label0_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label0_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEditOutputLocation = QtGui.QLineEdit(self.configGroupBox)
        self.lineEditOutputLocation.setObjectName("lineEditOutputLocation")
        self.horizontalLayout.addWidget(self.lineEditOutputLocation)
        self.pushButtonOutputLocation = QtGui.QPushButton(self.configGroupBox)
        self.pushButtonOutputLocation.setObjectName("pushButtonOutputLocation")
        self.horizontalLayout.addWidget(self.pushButtonOutputLocation)
        self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.gridLayout.addWidget(self.configGroupBox, 1, 0, 1, 1)

        self.retranslateUi(ConfigureDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ConfigureDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ConfigureDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigureDialog)

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QtGui.QApplication.translate("ConfigureDialog", "ConfigureDialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label0.setText(QtGui.QApplication.translate("ConfigureDialog", "identifier:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxDefaultLocation.setText(QtGui.QApplication.translate("ConfigureDialog", "Use output default location", None, QtGui.QApplication.UnicodeUTF8))
        self.label0_2.setText(QtGui.QApplication.translate("ConfigureDialog", "Output:  ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonOutputLocation.setText(QtGui.QApplication.translate("ConfigureDialog", "...", None, QtGui.QApplication.UnicodeUTF8))

