# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginformation.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_LogInformation(object):
    def setupUi(self, LogInformation):
        if not LogInformation.objectName():
            LogInformation.setObjectName(u"LogInformation")
        LogInformation.resize(645, 534)
        LogInformation.setMinimumSize(QSize(600, 450))
        LogInformation.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_2 = QGridLayout(LogInformation)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.history = QLabel(LogInformation)
        self.history.setObjectName(u"history")

        self.gridLayout.addWidget(self.history, 0, 0, 1, 1)

        self.information_table = QTableWidget(LogInformation)
        if (self.information_table.columnCount() < 5):
            self.information_table.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter);
        self.information_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter);
        self.information_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.information_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter);
        self.information_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.information_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.information_table.setObjectName(u"information_table")
        self.information_table.setEnabled(True)
        self.information_table.setMouseTracking(False)
        self.information_table.setAutoFillBackground(False)
        self.information_table.setInputMethodHints(Qt.ImhNone)
        self.information_table.setFrameShadow(QFrame.Raised)
        self.information_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.information_table.setTabKeyNavigation(False)
        self.information_table.setProperty("showDropIndicator", False)
        self.information_table.setDragDropOverwriteMode(False)
        self.information_table.setAlternatingRowColors(False)
        self.information_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.information_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.information_table.setShowGrid(False)
        self.information_table.setGridStyle(Qt.NoPen)
        self.information_table.setSortingEnabled(True)
        self.information_table.setCornerButtonEnabled(False)
        self.information_table.setRowCount(0)
        self.information_table.setColumnCount(5)
        self.information_table.horizontalHeader().setVisible(True)
        self.information_table.horizontalHeader().setCascadingSectionResizes(True)
        self.information_table.horizontalHeader().setMinimumSectionSize(75)
        self.information_table.horizontalHeader().setDefaultSectionSize(75)
        self.information_table.horizontalHeader().setHighlightSections(True)
        self.information_table.horizontalHeader().setProperty("showSortIndicator", True)
        self.information_table.horizontalHeader().setStretchLastSection(True)
        self.information_table.verticalHeader().setVisible(False)
        self.information_table.verticalHeader().setMinimumSectionSize(15)
        self.information_table.verticalHeader().setDefaultSectionSize(20)
        self.information_table.verticalHeader().setHighlightSections(False)

        self.gridLayout.addWidget(self.information_table, 1, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.loadButton = QPushButton(LogInformation)
        self.loadButton.setObjectName(u"loadButton")

        self.horizontalLayout.addWidget(self.loadButton)

        self.detailsButton = QPushButton(LogInformation)
        self.detailsButton.setObjectName(u"detailsButton")

        self.horizontalLayout.addWidget(self.detailsButton)

        self.horizontalSpacer = QSpacerItem(328, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.closeWindowButton = QPushButton(LogInformation)
        self.closeWindowButton.setObjectName(u"closeWindowButton")

        self.horizontalLayout.addWidget(self.closeWindowButton)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)


        self.retranslateUi(LogInformation)
        self.closeWindowButton.clicked.connect(LogInformation.close)

        QMetaObject.connectSlotsByName(LogInformation)
    # setupUi

    def retranslateUi(self, LogInformation):
        LogInformation.setWindowTitle(QCoreApplication.translate("LogInformation", u"Logged Information", None))
        self.history.setText(QCoreApplication.translate("LogInformation", u"History:", None))
        ___qtablewidgetitem = self.information_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("LogInformation", u"Date", None));
        ___qtablewidgetitem1 = self.information_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("LogInformation", u"Time", None));
        ___qtablewidgetitem2 = self.information_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("LogInformation", u"Location", None));
        ___qtablewidgetitem3 = self.information_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("LogInformation", u"Level", None));
        ___qtablewidgetitem4 = self.information_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("LogInformation", u"Description", None));
        self.loadButton.setText(QCoreApplication.translate("LogInformation", u"Load", None))
        self.detailsButton.setText(QCoreApplication.translate("LogInformation", u"Details", None))
        self.closeWindowButton.setText(QCoreApplication.translate("LogInformation", u"Close", None))
    # retranslateUi

