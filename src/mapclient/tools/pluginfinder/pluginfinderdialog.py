"""
This tool is used to search for new MAP Client plugins.

Author: Timothy Salemink
"""

import logging

from PySide2 import QtCore
from PySide2.QtWidgets import QDialog

from utils.plugindata import read_step_database, PushButtonDelegate
from mapclient.core.workflow.workflowsteps import WorkflowStepsFilter
from mapclient.tools.pluginfinder.ui.ui_pluginfinderdialog import Ui_PluginFinderDialog

from mapclient.tools.pluginfinder.downloadtodirectorydialog import DownloadToDirectoryDialog

logger = logging.getLogger(__name__)


class PluginFinderDialog(QDialog):
    """
    Manages information for finding and installing new MAP Client plugins.
    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self._ui = Ui_PluginFinderDialog()
        self._ui.setupUi(self)

        self._plugin_directories = parent.model().pluginManager().directories()
        self._plugin_data = read_step_database()
        self._filtered_plugins = WorkflowStepsFilter()
        self._filtered_plugins.setSourceModel(self._plugin_data)
        self._ui.stepTreeView.setMouseTracking(True)
        self._ui.stepTreeView.setModel(self._filtered_plugins)
        self.tree_delegate = PushButtonDelegate(self._plugin_data)
        self._ui.stepTreeView.setItemDelegateForColumn(0, self.tree_delegate)
        self.tree_delegate.buttonClicked.connect(self.tree_button_clicked)
        self.update_available_steps()
        self.expand_step_tree()

        self._make_connections()

    def tree_button_clicked(self, url):
        self._download_to_directory_dialog(url)

    def _download_to_directory_dialog(self, url):
        dlg = DownloadToDirectoryDialog(self._plugin_directories, url, self)
        dlg.setModal(True)
        dlg.exec_()

    def _make_connections(self):
        self._ui.lineEditFilter.textChanged.connect(self._filter_text_changed)

    def _filter_text_changed(self, text):
        reg_exp = QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive)
        self._ui.stepTreeView.setFilterRegExp(reg_exp)

    def update_available_steps(self):
        self._plugin_data.reload()
        self._filtered_plugins.sort(QtCore.Qt.AscendingOrder)

    def expand_step_tree(self):
        self._ui.stepTreeView.expandAll()
