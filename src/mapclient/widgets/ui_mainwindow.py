# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/mainwindow.ui'
#
# Created: Thu Jul 10 13:19:59 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/mapclient/images/icon-app.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName("action_About")
        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.actionPluginManager = QtGui.QAction(MainWindow)
        self.actionPluginManager.setObjectName("actionPluginManager")
        self.actionPMR = QtGui.QAction(MainWindow)
        self.actionPMR.setObjectName("actionPMR")
        self.actionAnnotation = QtGui.QAction(MainWindow)
        self.actionAnnotation.setObjectName("actionAnnotation")
        self.actionPluginWizard = QtGui.QAction(MainWindow)
        self.actionPluginWizard.setObjectName("actionPluginWizard")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MAP Client", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setStatusTip(QtGui.QApplication.translate("MainWindow", "Quit the application", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPluginManager.setText(QtGui.QApplication.translate("MainWindow", "Plugin &Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPMR.setText(QtGui.QApplication.translate("MainWindow", "&PMR", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAnnotation.setText(QtGui.QApplication.translate("MainWindow", "&Annotation", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPluginWizard.setText(QtGui.QApplication.translate("MainWindow", "Plugin Wi&zard", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
