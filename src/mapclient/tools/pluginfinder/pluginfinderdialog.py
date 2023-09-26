"""
This tool is used to search for new MAP Client plugins.

Author: Timothy Salemink
"""

from packaging import version

from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QMessageBox

from mapclient.tools.pluginfinder.plugindata import get_plugin_database, PushButtonDelegate, PluginData
from mapclient.core.workflow.workflowsteps import WorkflowStepsFilter
from mapclient.tools.pluginfinder.ui.ui_pluginfinderdialog import Ui_PluginFinderDialog
from mapclient.tools.pluginfinder.downloadtodirectorydialog import DownloadToDirectoryDialog


class PluginFinderDialog(QDialog):
    """
    Manages information for finding and installing new MAP Client plugins.
    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self._ui = Ui_PluginFinderDialog()
        self._ui.setupUi(self)

        self._selected_indexes = []
        self._plugin_manager = parent.model().pluginManager()
        self._plugin_database = get_plugin_database()
        self._plugin_data = PluginData(self._plugin_database)
        self._filtered_plugins = WorkflowStepsFilter()
        self._filtered_plugins.setSourceModel(self._plugin_data)
        self._ui.stepTreeView.setMouseTracking(True)
        self._ui.stepTreeView.setDragEnabled(False)
        self._ui.stepTreeView.setStyleSheet("QTreeView::item:hover{background-color:#94c8ea;}")
        self._ui.stepTreeView.setModel(self._filtered_plugins)
        self._database_versions = self._get_database_versions()
        self._tree_delegate = PushButtonDelegate(self._plugin_data, self._get_installed_versions(), self._database_versions)
        self._ui.stepTreeView.setItemDelegateForColumn(0, self._tree_delegate)
        self._tree_delegate.buttonClicked.connect(self._tree_button_clicked)
        self._ui.stepTreeView.selection_changed.connect(self._tree_selection_changed)
        self._update_available_steps()
        self._expand_step_tree()

        self._make_connections()

    def _get_installed_versions(self):
        version_dict = {}
        for plugin_name, plugin_data in self._plugin_manager.getPluginDatabase().getDatabase().items():
            version_dict[plugin_name] = plugin_data['version']
        return version_dict

    def _get_database_versions(self):
        version_dict = {}
        for _, plugin_data in self._plugin_database.items():
            version_dict[plugin_data.get_name()] = plugin_data.get_version()
        return version_dict

    def _tree_selection_changed(self, selected_indexes):
        self._selected_indexes = selected_indexes
        if self._selected_indexes:
            if self._ui.horizontalLayout_4.isEmpty():
                selection_label = QLabel(f"{len(self._selected_indexes)} plugin(s) selected.")
                selection_label.setFont(QtGui.QFont('MS Shell Dlg', 9))

                download_button = QPushButton("  Download Selected Plugins  ")
                download_button.setFont(QtGui.QFont('MS Shell Dlg', 9))
                download_button.clicked.connect(self._download_selected)

                self._ui.horizontalLayout_4.addWidget(selection_label)
                self._ui.horizontalLayout_4.addWidget(download_button, alignment=QtCore.Qt.AlignRight)
            else:
                self._ui.horizontalLayout_4.itemAt(0).widget().setText(f"{len(self._selected_indexes)} plugin(s) selected.")
        else:
            for i in reversed(range(self._ui.horizontalLayout_4.count())):
                self._ui.horizontalLayout_4.itemAt(i).widget().deleteLater()

    def _download_selected(self):
        url_list = []
        for index in self._selected_indexes:
            installed_versions = self._tree_delegate.get_installed_versions()
            name = index.data()

            if name in installed_versions.keys():
                if version.parse(self._database_versions[name]) <= version.parse(installed_versions[name]):
                    continue
                else:
                    overwrite = self._confirm_overwrite(name)
                    if overwrite == QMessageBox.No:
                        continue

            url = self._ui.stepTreeView.selectionModel().model().data(index, QtCore.Qt.UserRole + 1).get_url()
            url_list.append(url)
        self._download_to_directory_dialog(url_list)

    def _confirm_overwrite(self, name):
        overwrite = QMessageBox.question(self, 'Confirm Overwrite', f'The plugin ({name}) is already installed. Updating this plugin '
                                         'will overwrite the currently installed version of the plugin, please ensure that you don\'t '
                                         'have any development changes that you wish to retain.\n\n Do you want to overwrite the '
                                         'currently installed plugin?')
        return overwrite

    def _tree_button_clicked(self, name, url):
        installed_versions = self._tree_delegate.get_installed_versions()
        if name in installed_versions.keys():
            if version.parse(self._database_versions[name]) > version.parse(installed_versions[name]):
                overwrite = self._confirm_overwrite(name)
                if overwrite == QMessageBox.No:
                    return

        self._download_to_directory_dialog([url])

    def _download_to_directory_dialog(self, url_list):
        if url_list:
            dlg = DownloadToDirectoryDialog(self._plugin_manager, url_list, self)
            dlg.setModal(True)
            dlg.exec_()

    def _make_connections(self):
        self._ui.lineEditFilter.textChanged.connect(self._filter_text_changed)

    def _filter_text_changed(self, text):
        reg_exp = QtCore.QRegularExpression(text, QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption)
        self._ui.stepTreeView.setFilterRegularExpression(reg_exp)

    def _update_available_steps(self):
        self._plugin_data.reload()
        self._filtered_plugins.sort(1, QtCore.Qt.AscendingOrder)

    def _expand_step_tree(self):
        self._ui.stepTreeView.expandAll()
