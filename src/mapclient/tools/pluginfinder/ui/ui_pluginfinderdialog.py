# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pluginfinderdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QHeaderView, QLineEdit, QSizePolicy, QSplitter,
    QVBoxLayout, QWidget)

from mapclient.tools.pluginfinder.plugindata import PluginTreeView

class Ui_PluginFinderDialog(object):
    def setupUi(self, PluginFinderDialog):
        if not PluginFinderDialog.objectName():
            PluginFinderDialog.setObjectName(u"PluginFinderDialog")
        PluginFinderDialog.resize(900, 550)
        self.verticalLayout = QVBoxLayout(PluginFinderDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(PluginFinderDialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget_2 = QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lineEditFilter = QLineEdit(self.layoutWidget_2)
        self.lineEditFilter.setObjectName(u"lineEditFilter")

        self.verticalLayout_2.addWidget(self.lineEditFilter)

        self.stepTreeView = PluginTreeView(self.layoutWidget_2)
        self.stepTreeView.setObjectName(u"stepTreeView")
        self.stepTreeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.stepTreeView.setDragEnabled(True)
        self.stepTreeView.setSelectionMode(QAbstractItemView.NoSelection)
        self.stepTreeView.setIconSize(QSize(64, 64))
        self.stepTreeView.setIndentation(0)
        self.stepTreeView.setRootIsDecorated(False)
        self.stepTreeView.setSortingEnabled(False)
        self.stepTreeView.setHeaderHidden(True)
        self.stepTreeView.setExpandsOnDoubleClick(False)

        self.verticalLayout_2.addWidget(self.stepTreeView)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.splitter.addWidget(self.layoutWidget_2)

        self.verticalLayout.addWidget(self.splitter)


        self.retranslateUi(PluginFinderDialog)

        QMetaObject.connectSlotsByName(PluginFinderDialog)
    # setupUi

    def retranslateUi(self, PluginFinderDialog):
        PluginFinderDialog.setWindowTitle(QCoreApplication.translate("PluginFinderDialog", u"Plugin Finder Tool", None))
        self.lineEditFilter.setText("")
        self.lineEditFilter.setPlaceholderText(QCoreApplication.translate("PluginFinderDialog", u"Filter", None))
    # retranslateUi

