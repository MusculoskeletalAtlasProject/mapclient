"""
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland

This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
"""
import json
import os
from copy import deepcopy

from PySide6 import QtGui, QtWidgets

from mapclient.core.managers.pluginmanager import CONST_DEFAULT_PROFILE
from mapclient.tools.pluginmanager.ui.ui_pluginmanagerdialog import Ui_PluginManagerDialog


class PluginManagerDialog(QtWidgets.QDialog):
    """
    Dialog for managing the list of plugin directories.
    """

    def __init__(self, plugin_manager, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self._ui = Ui_PluginManagerDialog()
        self._ui.setupUi(self)
        self._ui.removeButton.setEnabled(False)
        self._ui.advancedButton.setVisible(False)

        self._plugin_manager = plugin_manager
        self._profile_directories = deepcopy(plugin_manager.profile_directories())
        self._initialise_ui()
        self._update_ui()

        self._make_connections()

    def _make_connections(self):
        self._ui.addButton.clicked.connect(self._add_directory_clicked)
        self._ui.profileNewButton.clicked.connect(self._create_new_profile)
        self._ui.profileEditButton.clicked.connect(self._edit_current_profile)
        self._ui.profileDeleteButton.clicked.connect(self._delete_current_profile)
        self._ui.profileComboBox.currentIndexChanged.connect(self._profile_changed)
        self._ui.directoryListing.itemSelectionChanged.connect(self._directory_selection_changed)
        self._ui.removeButton.clicked.connect(self._remove_button_clicked)
        self._ui.applyButton.clicked.connect(self.reload_plugins)
        self._ui.advancedButton.clicked.connect(self._show_advanced_dialog)

    def _show_advanced_dialog(self):
        from mapclient.view.managers.plugins.advanceddialog import AdvancedDialog
        dlg = AdvancedDialog(None, None, None, None)
        dlg.setModal(True)
        if dlg.exec():
            self._ignoredPlugins = dlg._ignoredPlugins
            self._do_not_show_plugin_errors = dlg._doNotShowErrors
            self._resource_filenames = dlg._resourceFiles
            self._updaterSettings = dlg._updaterSettings
            self.reload_plugins()

    def _initialise_ui(self):
        self._ui.profileComboBox.clear()
        self._ui.directoryListing.clear()

        # Add profiles to the combo box.
        current_profile = self._plugin_manager.current_profile()
        for profile in self._profile_directories:
            self._ui.profileComboBox.addItem(profile)
            if profile == current_profile:
                self._ui.profileComboBox.setCurrentText(profile)

        self._set_directories(self._profile_directories.get(current_profile, []))

    def _update_ui(self):
        editable_profile = self._ui.profileComboBox.currentText() != CONST_DEFAULT_PROFILE
        self._ui.profileEditButton.setEnabled(editable_profile)
        self._ui.profileDeleteButton.setEnabled(editable_profile)

    def _profile_changed(self, current_index):
        current_profile = self._ui.profileComboBox.currentText()
        self._set_directories(self._profile_directories.get(current_profile, []))
        self._update_ui()

    def _directory_selection_changed(self):
        self._ui.removeButton.setEnabled(len(self._ui.directoryListing.selectedItems()) > 0)

    def _create_new_profile(self):
        from mapclient.tools.pluginmanager.newprofiledialog import NewProfileDialog
        dlg = NewProfileDialog()
        dlg.setModal(True)
        if dlg.exec():
            new_profile = dlg.getProfileName()
            if new_profile:
                self._ui.profileComboBox.addItem(new_profile)
                self._ui.profileComboBox.setCurrentText(new_profile)
                self._ui.directoryListing.clear()
                self._profile_directories[new_profile] = []

    def _edit_current_profile(self):
        from mapclient.tools.pluginmanager.editprofiledialog import EditProfileDialog
        dlg = EditProfileDialog(self._ui.profileComboBox.currentText())
        dlg.setModal(True)
        if dlg.exec():
            current_profile = self._ui.profileComboBox.currentText()
            edited_profile = dlg.getProfileName()
            if edited_profile and edited_profile != current_profile and edited_profile not in self._profile_directories.keys():
                current_index = self._ui.profileComboBox.currentIndex()
                self._ui.profileComboBox.setItemText(current_index, edited_profile)
                self._profile_directories[edited_profile] = self._profile_directories[current_profile]
                del self._profile_directories[current_profile]

    def _delete_current_profile(self):
        current_profile = self._ui.profileComboBox.currentText()
        self._ui.profileComboBox.removeItem(self._ui.profileComboBox.currentIndex())
        self._profile_directories.pop(current_profile)
        self._update_ui()

    def _remove_button_clicked(self):
        for item in self._ui.directoryListing.selectedItems():
            row = self._ui.directoryListing.row(item)
            current_profile = self._ui.profileComboBox.currentText()
            del self._profile_directories[current_profile][row]
            self._ui.directoryListing.takeItem(row)

    def _add_directory_clicked(self):
        selected_items = self._ui.directoryListing.selectedItems()
        if selected_items:
            last_selected_item = selected_items[-1]
            last = last_selected_item
        else:
            last = self._ui.directoryListing.item(self._ui.directoryListing.count() - 1)

        if last:
            last = last.text()

        directory = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Select External Plugin Directory', dir=last, options=QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ReadOnly)
        if len(directory) > 0:
            current_profile = self._ui.profileComboBox.currentText()
            self._profile_directories[current_profile].append(directory)
            self._ui.directoryListing.addItem(directory)

    def _get_profile_directories(self, profile_name):
        """
        This method should be overridden to return the directories associated with the given profile name.
        """
        # Placeholder for actual implementation.
        return []

    def _display_directories(self):
        pass

    def reload_plugins(self):
        """
        Set this to a callable method that will reload the plugins in the plugin manager.
        """
        pass

    def _set_profile(self, profile_name):
        """
        Set the current profile in the dialog.
        """
        have_profile = profile_name in self._ui.profileComboBox
        if have_profile:
            self._ui.profileComboBox.setCurrentText(profile_name)
        elif "Default" not in self._ui.profileComboBox:
            self._ui.profileComboBox.addItem("Default")

        if not have_profile:
            self._ui.profileComboBox.setCurrentText("Default")

        self._display_directories()

    def profile(self):
        """
        Get the current profile name from the dialog.
        """
        return self._ui.profileComboBox.currentText()

    def _set_directories(self, directories):
        self._ui.directoryListing.clear()
        self._ui.directoryListing.addItems([directory for directory in directories if os.path.exists(directory)])

    def directories(self):
        directories = []
        for index in range(self._ui.directoryListing.count()):
            directories.append(self._ui.directoryListing.item(index).text())

        return directories

    def save_profile_data(self):
        self._plugin_manager.set_current_profile(self._ui.profileComboBox.currentText())
        self._plugin_manager.set_profile_directories(self._profile_directories)

# import sys
# import json
# import os
# from PySide6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QListView,
#     QPushButton, QMessageBox, QInputDialog
# )
# from PySide6.QtGui import QStandardItemModel, QStandardItem
#
DATA_FILE = "models_data.json"
#
initial_data = {
    "default": ["/path/1", "/path/2"],
    "sparc": ["/path/4", "/path/5"],
}


class ModelManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model Manager")

        main_layout = QtWidgets.QVBoxLayout(self)
        control_layout = QtWidgets.QHBoxLayout()
        path_control_layout = QtWidgets.QHBoxLayout()

        self.combo_box = QtWidgets.QComboBox()
        self.list_view = QtWidgets.QListView()
        self.save_button = QtWidgets.QPushButton("Save to Disk")
        self.add_key_button = QtWidgets.QPushButton("Add Key")
        self.remove_key_button = QtWidgets.QPushButton("Remove Key")
        self.add_path_button = QtWidgets.QPushButton("Add Path")
        self.remove_path_button = QtWidgets.QPushButton("Remove Path")

        control_layout.addWidget(self.combo_box)
        control_layout.addWidget(self.add_key_button)
        control_layout.addWidget(self.remove_key_button)

        path_control_layout.addWidget(self.add_path_button)
        path_control_layout.addWidget(self.remove_path_button)

        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.list_view)
        main_layout.addLayout(path_control_layout)
        main_layout.addWidget(self.save_button)

        self.list_models = {}
        self.load_data()

        self.combo_box.addItems(self.list_models.keys())
        self.combo_box.currentIndexChanged.connect(self.update_list_model)
        self.save_button.clicked.connect(self.save_data)
        self.add_key_button.clicked.connect(self.add_key)
        self.remove_key_button.clicked.connect(self.remove_key)
        self.add_path_button.clicked.connect(self.add_path)
        self.remove_path_button.clicked.connect(self.remove_path)

        self.update_list_model(0)

    def create_model(self, paths):
        model = QtGui.QStandardItemModel()
        for path in paths:
            item = QtGui.QStandardItem(path)
            item.setEditable(True)
            model.appendRow(item)
        return model

    def update_list_model(self, index):
        if index < 0 or self.combo_box.count() == 0:
            self.list_view.setModel(QtGui.QStandardItemModel())
            return
        key = self.combo_box.itemText(index)
        self.list_view.setModel(self.list_models[key])

    def save_data(self):
        data_to_save = {
            key: [self.list_models[key].item(i).text() for i in range(self.list_models[key].rowCount())]
            for key in self.list_models
        }
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(data_to_save, f, indent=2)
            QtWidgets.QMessageBox.information(self, "Success", "Data saved successfully.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save data: {e}")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    loaded_data = json.load(f)
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
                loaded_data = initial_data
        else:
            loaded_data = initial_data

        for key, paths in loaded_data.items():
            self.list_models[key] = self.create_model(paths)

    def add_key(self):
        key, ok = QtWidgets.QInputDialog.getText(self, "Add Key", "Enter new key name:")
        if ok and key:
            if key in self.list_models:
                QtWidgets.QMessageBox.warning(self, "Warning", "Key already exists.")
                return
            self.list_models[key] = self.create_model([])
            self.combo_box.addItem(key)
            self.combo_box.setCurrentText(key)

    def remove_key(self):
        index = self.combo_box.currentIndex()
        if index < 0:
            return
        key = self.combo_box.itemText(index)
        confirm = QtWidgets.QMessageBox.question(self, "Confirm", f"Delete key '{key}'?")
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            self.combo_box.removeItem(index)
            del self.list_models[key]
            self.update_list_model(self.combo_box.currentIndex())

    def add_path(self):
        index = self.combo_box.currentIndex()
        if index < 0:
            return
        key = self.combo_box.itemText(index)
        path, ok = QtWidgets.QInputDialog.getText(self, "Add Path", "Enter new path:")
        if ok and path:
            item = QtGui.QStandardItem(path)
            item.setEditable(True)
            self.list_models[key].appendRow(item)

    def remove_path(self):
        index = self.combo_box.currentIndex()
        if index < 0:
            return
        key = self.combo_box.itemText(index)
        selected_indexes = self.list_view.selectedIndexes()
        if not selected_indexes:
            QtWidgets.QMessageBox.warning(self, "Warning", "No path selected.")
            return
        for idx in selected_indexes:
            self.list_models[key].removeRow(idx.row())

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = ModelManager()
#     window.show()
#     sys.exit(app.exec())
