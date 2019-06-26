# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/mapclient/view/qt/mainwindow.ui',
# licensing of 'src/mapclient/view/qt/mainwindow.ui' applies.
#
# Created: Wed Jun 26 11:07:29 2019
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/mapclient/images/icon-app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.action_Quit = QtWidgets.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.actionPluginManager = QtWidgets.QAction(MainWindow)
        self.actionPluginManager.setObjectName("actionPluginManager")
        self.actionPMR = QtWidgets.QAction(MainWindow)
        self.actionPMR.setObjectName("actionPMR")
        self.actionAnnotation = QtWidgets.QAction(MainWindow)
        self.actionAnnotation.setObjectName("actionAnnotation")
        self.actionPluginWizard = QtWidgets.QAction(MainWindow)
        self.actionPluginWizard.setObjectName("actionPluginWizard")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MAP Client", None, -1))
        self.action_About.setText(QtWidgets.QApplication.translate("MainWindow", "&About", None, -1))
        self.action_Quit.setText(QtWidgets.QApplication.translate("MainWindow", "&Quit", None, -1))
        self.action_Quit.setStatusTip(QtWidgets.QApplication.translate("MainWindow", "Quit the application", None, -1))
        self.action_Quit.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Q", None, -1))
        self.actionPluginManager.setText(QtWidgets.QApplication.translate("MainWindow", "Plugin &Manager", None, -1))
        self.actionPMR.setText(QtWidgets.QApplication.translate("MainWindow", "&PMR", None, -1))
        self.actionAnnotation.setText(QtWidgets.QApplication.translate("MainWindow", "&Annotation", None, -1))
        self.actionPluginWizard.setText(QtWidgets.QApplication.translate("MainWindow", "Plugin Wi&zard", None, -1))

from . import resources_rc
