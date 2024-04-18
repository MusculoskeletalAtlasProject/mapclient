
import io
import zipfile
import requests

from posixpath import join
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox

from mapclient.tools.pluginfinder.ui.ui_downloadtodirectorydialog import Ui_DownloadToDirectoryDialog


class DownloadToDirectoryDialog(QDialog):
    """
    This dialog is used to select the directory in which to download new MAP-Client plugins.
    """
    def __init__(self, plugin_manager, url_list, parent=None):
        QDialog.__init__(self, parent)

        self._ui = Ui_DownloadToDirectoryDialog()
        self._ui.setupUi(self)

        self._plugin_manager = plugin_manager
        self._plugin_directories = plugin_manager.directories()
        self._url_list = url_list

        self._update_combo_box()
        self._selection_changed()

        self._make_connections()

    def _make_connections(self):
        self._ui.pushButtonDownload.clicked.connect(self._download_clicked)
        self._ui.pushButtonDirChooser.clicked.connect(self._choose_directory_clicked)
        self._ui.comboBoxDirChooser.currentIndexChanged.connect(self._selection_changed)

    def _update_combo_box(self):
        self._ui.comboBoxDirChooser.clear()
        self._ui.comboBoxDirChooser.addItems(self._plugin_directories)

    def _selection_changed(self):
        self._selected_directory = self._ui.comboBoxDirChooser.currentText()

    def _choose_directory_clicked(self):
        selected_directory = QFileDialog.getExistingDirectory(self, 'Select Directory', self._selected_directory)
        self._update_combo_box()

        if selected_directory is not None and (selected_directory not in self._plugin_directories):
            self._ui.comboBoxDirChooser.addItem(selected_directory)
            self._ui.comboBoxDirChooser.setCurrentText(selected_directory)

    def _download_clicked(self):
        if self._selected_directory:
            for url in self._url_list:
                x = requests.get(join(url, "zipball", ""))

                with zipfile.ZipFile(io.BytesIO(x.content)) as archive:
                    archive.extractall(self._selected_directory)

            # If the selected directory is not a MAP-plugin-directory, ask the user if they want to add it as one.
            if self._selected_directory not in self._plugin_directories:
                add_dir = QMessageBox.question(self, 'Add Directory', 'The selected directory is not recognized as a MAP-Client plugins '
                                               'directory. Do you wish to add this directory to the MAP-Client plugin search path?')
                if add_dir == QMessageBox.Yes:
                    self._plugin_directories.append(self._selected_directory)
                    self._plugin_manager.setDirectories(self._plugin_directories)

            answer = QMessageBox.information(self, 'Download Successful', 'The selected plugin was successfully downloaded. '
                                             'You may need to restart the application to pick up newly downloaded plugins.')

            if answer == QMessageBox.Ok:
                self.accept()

        else:
            QMessageBox.warning(self, 'No Directory Selected', 'Please select a download directory.')
