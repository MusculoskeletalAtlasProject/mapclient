from urllib.parse import quote_plus

from PySide6 import QtWidgets

from mapclient.view.dialogs.reportissue.utils import create_github_issue


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, title, text, parent=None):
        super().__init__(parent=parent)
        self._text = text

        critical_icon = QtWidgets.QMessageBox.standardIcon(QtWidgets.QMessageBox.Icon.Critical)
        layout = QtWidgets.QVBoxLayout()

        # Create and add the icon.
        critical_icon_label = QtWidgets.QLabel()
        critical_icon_label.setPixmap(critical_icon)
        layout.addWidget(critical_icon_label)

        # Create text.
        label = QtWidgets.QLabel(text)
        label.setWordWrap(True)
        layout.addWidget(label)

        # Create buttons.
        button_layout = QtWidgets.QHBoxLayout()
        github_issue_button = QtWidgets.QPushButton("Submit GitHub Issue")
        spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding)
        ok_button = QtWidgets.QPushButton("OK")
        button_layout.addWidget(github_issue_button)
        button_layout.addSpacerItem(spacer)
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)
        ok_button.clicked.connect(self.accept)
        github_issue_button.clicked.connect(self._create_github_issue)

        self.setWindowTitle(title)
        self.setWindowIcon(critical_icon)
        self.setLayout(layout)

    def _create_github_issue(self):
        text = "<Describe steps to reproduce the error here>\n\n```\n" + self._text + "```"
        create_github_issue(quote_plus(text))
