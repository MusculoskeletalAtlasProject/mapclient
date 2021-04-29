# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pluginmanagerdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_PluginManagerDialog(object):
    def setupUi(self, PluginManagerDialog):
        if not PluginManagerDialog.objectName():
            PluginManagerDialog.setObjectName(u"PluginManagerDialog")
        PluginManagerDialog.resize(567, 496)
        icon = QIcon()
        icon.addFile(u":/mapclient/images/icon-app.png", QSize(), QIcon.Normal, QIcon.Off)
        PluginManagerDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(PluginManagerDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(PluginManagerDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.groupBox.setFlat(False)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.directoryListing = QListWidget(self.groupBox)
        self.directoryListing.setObjectName(u"directoryListing")

        self.verticalLayout_3.addWidget(self.directoryListing)

        self.defaultPluginCheckBox = QCheckBox(self.groupBox)
        self.defaultPluginCheckBox.setObjectName(u"defaultPluginCheckBox")
        self.defaultPluginCheckBox.setChecked(True)

        self.verticalLayout_3.addWidget(self.defaultPluginCheckBox)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.addButton = QPushButton(self.groupBox)
        self.addButton.setObjectName(u"addButton")

        self.verticalLayout_2.addWidget(self.addButton)

        self.removeButton = QPushButton(self.groupBox)
        self.removeButton.setObjectName(u"removeButton")

        self.verticalLayout_2.addWidget(self.removeButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.reloadButton = QPushButton(self.groupBox)
        self.reloadButton.setObjectName(u"reloadButton")

        self.verticalLayout_2.addWidget(self.reloadButton)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.advancedButton = QPushButton(PluginManagerDialog)
        self.advancedButton.setObjectName(u"advancedButton")
        self.advancedButton.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_2.addWidget(self.advancedButton)

        self.horizontalSpacer = QSpacerItem(80, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.buttonBox = QDialogButtonBox(PluginManagerDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(PluginManagerDialog)
        self.buttonBox.accepted.connect(PluginManagerDialog.accept)
        self.buttonBox.rejected.connect(PluginManagerDialog.reject)

        QMetaObject.connectSlotsByName(PluginManagerDialog)
    # setupUi

    def retranslateUi(self, PluginManagerDialog):
        PluginManagerDialog.setWindowTitle(QCoreApplication.translate("PluginManagerDialog", u"Plugin Manager", None))
        self.groupBox.setTitle(QCoreApplication.translate("PluginManagerDialog", u"Plugin Manager", None))
        self.label.setText(QCoreApplication.translate("PluginManagerDialog", u"Plugin directories:", None))
        self.defaultPluginCheckBox.setText(QCoreApplication.translate("PluginManagerDialog", u"Use default plugin directory", None))
        self.addButton.setText(QCoreApplication.translate("PluginManagerDialog", u"Add Directory", None))
        self.removeButton.setText(QCoreApplication.translate("PluginManagerDialog", u"Remove Directory", None))
#if QT_CONFIG(tooltip)
        self.reloadButton.setToolTip(QCoreApplication.translate("PluginManagerDialog", u"Reload the plugins from the current plugin directories", None))
#endif // QT_CONFIG(tooltip)
        self.reloadButton.setText(QCoreApplication.translate("PluginManagerDialog", u"Reload", None))
        self.advancedButton.setText(QCoreApplication.translate("PluginManagerDialog", u"Advanced...", None))
    # retranslateUi

