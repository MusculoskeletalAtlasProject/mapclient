from PySide6 import QtWidgets

from mapclient.core.utils import is_mapping_tools
from mapclient.view.dialogs.reportissue.utils import create_github_issue, create_wrike_ticket
from mapclient.view.dialogs.reportissue.ui.ui_reportissuedialog import Ui_ReportIssueDialog


class ReportIssueDialog(QtWidgets.QDialog):
    """
    Dialog with instructions on how and where to report issues in the MAP-Client.
    """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_ReportIssueDialog()
        self._ui.setupUi(self)
        self._make_connections()
        self._check_variant()

    def _make_connections(self):
        self._ui.github_issue_button.clicked.connect(_create_github_issue)
        self._ui.wrike_ticket_button.clicked.connect(create_wrike_ticket)

    def _check_variant(self):
        if not is_mapping_tools():
            self._ui.wrike_description.hide()
            self._ui.wrike_ticket_button.hide()


def _create_github_issue():
    create_github_issue()
