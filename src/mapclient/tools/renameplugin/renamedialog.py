
import os

import shutil
import subprocess

from PySide2 import QtCore, QtWidgets

from mapclient.core.managers.pluginmanager import isMapClientPluginsDir
from mapclient.core.utils import grep, determinePackageName, determineStepClassName, determineStepName, \
    convertNameToPythonPackage, find_file
from mapclient.settings.definitions import PLUGINS_PACKAGE_NAME
from mapclient.tools.renameplugin.ui.ui_renamedialog import Ui_RenameDialog


class RenameDialog(QtWidgets.QDialog):

    def __init__(self, pyside_rcc, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self._ui = Ui_RenameDialog()
        self._ui.setupUi(self)

        self._pyside_rcc = pyside_rcc

        self._editDelayTimer = QtCore.QTimer()
        self._editDelayTimer.setInterval(500)
        self._editDelayTimer.setSingleShot(True)

        self._package_name_edited = False

        self._previousLocation = None

        self._makeConnections()

    def _makeConnections(self):
        self._ui.pushButtonRename.clicked.connect(self._renameClicked)
        self._ui.pushButtonStepChooser.clicked.connect(self._chooseStepClicked)
        self._ui.lineEditRenameStepTo.textEdited.connect(self._editDelayTimer.start)
        self._ui.lineEditRenameStepTo.textEdited.connect(self._stepNameEdited)
        self._ui.lineEditRenamePackageTo.textEdited.connect(self._packageNameEdited)
        self._editDelayTimer.timeout.connect(self._runRenameSearch)

    def _runRenameSearch(self):
        self._ui.treeWidgetRename.clear()
        self._ui.treeWidgetRename.setColumnCount(1)
        root = QtWidgets.QTreeWidgetItem(self._ui.treeWidgetRename, ['Found Occurrences'])

        package_name = self._ui.lineEditRenamePackageFrom.text()
        new_package_name = self._ui.lineEditRenamePackageTo.text()
        package_name_files = grep(self._ui.lineEditStepLocation.text(), package_name)
        self._addSearchResults(root, package_name_files, package_name, new_package_name)

        step_name = self._ui.lineEditRenameStepFrom.text()
        new_step_name = self._ui.lineEditRenameStepTo.text()
        step_name_files = grep(self._ui.lineEditStepLocation.text(), step_name)
        self._addSearchResults(root, step_name_files, step_name, new_step_name)

        step_class_name = step_name.replace(' ', '') + 'Step'
        new_step_class_name = new_step_name.replace(' ', '') + 'Step'
        step_class_name_files = grep(self._ui.lineEditStepLocation.text(), step_class_name)
        self._addSearchResults(root, step_class_name_files, step_class_name, new_step_class_name)

        self._ui.treeWidgetRename.expandAll()
        self._ui.treeWidgetRename.setColumnWidth(0, self._ui.treeWidgetRename.sizeHintForColumn(0))

    def _addSearchResults(self, root_item, result_files, search_string, replace_string):
        tree = root_item.treeWidget()
        for result_file in result_files:
            items = tree.findItems(result_file, QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive)
            if items:
                file_branch = items[0]
                new_item = False
            else:
                file_branch = QtWidgets.QTreeWidgetItem(root_item, [result_file])
                new_item = True
            for results in result_files[result_file]:
                line_no = results[0]
                line_leaf = None
                if not new_item:
                    line_leaf = self._find_matching_leaf_item(file_branch, line_no)

                if line_leaf is None:
                    line_leaf = QtWidgets.QTreeWidgetItem(file_branch)
                    line_leaf.setCheckState(0, QtCore.Qt.Checked)
                    preview_string = results[1]
                else:
                    preview_string = line_leaf.data(1, QtCore.Qt.UserRole + 2)
                # line_leaf.setData(1, QtCore.Qt.UserRole + 0, replace_string)
                preview_string = preview_string.replace(search_string, replace_string)
                line_leaf.setText(0, '(line #{0}) {1}'.format(line_no, preview_string))
                line_leaf.setData(1, QtCore.Qt.UserRole + 1, line_no)
                line_leaf.setData(1, QtCore.Qt.UserRole + 2, preview_string)

    def _find_matching_leaf_item(self, parent_item, line_no):
        for index in range(parent_item.childCount()):
            child_item = parent_item.child(index)
            if child_item.data(1, QtCore.Qt.UserRole + 1) == line_no:
                return child_item

        return None

    def _stepNameEdited(self):
        if not self._package_name_edited:
            package_name = convertNameToPythonPackage(self._ui.lineEditRenameStepTo.text())
            self._ui.lineEditRenamePackageTo.setText(package_name)

        self._setRenameButtonEnabled()

    def _setRenameButtonEnabled(self):
        rename_enabled = len(self._ui.lineEditRenameStepTo.text()) and len(self._ui.lineEditRenamePackageTo.text())
        self._ui.pushButtonRename.setEnabled(rename_enabled)

    def _packageNameEdited(self):
        self._package_name_edited = True
        self._setRenameButtonEnabled()

    def _chooseStepClicked(self):
        location = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory', self._previousLocation)

        if location:
            self._previousLocation = location
            self._ui.lineEditStepLocation.setText(location)
            self._interrogateTarget()

    def _interrogateTarget(self):
        target = self._ui.lineEditStepLocation.text()
        is_plugin_dir = isMapClientPluginsDir(target)
        if is_plugin_dir:
            step_dir = os.path.join(target, PLUGINS_PACKAGE_NAME)
            files = grep(step_dir, r'(from|import) mapclient.mountpoints.workflowstep',
                         one_only=True, file_endswith='.py')
            step_name_file, _ = files.popitem()
            package_name = determinePackageName(target, step_name_file)
            class_name = determineStepClassName(os.path.join(target, PLUGINS_PACKAGE_NAME, step_name_file))
            step_name = determineStepName(os.path.join(target, PLUGINS_PACKAGE_NAME, step_name_file), class_name)

            self._ui.lineEditRenameStepFrom.setText(step_name)
            self._ui.lineEditRenamePackageFrom.setText(package_name)
        else:
            QtGui.QMessageBox.warning(self, 'Rename',
                                      'Target directory is not recognized as a MAP Client plugin directory')

    def _renameClicked(self):
        tree = self._ui.treeWidgetRename
        tree_it = QtWidgets.QTreeWidgetItemIterator(tree)
        for tree_item in tree_it:
            item = tree_item.value()
            if item.childCount() == 0:  # Leaf node
                if item.checkState(0) == QtCore.Qt.Checked:
                    filename = item.parent().text(0)
                    line_no = item.data(1, QtCore.Qt.UserRole + 1)
                    new_string = item.data(1, QtCore.Qt.UserRole + 2)
                    self._doRename(filename, line_no, new_string)

        if self._updateResourceFile():
            QtWidgets.QMessageBox.critical(self, 'Rename', 'Errors when running pyside-rcc.')
            return

        try:
            self._doDirectoryRename()
            QtWidgets.QMessageBox.information(self, 'Rename', 'Renaming the step was successful')
            self.accept()
        except OSError:
            QtWidgets.QMessageBox.critical(self, 'Rename directory', 'Could not rename the directory.')

    def _updateResourceFile(self):
        target = self._ui.lineEditStepLocation.text()
        qrc_file = find_file('resources.qrc', target)
        python_rc_file = find_file('resources_rc.py', target)
        if qrc_file is None or python_rc_file is None:
            return -1
        p = subprocess.Popen([self._pyside_rcc, '-py3', qrc_file, '-o', python_rc_file],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()
        return p.returncode

    def _doDirectoryRename(self):
        target = self._ui.lineEditStepLocation.text()
        old_package = self._ui.lineEditRenamePackageFrom.text()
        new_package = self._ui.lineEditRenamePackageTo.text()
        shutil.move(os.path.join(target, PLUGINS_PACKAGE_NAME, old_package),
                    os.path.join(target, PLUGINS_PACKAGE_NAME, new_package))

    def _doRename(self, filename, line_no, new_string):
        target = self._ui.lineEditStepLocation.text()
        with open(os.path.join(target, filename), 'r+') as f:
            lines = f.readlines()
            lines[line_no] = '{0}\n'.format(new_string)
            f.seek(0)
            f.write(''.join(lines))
            f.truncate()
