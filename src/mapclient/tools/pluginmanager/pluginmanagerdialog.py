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
import os
from copy import deepcopy

from PySide6 import QtWidgets

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

        dlg_options = (QtWidgets.QFileDialog.Option.ShowDirsOnly |
                       QtWidgets.QFileDialog.Option.DontResolveSymlinks |
                       QtWidgets.QFileDialog.Option.ReadOnly)
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, caption='Select External Plugin Directory', dir=last, options=dlg_options)
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
