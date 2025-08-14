# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pluginmanagerdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGroupBox, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_PluginManagerDialog(object):
    def setupUi(self, PluginManagerDialog):
        if not PluginManagerDialog.objectName():
            PluginManagerDialog.setObjectName(u"PluginManagerDialog")
        PluginManagerDialog.resize(567, 496)
        icon = QIcon()
        icon.addFile(u":/mapclient/images/icon-app.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        PluginManagerDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(PluginManagerDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.profileLabel = QLabel(PluginManagerDialog)
        self.profileLabel.setObjectName(u"profileLabel")

        self.horizontalLayout_3.addWidget(self.profileLabel)

        self.profileComboBox = QComboBox(PluginManagerDialog)
        self.profileComboBox.setObjectName(u"profileComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profileComboBox.sizePolicy().hasHeightForWidth())
        self.profileComboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.profileComboBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.profileDeleteButton = QPushButton(PluginManagerDialog)
        self.profileDeleteButton.setObjectName(u"profileDeleteButton")

        self.horizontalLayout_3.addWidget(self.profileDeleteButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.profileEditButton = QPushButton(PluginManagerDialog)
        self.profileEditButton.setObjectName(u"profileEditButton")

        self.horizontalLayout_3.addWidget(self.profileEditButton)

        self.profileNewButton = QPushButton(PluginManagerDialog)
        self.profileNewButton.setObjectName(u"profileNewButton")

        self.horizontalLayout_3.addWidget(self.profileNewButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.groupBox = QGroupBox(PluginManagerDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.groupBox.setFlat(False)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
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


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.addButton = QPushButton(self.groupBox)
        self.addButton.setObjectName(u"addButton")

        self.verticalLayout_2.addWidget(self.addButton)

        self.removeButton = QPushButton(self.groupBox)
        self.removeButton.setObjectName(u"removeButton")

        self.verticalLayout_2.addWidget(self.removeButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.applyButton = QPushButton(self.groupBox)
        self.applyButton.setObjectName(u"applyButton")

        self.verticalLayout_2.addWidget(self.applyButton)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.advancedButton = QPushButton(PluginManagerDialog)
        self.advancedButton.setObjectName(u"advancedButton")
        self.advancedButton.setEnabled(False)
        self.advancedButton.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_2.addWidget(self.advancedButton)

        self.horizontalSpacer = QSpacerItem(80, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.buttonBox = QDialogButtonBox(PluginManagerDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Ok)

        self.horizontalLayout_2.addWidget(self.buttonBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(PluginManagerDialog)
        self.buttonBox.accepted.connect(PluginManagerDialog.accept)
        self.buttonBox.rejected.connect(PluginManagerDialog.reject)

        self.profileNewButton.setDefault(True)


        QMetaObject.connectSlotsByName(PluginManagerDialog)
    # setupUi

    def retranslateUi(self, PluginManagerDialog):
        PluginManagerDialog.setWindowTitle(QCoreApplication.translate("PluginManagerDialog", u"Plugin Manager", None))
        self.profileLabel.setText(QCoreApplication.translate("PluginManagerDialog", u"Profile:", None))
        self.profileDeleteButton.setText(QCoreApplication.translate("PluginManagerDialog", u"Delete", None))
        self.profileEditButton.setText(QCoreApplication.translate("PluginManagerDialog", u"Edit", None))
        self.profileNewButton.setText(QCoreApplication.translate("PluginManagerDialog", u"New", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("PluginManagerDialog", u"Plugin directories:", None))
        self.addButton.setText(QCoreApplication.translate("PluginManagerDialog", u"Add Directory", None))
        self.removeButton.setText(QCoreApplication.translate("PluginManagerDialog", u"Remove Directory", None))
#if QT_CONFIG(tooltip)
        self.applyButton.setToolTip(QCoreApplication.translate("PluginManagerDialog", u"Apply changes and reload the plugins from the current plugin directories", None))
#endif // QT_CONFIG(tooltip)
        self.applyButton.setText(QCoreApplication.translate("PluginManagerDialog", u"Apply", None))
        self.advancedButton.setText(QCoreApplication.translate("PluginManagerDialog", u"Advanced...", None))
    # retranslateUi

