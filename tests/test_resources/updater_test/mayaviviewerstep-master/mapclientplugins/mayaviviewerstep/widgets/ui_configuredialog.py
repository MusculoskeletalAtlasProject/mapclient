# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuredialog.ui'
#
# Created: Thu Oct 24 14:38:01 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ConfigureDialog(object):
    def setupUi(self, ConfigureDialog):
        ConfigureDialog.setObjectName("ConfigureDialog")
        ConfigureDialog.resize(593, 253)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ConfigureDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(ConfigureDialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.renderArgsLineEdit = QtGui.QLineEdit(self.groupBox)
        self.renderArgsLineEdit.setObjectName("renderArgsLineEdit")
        self.gridLayout.addWidget(self.renderArgsLineEdit, 3, 1, 1, 1)
        self.renderArgsLabel = QtGui.QLabel(self.groupBox)
        self.renderArgsLabel.setObjectName("renderArgsLabel")
        self.gridLayout.addWidget(self.renderArgsLabel, 3, 0, 1, 1)
        self.identifierLineEdit = QtGui.QLineEdit(self.groupBox)
        self.identifierLineEdit.setObjectName("identifierLineEdit")
        self.gridLayout.addWidget(self.identifierLineEdit, 0, 1, 1, 1)
        self.discretisationLabel = QtGui.QLabel(self.groupBox)
        self.discretisationLabel.setMinimumSize(QtCore.QSize(71, 0))
        self.discretisationLabel.setToolTip("")
        self.discretisationLabel.setObjectName("discretisationLabel")
        self.gridLayout.addWidget(self.discretisationLabel, 1, 0, 1, 1)
        self.displayNodeLabel = QtGui.QLabel(self.groupBox)
        self.displayNodeLabel.setMinimumSize(QtCore.QSize(71, 0))
        self.displayNodeLabel.setObjectName("displayNodeLabel")
        self.gridLayout.addWidget(self.displayNodeLabel, 2, 0, 1, 1)
        self.identifierLabel = QtGui.QLabel(self.groupBox)
        self.identifierLabel.setObjectName("identifierLabel")
        self.gridLayout.addWidget(self.identifierLabel, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.displayNodesCheckBox = QtGui.QCheckBox(self.groupBox)
        self.displayNodesCheckBox.setText("")
        self.displayNodesCheckBox.setObjectName("displayNodesCheckBox")
        self.gridLayout.addWidget(self.displayNodesCheckBox, 2, 1, 1, 1)
        self.discretisationLineEdit = QtGui.QLineEdit(self.groupBox)
        self.discretisationLineEdit.setObjectName("discretisationLineEdit")
        self.gridLayout.addWidget(self.discretisationLineEdit, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(ConfigureDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.identifierLabel.setBuddy(self.identifierLineEdit)

        self.retranslateUi(ConfigureDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ConfigureDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ConfigureDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfigureDialog)

    def retranslateUi(self, ConfigureDialog):
        ConfigureDialog.setWindowTitle(QtGui.QApplication.translate("ConfigureDialog", "Configure - Mayavi Model Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.renderArgsLineEdit.setText(QtGui.QApplication.translate("ConfigureDialog", "{\'color\':\'bone\'}", None, QtGui.QApplication.UnicodeUTF8))
        self.renderArgsLabel.setText(QtGui.QApplication.translate("ConfigureDialog", "Render Args:", None, QtGui.QApplication.UnicodeUTF8))
        self.discretisationLabel.setText(QtGui.QApplication.translate("ConfigureDialog", "Discretisation:", None, QtGui.QApplication.UnicodeUTF8))
        self.displayNodeLabel.setText(QtGui.QApplication.translate("ConfigureDialog", "Display Nodes:", None, QtGui.QApplication.UnicodeUTF8))
        self.identifierLabel.setText(QtGui.QApplication.translate("ConfigureDialog", "Identifier:", None, QtGui.QApplication.UnicodeUTF8))
        self.discretisationLineEdit.setText(QtGui.QApplication.translate("ConfigureDialog", "5x5", None, QtGui.QApplication.UnicodeUTF8))

