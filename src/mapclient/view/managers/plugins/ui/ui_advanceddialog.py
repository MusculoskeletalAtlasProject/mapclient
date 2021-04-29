# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'advanceddialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_AdvancedDialog(object):
    def setupUi(self, AdvancedDialog):
        if not AdvancedDialog.objectName():
            AdvancedDialog.setObjectName(u"AdvancedDialog")
        AdvancedDialog.resize(573, 481)
        icon = QIcon()
        icon.addFile(u":/mapclient/images/icon-app.png", QSize(), QIcon.Normal, QIcon.Off)
        AdvancedDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(AdvancedDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(AdvancedDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setIconSize(QSize(16, 16))
        self.updatesTab = QWidget()
        self.updatesTab.setObjectName(u"updatesTab")
        self.gridLayout_3 = QGridLayout(self.updatesTab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.updatesTab)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(218, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.analyseButton = QPushButton(self.updatesTab)
        self.analyseButton.setObjectName(u"analyseButton")
        self.analyseButton.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.analyseButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.listWidget = QListWidget(self.updatesTab)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_2.addWidget(self.listWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.updatesTab)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalSpacer_2 = QSpacerItem(118, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.updateAllButton = QPushButton(self.updatesTab)
        self.updateAllButton.setObjectName(u"updateAllButton")

        self.horizontalLayout_2.addWidget(self.updateAllButton)

        self.updateButton = QPushButton(self.updatesTab)
        self.updateButton.setObjectName(u"updateButton")

        self.horizontalLayout_2.addWidget(self.updateButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.updatesTab, "")
        self.dependenciesTab = QWidget()
        self.dependenciesTab.setObjectName(u"dependenciesTab")
        self.gridLayout_4 = QGridLayout(self.dependenciesTab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_8 = QLabel(self.dependenciesTab)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_5.addWidget(self.label_8)

        self.installedPackagesList = QListWidget(self.dependenciesTab)
        self.installedPackagesList.setObjectName(u"installedPackagesList")

        self.verticalLayout_5.addWidget(self.installedPackagesList)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.failedInstallsButton = QPushButton(self.dependenciesTab)
        self.failedInstallsButton.setObjectName(u"failedInstallsButton")
        self.failedInstallsButton.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_9.addWidget(self.failedInstallsButton)

        self.updatePackages = QPushButton(self.dependenciesTab)
        self.updatePackages.setObjectName(u"updatePackages")

        self.horizontalLayout_9.addWidget(self.updatePackages)

        self.uninstallPackages = QPushButton(self.dependenciesTab)
        self.uninstallPackages.setObjectName(u"uninstallPackages")

        self.horizontalLayout_9.addWidget(self.uninstallPackages)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)


        self.horizontalLayout_8.addLayout(self.verticalLayout_5)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_9 = QLabel(self.dependenciesTab)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_11.addWidget(self.label_9)

        self.recommendedPackagesList = QListWidget(self.dependenciesTab)
        self.recommendedPackagesList.setObjectName(u"recommendedPackagesList")

        self.verticalLayout_11.addWidget(self.recommendedPackagesList)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_5)

        self.installPackages = QPushButton(self.dependenciesTab)
        self.installPackages.setObjectName(u"installPackages")

        self.horizontalLayout_10.addWidget(self.installPackages)

        self.packageInformation = QPushButton(self.dependenciesTab)
        self.packageInformation.setObjectName(u"packageInformation")

        self.horizontalLayout_10.addWidget(self.packageInformation)


        self.verticalLayout_11.addLayout(self.horizontalLayout_10)


        self.horizontalLayout_8.addLayout(self.verticalLayout_11)


        self.verticalLayout_10.addLayout(self.horizontalLayout_8)

        self.groupBox_2 = QGroupBox(self.dependenciesTab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.defaultVELocationCheckBox = QCheckBox(self.groupBox_2)
        self.defaultVELocationCheckBox.setObjectName(u"defaultVELocationCheckBox")

        self.horizontalLayout_11.addWidget(self.defaultVELocationCheckBox)

        self.virtualenvCheckBox = QCheckBox(self.groupBox_2)
        self.virtualenvCheckBox.setObjectName(u"virtualenvCheckBox")

        self.horizontalLayout_11.addWidget(self.virtualenvCheckBox)

        self.syntaxUpdatesCheckBox = QCheckBox(self.groupBox_2)
        self.syntaxUpdatesCheckBox.setObjectName(u"syntaxUpdatesCheckBox")

        self.horizontalLayout_11.addWidget(self.syntaxUpdatesCheckBox)


        self.gridLayout_2.addLayout(self.horizontalLayout_11, 0, 0, 1, 1)


        self.verticalLayout_10.addWidget(self.groupBox_2)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_7 = QLabel(self.dependenciesTab)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_12.addWidget(self.label_7)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.virtEnvLocation = QLineEdit(self.dependenciesTab)
        self.virtEnvLocation.setObjectName(u"virtEnvLocation")

        self.horizontalLayout_12.addWidget(self.virtEnvLocation)

        self.modifyVELocation = QPushButton(self.dependenciesTab)
        self.modifyVELocation.setObjectName(u"modifyVELocation")

        self.horizontalLayout_12.addWidget(self.modifyVELocation)


        self.verticalLayout_12.addLayout(self.horizontalLayout_12)


        self.verticalLayout_10.addLayout(self.verticalLayout_12)


        self.gridLayout_4.addLayout(self.verticalLayout_10, 0, 0, 1, 1)

        self.tabWidget.addTab(self.dependenciesTab, "")
        self.optionsTab = QWidget()
        self.optionsTab.setObjectName(u"optionsTab")
        self.verticalLayout_9 = QVBoxLayout(self.optionsTab)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.groupBox = QGroupBox(self.optionsTab)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.revertButton = QPushButton(self.groupBox)
        self.revertButton.setObjectName(u"revertButton")
        self.revertButton.setCheckable(False)
        self.revertButton.setFlat(False)

        self.horizontalLayout_4.addWidget(self.revertButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.ignoreList = QListWidget(self.groupBox)
        self.ignoreList.setObjectName(u"ignoreList")
        self.ignoreList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_3.addWidget(self.ignoreList)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.showPluginErrors = QCheckBox(self.groupBox)
        self.showPluginErrors.setObjectName(u"showPluginErrors")
        self.showPluginErrors.setChecked(True)

        self.gridLayout.addWidget(self.showPluginErrors, 1, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.groupBox)

        self.groupBox1 = QGroupBox(self.optionsTab)
        self.groupBox1.setObjectName(u"groupBox1")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox1)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.syntaxCheckBox = QCheckBox(self.groupBox1)
        self.syntaxCheckBox.setObjectName(u"syntaxCheckBox")
        self.syntaxCheckBox.setChecked(True)

        self.verticalLayout_7.addWidget(self.syntaxCheckBox)

        self.indentCheckBox = QCheckBox(self.groupBox1)
        self.indentCheckBox.setObjectName(u"indentCheckBox")
        self.indentCheckBox.setChecked(True)

        self.verticalLayout_7.addWidget(self.indentCheckBox)

        self.resourceCheckBox = QCheckBox(self.groupBox1)
        self.resourceCheckBox.setObjectName(u"resourceCheckBox")
        self.resourceCheckBox.setChecked(True)

        self.verticalLayout_7.addWidget(self.resourceCheckBox)

        self.locationCheckBox = QCheckBox(self.groupBox1)
        self.locationCheckBox.setObjectName(u"locationCheckBox")
        self.locationCheckBox.setChecked(True)

        self.verticalLayout_7.addWidget(self.locationCheckBox)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_5 = QLabel(self.groupBox1)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_6.addWidget(self.label_5)

        self.resourceList = QListWidget(self.groupBox1)
        self.resourceList.setObjectName(u"resourceList")
        self.resourceList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_6.addWidget(self.resourceList)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineEdit = QLineEdit(self.groupBox1)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_6.addWidget(self.lineEdit)

        self.addResource = QPushButton(self.groupBox1)
        self.addResource.setObjectName(u"addResource")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addResource.sizePolicy().hasHeightForWidth())
        self.addResource.setSizePolicy(sizePolicy)
        self.addResource.setMinimumSize(QSize(0, 0))
        self.addResource.setMaximumSize(QSize(30, 23))

        self.horizontalLayout_6.addWidget(self.addResource)

        self.removeResource = QPushButton(self.groupBox1)
        self.removeResource.setObjectName(u"removeResource")
        sizePolicy.setHeightForWidth(self.removeResource.sizePolicy().hasHeightForWidth())
        self.removeResource.setSizePolicy(sizePolicy)
        self.removeResource.setMinimumSize(QSize(0, 0))
        self.removeResource.setMaximumSize(QSize(30, 23))

        self.horizontalLayout_6.addWidget(self.removeResource)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)


        self.verticalLayout_8.addLayout(self.verticalLayout_6)


        self.horizontalLayout_7.addWidget(self.groupBox1)


        self.verticalLayout_9.addLayout(self.horizontalLayout_7)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.optionsTab)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_4.addWidget(self.label_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.dir2to3 = QLineEdit(self.optionsTab)
        self.dir2to3.setObjectName(u"dir2to3")

        self.horizontalLayout_5.addWidget(self.dir2to3)

        self.locateButton = QPushButton(self.optionsTab)
        self.locateButton.setObjectName(u"locateButton")

        self.horizontalLayout_5.addWidget(self.locateButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)


        self.verticalLayout_9.addLayout(self.verticalLayout_4)

        self.tabWidget.addTab(self.optionsTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.buttonBox = QDialogButtonBox(AdvancedDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_3.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(AdvancedDialog)
        self.buttonBox.accepted.connect(AdvancedDialog.accept)
        self.buttonBox.rejected.connect(AdvancedDialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AdvancedDialog)
    # setupUi

    def retranslateUi(self, AdvancedDialog):
        AdvancedDialog.setWindowTitle(QCoreApplication.translate("AdvancedDialog", u"Advanced", None))
        self.label.setText(QCoreApplication.translate("AdvancedDialog", u"Plugins:", None))
#if QT_CONFIG(whatsthis)
        self.analyseButton.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.analyseButton.setText(QCoreApplication.translate("AdvancedDialog", u"Analyse Plugins", None))
        self.label_2.setText("")
        self.updateAllButton.setText(QCoreApplication.translate("AdvancedDialog", u"Update All", None))
        self.updateButton.setText(QCoreApplication.translate("AdvancedDialog", u"Update", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.updatesTab), QCoreApplication.translate("AdvancedDialog", u"Updates", None))
        self.label_8.setText(QCoreApplication.translate("AdvancedDialog", u"Installed Packages:", None))
        self.failedInstallsButton.setText(QCoreApplication.translate("AdvancedDialog", u"Failed Installs...", None))
        self.updatePackages.setText(QCoreApplication.translate("AdvancedDialog", u"Update", None))
        self.uninstallPackages.setText(QCoreApplication.translate("AdvancedDialog", u"Uninstall", None))
        self.label_9.setText(QCoreApplication.translate("AdvancedDialog", u"Recommended Packages:", None))
        self.installPackages.setText(QCoreApplication.translate("AdvancedDialog", u"Install", None))
        self.packageInformation.setText(QCoreApplication.translate("AdvancedDialog", u"Information", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("AdvancedDialog", u"Dependency Settings", None))
        self.defaultVELocationCheckBox.setText(QCoreApplication.translate("AdvancedDialog", u"Automatically check for updates", None))
        self.virtualenvCheckBox.setText(QCoreApplication.translate("AdvancedDialog", u"Double-click for documentation", None))
        self.syntaxUpdatesCheckBox.setText(QCoreApplication.translate("AdvancedDialog", u"Check for syntax updates", None))
        self.label_7.setText(QCoreApplication.translate("AdvancedDialog", u"Virtual Environment Location:", None))
        self.modifyVELocation.setText(QCoreApplication.translate("AdvancedDialog", u"Modify", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dependenciesTab), QCoreApplication.translate("AdvancedDialog", u"Dependencies", None))
        self.groupBox.setTitle(QCoreApplication.translate("AdvancedDialog", u"Plugin Error Settings", None))
        self.label_3.setText(QCoreApplication.translate("AdvancedDialog", u"Ignored Plugins:", None))
        self.revertButton.setText(QCoreApplication.translate("AdvancedDialog", u"Revert", None))
        self.showPluginErrors.setText(QCoreApplication.translate("AdvancedDialog", u"Show Plugin Errors Dialog", None))
        self.groupBox1.setTitle(QCoreApplication.translate("AdvancedDialog", u"Plugin Updater Settings", None))
        self.syntaxCheckBox.setText(QCoreApplication.translate("AdvancedDialog", u"Syntax updates", None))
        self.indentCheckBox.setText(QCoreApplication.translate("AdvancedDialog", u"Indentation updates", None))
        self.resourceCheckBox.setText(QCoreApplication.translate("AdvancedDialog", u"Resource updates", None))
        self.locationCheckBox.setText(QCoreApplication.translate("AdvancedDialog", u"Location updates", None))
        self.label_5.setText(QCoreApplication.translate("AdvancedDialog", u"Resource Filenames:", None))
        self.addResource.setText(QCoreApplication.translate("AdvancedDialog", u"+", None))
        self.removeResource.setText(QCoreApplication.translate("AdvancedDialog", u"-", None))
        self.label_4.setText(QCoreApplication.translate("AdvancedDialog", u"2to3.py Location:", None))
        self.locateButton.setText(QCoreApplication.translate("AdvancedDialog", u"...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.optionsTab), QCoreApplication.translate("AdvancedDialog", u"Options", None))
    # retranslateUi

