# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/settingswidget.ui'
#
# Created: Tue Mar  3 09:56:53 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SettingsWidget(object):
    def setupUi(self, SettingsWidget):
        SettingsWidget.setObjectName("SettingsWidget")
        SettingsWidget.resize(498, 476)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SettingsWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtGui.QLabel(SettingsWidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.hostListView = QtGui.QListView(SettingsWidget)
        self.hostListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.hostListView.setObjectName("hostListView")
        self.horizontalLayout.addWidget(self.hostListView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addPushButton = QtGui.QPushButton(SettingsWidget)
        self.addPushButton.setObjectName("addPushButton")
        self.verticalLayout.addWidget(self.addPushButton)
        self.removePushButton = QtGui.QPushButton(SettingsWidget)
        self.removePushButton.setObjectName("removePushButton")
        self.verticalLayout.addWidget(self.removePushButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.actionAddHost = QtGui.QAction(SettingsWidget)
        self.actionAddHost.setObjectName("actionAddHost")

        self.retranslateUi(SettingsWidget)
        QtCore.QMetaObject.connectSlotsByName(SettingsWidget)

    def retranslateUi(self, SettingsWidget):
        SettingsWidget.setWindowTitle(QtGui.QApplication.translate("SettingsWidget", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SettingsWidget", "Host list:", None, QtGui.QApplication.UnicodeUTF8))
        self.addPushButton.setText(QtGui.QApplication.translate("SettingsWidget", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removePushButton.setText(QtGui.QApplication.translate("SettingsWidget", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddHost.setText(QtGui.QApplication.translate("SettingsWidget", "Add Host", None, QtGui.QApplication.UnicodeUTF8))

