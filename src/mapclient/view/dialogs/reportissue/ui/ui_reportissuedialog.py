# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reportissuedialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ReportIssueDialog(object):
    def setupUi(self, ReportIssueDialog):
        if not ReportIssueDialog.objectName():
            ReportIssueDialog.setObjectName(u"ReportIssueDialog")
        ReportIssueDialog.resize(650, 400)
        self.verticalLayout = QVBoxLayout(ReportIssueDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_2 = QFrame(ReportIssueDialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.description = QLabel(self.frame_2)
        self.description.setObjectName(u"description")
        self.description.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.description.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.description)

        self.wrike_description = QLabel(self.frame_2)
        self.wrike_description.setObjectName(u"wrike_description")
        self.wrike_description.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.wrike_description)

        self.description_2 = QLabel(self.frame_2)
        self.description_2.setObjectName(u"description_2")
        self.description_2.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.description_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame = QFrame(ReportIssueDialog)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.github_issue_button = QPushButton(self.frame)
        self.github_issue_button.setObjectName(u"github_issue_button")

        self.horizontalLayout.addWidget(self.github_issue_button)

        self.wrike_ticket_button = QPushButton(self.frame)
        self.wrike_ticket_button.setObjectName(u"wrike_ticket_button")

        self.horizontalLayout.addWidget(self.wrike_ticket_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.close_button = QPushButton(self.frame)
        self.close_button.setObjectName(u"close_button")

        self.horizontalLayout.addWidget(self.close_button)


        self.verticalLayout.addWidget(self.frame)


        self.retranslateUi(ReportIssueDialog)
        self.close_button.clicked.connect(ReportIssueDialog.close)

        QMetaObject.connectSlotsByName(ReportIssueDialog)
    # setupUi

    def retranslateUi(self, ReportIssueDialog):
        ReportIssueDialog.setWindowTitle(QCoreApplication.translate("ReportIssueDialog", u"Report Issue", None))
        self.description.setText(QCoreApplication.translate("ReportIssueDialog", u"<p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Issue Reporting</span></p>\n"
"\n"
"<p align=\"justify\">If you have encountered an issue with the Mapping-Tools, please consider submitting an issue report using one of the following methods:</p>\n"
"\n"
"<p align=\"justify\" style=\"margin-left:20; margin-right:20;\">\n"
"\n"
"If possible, we recommend submitting an issue in the <a href=\"https://github.com/MusculoskeletalAtlasProject/mapclient\">MAP-Client</a> GitHub repository. This is our primary location for all issues related to the MAP-Client and Mapping-Tools. Once you have submitted an issue, the MAP-Client developers will be notified and you can use the issue page to track any progress made in response to your submission. Note that you will need a GitHub account for this method.\n"
"\n"
"</p>\n"
"", None))
        self.wrike_description.setText(QCoreApplication.translate("ReportIssueDialog", u"<p align=\"justify\" style=\"margin-left:20; margin-right:20;\">\n"
"\n"
"If you are a member of the SPARC Wrike group, you may also wish to submit a request for a Wrike ticket using the link provided below.\n"
"\n"
"</p>\n"
"", None))
        self.description_2.setText(QCoreApplication.translate("ReportIssueDialog", u"<p align=\"justify\" style=\"margin-left:20; margin-right:20;\">\n"
"\n"
"Alternatively, it is also possible to report an issue by email if you'd prefer. Please direct your messages to <i>support@sparc.science</i> for any issues or questions you have in regards to the MAP-Client.\n"
"\n"
"<br/></p>\n"
"\n"
"<p align=\"justify\">Make sure to provide a description of the issue or error that you have encountered, including any steps that may be required to reproduce it. If possible, please also include any relevant error messages. Note that the MAP-Client keeps a log of the current session if you need to review any error messages or related application events. A copy of this log can be accessed within the MAP-Client under <i>View -> Log Information</i>. If the error occurred during the execution of a plugin step, please include the name of the plugin in your report.</p>", None))
        self.github_issue_button.setText(QCoreApplication.translate("ReportIssueDialog", u"GitHub Issue", None))
        self.wrike_ticket_button.setText(QCoreApplication.translate("ReportIssueDialog", u"Wrike Ticket", None))
        self.close_button.setText(QCoreApplication.translate("ReportIssueDialog", u"Close", None))
    # retranslateUi

