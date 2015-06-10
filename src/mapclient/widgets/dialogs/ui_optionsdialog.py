# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/optionsdialog.ui'
#
# Created: Fri May 29 14:31:23 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        OptionsDialog.setObjectName("OptionsDialog")
        OptionsDialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(OptionsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(OptionsDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tabGeneral = QtGui.QWidget()
        self.tabGeneral.setObjectName("tabGeneral")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabGeneral)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBoxShowStepNames = QtGui.QCheckBox(self.tabGeneral)
        self.checkBoxShowStepNames.setChecked(True)
        self.checkBoxShowStepNames.setObjectName("checkBoxShowStepNames")
        self.verticalLayout_2.addWidget(self.checkBoxShowStepNames)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.tabWidget.addTab(self.tabGeneral, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(OptionsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(OptionsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), OptionsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), OptionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

    def retranslateUi(self, OptionsDialog):
        OptionsDialog.setWindowTitle(QtGui.QApplication.translate("OptionsDialog", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowStepNames.setText(QtGui.QApplication.translate("OptionsDialog", "Show step names", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabGeneral), QtGui.QApplication.translate("OptionsDialog", "&General", None, QtGui.QApplication.UnicodeUTF8))

