# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mapclientplugins/filechooserstep/qt/configuredialog.ui',
# licensing of 'src/mapclientplugins/filechooserstep/qt/configuredialog.ui' applies.
#
# Created: Wed Jun 26 14:52:09 2019
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
        self.configGroupBox = QtWidgets.QGroupBox(ConfigureDialog)
        self.configGroupBox.setTitle("")
        self.configGroupBox.setObjectName("configGroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.configGroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label0 = QtWidgets.QLabel(self.configGroupBox)
        self.label0.setObjectName("label0")
        self.gridLayout_2.addWidget(self.label0, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEditFileLocation = QtWidgets.QLineEdit(self.configGroupBox)
        self.lineEditFileLocation.setObjectName("lineEditFileLocation")
        self.horizontalLayout.addWidget(self.lineEditFileLocation)
        self.pushButtonFileChooser = QtWidgets.QPushButton(self.configGroupBox)
        self.pushButtonFileChooser.setObjectName("pushButtonFileChooser")
        self.horizontalLayout.addWidget(self.pushButtonFileChooser)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.lineEdit0 = QtWidgets.QLineEdit(self.configGroupBox)
        self.lineEdit0.setObjectName("lineEdit0")
        self.gridLayout_2.addWidget(self.lineEdit0, 0, 1, 1, 1)
        self.label1 = QtWidgets.QLabel(self.configGroupBox)
        self.label1.setObjectName("label1")
        self.gridLayout_2.addWidget(self.label1, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.configGroupBox, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ConfigureDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ConfigureDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ConfigureDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigureDialog)

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QtWidgets.QApplication.translate("ConfigureDialog", "ConfigureDialog", None, -1))
        self.label0.setText(QtWidgets.QApplication.translate("ConfigureDialog", "identifier:  ", None, -1))
        self.pushButtonFileChooser.setText(QtWidgets.QApplication.translate("ConfigureDialog", "...", None, -1))
        self.label1.setText(QtWidgets.QApplication.translate("ConfigureDialog", "File:  ", None, -1))

