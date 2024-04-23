# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'logdetails.ui'
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
    QHeaderView, QSizePolicy, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_LogDetails(object):
    def setupUi(self, LogDetails):
        if not LogDetails.objectName():
            LogDetails.setObjectName(u"LogDetails")
        LogDetails.resize(655, 310)
        LogDetails.setMinimumSize(QSize(350, 150))
        LogDetails.setSizeGripEnabled(False)
        self.horizontalLayout = QHBoxLayout(LogDetails)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.detailedTable = QTableWidget(LogDetails)
        if (self.detailedTable.rowCount() < 5):
            self.detailedTable.setRowCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeft|Qt.AlignVCenter);
        self.detailedTable.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignLeft|Qt.AlignVCenter);
        self.detailedTable.setVerticalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignLeft|Qt.AlignVCenter);
        self.detailedTable.setVerticalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignLeft|Qt.AlignVCenter);
        self.detailedTable.setVerticalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignLeft|Qt.AlignTop);
        self.detailedTable.setVerticalHeaderItem(4, __qtablewidgetitem4)
        self.detailedTable.setObjectName(u"detailedTable")
        self.detailedTable.setAutoScroll(True)
        self.detailedTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.detailedTable.setTabKeyNavigation(False)
        self.detailedTable.setProperty("showDropIndicator", False)
        self.detailedTable.setDragDropOverwriteMode(False)
        self.detailedTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.detailedTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.detailedTable.setShowGrid(False)
        self.detailedTable.setCornerButtonEnabled(False)
        self.detailedTable.setRowCount(5)
        self.detailedTable.horizontalHeader().setVisible(False)
        self.detailedTable.horizontalHeader().setStretchLastSection(True)
        self.detailedTable.verticalHeader().setDefaultSectionSize(20)
        self.detailedTable.verticalHeader().setStretchLastSection(True)

        self.horizontalLayout.addWidget(self.detailedTable)


        self.retranslateUi(LogDetails)

        QMetaObject.connectSlotsByName(LogDetails)
    # setupUi

    def retranslateUi(self, LogDetails):
        LogDetails.setWindowTitle(QCoreApplication.translate("LogDetails", u"Details", None))
        ___qtablewidgetitem = self.detailedTable.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("LogDetails", u"Date:", None));
        ___qtablewidgetitem1 = self.detailedTable.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("LogDetails", u"Time:", None));
        ___qtablewidgetitem2 = self.detailedTable.verticalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("LogDetails", u"Source:", None));
        ___qtablewidgetitem3 = self.detailedTable.verticalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("LogDetails", u"Level:", None));
        ___qtablewidgetitem4 = self.detailedTable.verticalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("LogDetails", u"Description:", None));
    # retranslateUi

