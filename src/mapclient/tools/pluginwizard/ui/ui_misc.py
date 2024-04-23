# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'misc.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QWidget)

class Ui_Misc(object):
    def setupUi(self, Misc):
        if not Misc.objectName():
            Misc.setObjectName(u"Misc")
        Misc.resize(400, 300)
        self.formLayout = QFormLayout(Misc)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Misc)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.authorNameLineEdit = QLineEdit(Misc)
        self.authorNameLineEdit.setObjectName(u"authorNameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.authorNameLineEdit)

        self.label_2 = QLabel(Misc)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.categoryLineEdit = QLineEdit(Misc)
        self.categoryLineEdit.setObjectName(u"categoryLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.categoryLineEdit)

        self.label_3 = QLabel(Misc)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.pluginLocationEdit = QLineEdit(Misc)
        self.pluginLocationEdit.setObjectName(u"pluginLocationEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.pluginLocationEdit)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.authorNameLineEdit)
        self.label_2.setBuddy(self.categoryLineEdit)
        self.label_3.setBuddy(self.pluginLocationEdit)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(Misc)

        QMetaObject.connectSlotsByName(Misc)
    # setupUi

    def retranslateUi(self, Misc):
        Misc.setWindowTitle(QCoreApplication.translate("Misc", u"Form", None))
        self.label.setText(QCoreApplication.translate("Misc", u"Author name(s):  ", None))
        self.authorNameLineEdit.setPlaceholderText(QCoreApplication.translate("Misc", u"Xxxx Yyyyy", None))
        self.label_2.setText(QCoreApplication.translate("Misc", u"Category:  ", None))
        self.categoryLineEdit.setPlaceholderText(QCoreApplication.translate("Misc", u"General", None))
        self.label_3.setText(QCoreApplication.translate("Misc", u"Plugin Location:", None))
        self.pluginLocationEdit.setPlaceholderText(QCoreApplication.translate("Misc", u"eg. https://github.com.../archive/master.zip", None))
    # retranslateUi

