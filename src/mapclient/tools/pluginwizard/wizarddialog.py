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
import sys
import platform
import ast

from PySide2 import QtCore, QtWidgets, QtGui

from mapclient.core.utils import convertNameToPythonPackage, is_frozen
from mapclient.tools.pluginwizard.skeleton import SkeletonOptions
from mapclient.tools.pluginwizard.ui_output import Ui_Output
from mapclient.tools.pluginwizard.ui_name import Ui_Name
from mapclient.tools.pluginwizard.ui_ports import Ui_Ports
from mapclient.tools.pluginwizard.ui_config import Ui_Config
from mapclient.tools.pluginwizard.ui_misc import Ui_Misc

# Registered field names:
OUTPUT_DIRECTORY_FIELD = 'output_directory'
NAME_FIELD = 'name'
IMAGE_FILE_FIELD = 'image_file'
PREDEFINED_IMAGE_FIELD = 'predefined_image_field'
PACKAGE_NAME_FIELD = 'package_name'
PORTS_FIELD = 'ports_table'
IDENTIFIER_CHECKBOX = 'identifier_checkbox'
CATEGORY_FIELD = 'category'
AUTHOR_NAME_FIELD = 'author_name'
PLUGIN_LOCATION_FIELD = 'plugin_location'
ICON_PICTURE_LABEL_FIELD = 'icon_picture_label'

# Style sheets
REQUIRED_STYLE_SHEET = 'background-color: rgba(239, 16, 16, 20%)'
DEFAULT_STYLE_SHEET = ''

imageNameMap = {'Default': 'default.png', 'Source': 'data-source.png', 'Sink': 'data-sink.png', 'Fitting': 'fitting.png', 'Model Viewer': 'model-viewer.png',
                'Image Processing': 'image-processing.png', 'Segmentation': 'segmentation.png', 'Morphometric': 'morphometric.png', 'Registration': 'registration.png',
                'Utility': 'utility.png'}


class WizardDialog(QtWidgets.QWizard):

    def __init__(self, parent=None):
        super(WizardDialog, self).__init__(parent)
        self.setWindowTitle('Workflow Step Wizard')
        self.setFixedSize(675, 550)

        self.setDefaultProperty('QComboBox', 'currentText', 'currentIndexChanged')
        self.setDefaultProperty('QLabel', 'pixmap', '')

        if platform.system() == 'Darwin':
            self.setWizardStyle(QtWidgets.QWizard.MacStyle)
        else:
            self.setWizardStyle(QtWidgets.QWizard.ModernStyle)
        # set pages
        self.addPage(createIntroPage())
        self.addPage(NameWizardPage())
        self.addPage(PortsWizardPage())
        self.addPage(ConfigWizardPage())
        self.addPage(MiscWizardPage())
        self.addPage(OutputWizardPage())

        # set images banner, logo, watermark and background
        self.setPixmap(QtWidgets.QWizard.LogoPixmap, QtGui.QPixmap(':/wizard/images/logo.png'))
        self.setPixmap(QtWidgets.QWizard.BannerPixmap, QtGui.QPixmap(':/wizard/images/banner.png'))
#         self.setPixmap(QtWidgets.QWizard.WatermarkPixmap, QtGui.QPixmap(':/wizard/images/watermark.png'))
#         self.setPixmap(QtWidgets.QWizard.BackgroundPixmap, QtGui.QPixmap(':/wizard/images/background.png'))
        self._options = SkeletonOptions()

    def setPreviousWriteStepLocation(self, location):
        page = self.page(5)
        page.setDirectory(location)

    def setPreviousIconLocation(self, location):
        page = self.page(1)
        page.setPreviousLocation(location)

    def getPreviousWriteStepLocation(self):
        return self.field(OUTPUT_DIRECTORY_FIELD)

    def getPreviousIconLocation(self):
        icon_file = self.field(IMAGE_FILE_FIELD)
        return os.path.dirname(icon_file)

    def getOptions(self):
        return self._options

    def accept(self):
        self._options.setOutputDirectory(self.field(OUTPUT_DIRECTORY_FIELD))
        self._options.setImageFile(self.field(IMAGE_FILE_FIELD))
        self._options.setName(self.field(NAME_FIELD))
        self._options.setPackageName(self.field(PACKAGE_NAME_FIELD))
        self._options.setPluginLocation(self.field(PLUGIN_LOCATION_FIELD))

        predefinedName = self.field(PREDEFINED_IMAGE_FIELD)
        predefined_filename = getPredefinedImageLocation(predefinedName)
        icon_filename = self.field(IMAGE_FILE_FIELD)
        if (predefined_filename == icon_filename and predefinedName != 'Default') or \
           (icon_filename and predefined_filename != icon_filename):
            (_, image_filename) = os.path.split(icon_filename)
            self._options.setImageFile(image_filename)
            self._options.setIcon(self.field(ICON_PICTURE_LABEL_FIELD))

        # Registered field failed to return table, may need to set up
        # default property for this to work.  Currently using workaround
        # by directly getting desired widget
        ports_table = self.page(2)._ui.portTableWidget
        row_index = 0
        while row_index < ports_table.rowCount():
            self._options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#' + ports_table.cellWidget(row_index, 0).currentText(),
                                   ports_table.item(row_index, 1).text() if ports_table.item(row_index, 1) else '<not-set>')
            row_index += 1

        if self.page(3)._ui.identifierCheckBox.isChecked():
            self._options.addConfig('identifier', '')

        configs_table = self.page(3)._ui.configTableWidget
        row_index = 0
        while row_index < configs_table.rowCount():
            config_label = configs_table.item(row_index, 0)
            config_default_value = configs_table.item(row_index, 1)
            if config_label is not None:
                self._options.addConfig(config_label.text(),
                                        '' if config_default_value is None else config_default_value.text())
            row_index += 1

        self._options.setCategory(self.field(CATEGORY_FIELD))
        self._options.setAuthorName(self.field(AUTHOR_NAME_FIELD))

        super(WizardDialog, self).accept()


def createIntroPage():
    page = QtWidgets.QWizardPage()
    page.setTitle('Introduction')
    page.setSubTitle('Create skeleton Python code to get started creating a workflow step.')
    label = QtWidgets.QLabel('This wizard will help get you started creating your own plugin for the MAP Client.')
    label.setWordWrap(True)

    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(label)
    page.setLayout(layout)

    page.setPixmap(QtWidgets.QWizard.WatermarkPixmap, QtGui.QPixmap(':/wizard/images/watermark.png'))
    page.setPixmap(QtWidgets.QWizard.BackgroundPixmap, QtGui.QPixmap(':/wizard/images/background.png'))
    page.setPixmap(QtWidgets.QWizard.BannerPixmap, QtGui.QPixmap(':/wizard/images/banner.png'))

    return page


class NameWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent=None):
        super(NameWizardPage, self).__init__(parent)

        self.setTitle('Identify Workflow Step')
        self.setSubTitle('Set the name and icon (optional) for the workflow step.')

        self._ui = Ui_Name()
        self._ui.setupUi(self)

        self._previous_location = ''

        self._invalidPixmap = QtGui.QPixmap(':wizard/images/cross.png')
        self._invalidNameLabel = QtWidgets.QLabel(self)
        self._invalidNameLabel.setStyleSheet('border: none; padding: 0px;')
        self._invalidPackageLabel = QtWidgets.QLabel(self)
        self._invalidPackageLabel.setStyleSheet('border: none; padding: 0px;')
        self._invalidIconLabel = QtWidgets.QLabel(self)
        self._invalidIconLabel.setStyleSheet('border: none; padding: 0px;')

        self._updateImage()

        self._makeConnections()
        self._defineFields()
        self._packageNameEdited = False

    def _defineFields(self):
        self.registerField(NAME_FIELD + '*', self._ui.nameLineEdit)
        self.registerField(PACKAGE_NAME_FIELD + '*', self._ui.packageNameLineEdit)
        self.registerField(IMAGE_FILE_FIELD, self._ui.iconLineEdit)
        self.registerField(PREDEFINED_IMAGE_FIELD, self._ui.comboBoxPresetIcons)
        self.registerField(ICON_PICTURE_LABEL_FIELD, self._ui.iconPictureLabel)

    def _makeConnections(self):
        self._ui.nameLineEdit.textChanged.connect(self._nameChanged)
        self._ui.nameLineEdit.textChanged.connect(self._updateImage)
        self._ui.packageNameLineEdit.textEdited.connect(self._packageNameChanged)
        self._ui.iconLineEdit.textChanged.connect(self._updateImage)
        self._ui.iconButton.clicked.connect(self._chooseImage)
        self._ui.comboBoxPresetIcons.currentIndexChanged.connect(self._selectPredefinedImage)

    def _nameChanged(self):
        if not self._packageNameEdited:
            package_name = convertNameToPythonPackage(self._ui.nameLineEdit.text())
            self._ui.packageNameLineEdit.setText(package_name)

        self.completeChanged.emit()

    def _packageNameChanged(self):
        self._packageNameEdited = True

    def _selectPredefinedImage(self, index):
        image_file = getPredefinedImageLocation(self._ui.comboBoxPresetIcons.currentText())
        self._ui.iconLineEdit.setText(image_file)

    def _chooseImage(self):
        image, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Choose Image File', dir=self._previous_location, options=QtWidgets.QFileDialog.ReadOnly)
        if len(image) > 0:
            self._previous_location = os.path.dirname(image)
            self._ui.iconLineEdit.setText(image)

    def _updateImage(self):

        image_file = self._ui.iconLineEdit.text()
        if image_file:
            image = QtGui.QPixmap(image_file)

            predefined_image_file = getPredefinedImageLocation(self._ui.comboBoxPresetIcons.currentText())
            if predefined_image_file == image_file:
                image = self._combineImageWithBackground(image.toImage())
                image = QtGui.QPixmap.fromImage(image)

            if image:
                self._ui.iconPictureLabel.setPixmap(image.scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation))
        else:
            image = QtGui.QImage(':icons/images/default.png')
            image = self._combineImageWithBackground(image)
            self._ui.iconPictureLabel.setPixmap(QtGui.QPixmap.fromImage(image).scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation))

        self.completeChanged.emit()

    def _combineImageWithBackground(self, image):
        background_image = QtGui.QImage(':icons/images/icon-background.png')
        painter = QtGui.QPainter(background_image)

        painter.drawImage(QtCore.QPoint(0, 0), image)
        painter.end()

        return background_image

    def setPreviousLocation(self, location):
        self._previous_location = location

    def resizeEvent(self, event):
        rect = self._ui.nameLineEdit.rect()
        pos = self._ui.nameLineEdit.pos()
        self._invalidNameLabel.setPixmap(self._invalidPixmap.scaledToHeight(rect.height() / 2))
        self._invalidNameLabel.move(pos.x() - rect.height() / 2, pos.y() + rect.height() / 4)
        self._invalidNameLabel.setFixedSize(self._invalidNameLabel.sizeHint())
        rect = self._ui.packageNameLineEdit.rect()
        pos = self._ui.packageNameLineEdit.pos()
        self._invalidPackageLabel.setPixmap(self._invalidPixmap.scaledToHeight(rect.height() / 2))
        self._invalidPackageLabel.move(pos.x() - rect.height() / 2, pos.y() + rect.height() / 4)
        self._invalidPackageLabel.setFixedSize(self._invalidPackageLabel.sizeHint())
        rect = self._ui.iconLineEdit.rect()
        pos = self._ui.iconLineEdit.pos()
        self._invalidIconLabel.setPixmap(self._invalidPixmap.scaledToHeight(rect.height() / 2))
        self._invalidIconLabel.move(pos.x() - rect.height() / 2, pos.y() + rect.height() / 4)
        self._invalidIconLabel.setFixedSize(self._invalidIconLabel.sizeHint())

    def isComplete(self):
        name_status = False
        if len(self._ui.nameLineEdit.text()) > 0:
            name_status = True

        package_status = isIdentifier(str(self._ui.packageNameLineEdit.text()))

        image_status = os.path.exists(self._ui.iconLineEdit.text()) if len(self._ui.iconLineEdit.text()) > 0 else True

        self._invalidNameLabel.setVisible(not name_status)
        self._invalidPackageLabel.setVisible(not package_status)
        self._invalidIconLabel.setVisible(not image_status)

        return name_status and package_status and image_status


class PortsWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent=None):
        super(PortsWizardPage, self).__init__(parent)

        self.setTitle('Set Step Ports')
        self.setSubTitle('Set the ports for the workflow step.')

        self._ui = Ui_Ports()
        self._ui.setupUi(self)

        self._ui.portTableWidget.setColumnCount(2)
        self._ui.portTableWidget.setShowGrid(False)
        self._ui.portTableWidget.setHorizontalHeaderLabels(['Type', 'Object'])
        horizontal_header = self._ui.portTableWidget.horizontalHeader()
        horizontal_header.setStretchLastSection(True)

        self._updateUi()
        self._defineFields()
        self._makeConnections()

    def _defineFields(self):
        self.registerField(PORTS_FIELD, self._ui.portTableWidget)

    def _updateUi(self):
        have_selected_rows = len(self._ui.portTableWidget.selectedIndexes()) > 0
        self._ui.removeButton.setEnabled(have_selected_rows)

    def _makeConnections(self):
        self._ui.addButton.clicked.connect(self._addPort)
        self._ui.removeButton.clicked.connect(self._removePort)
        self._ui.portTableWidget.itemSelectionChanged.connect(self._updateUi)

    def _addPort(self):

        def createPortTypeComboBox():
            cb = QtWidgets.QComboBox()
            cb.addItems(['provides', 'uses'])

            return cb

        next_row = self._ui.portTableWidget.rowCount()
        self._ui.portTableWidget.insertRow(next_row)
        self._ui.portTableWidget.setCellWidget(next_row, 0, createPortTypeComboBox())

    def _removePort(self):
        indexes = self._ui.portTableWidget.selectedIndexes()
        reversed_rows = indexes[::2]
        reversed_rows.reverse()
        for row in reversed_rows:
            self._ui.portTableWidget.removeRow(row.row())


class ConfigWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent=None):
        super(ConfigWizardPage, self).__init__(parent)

        self.setTitle('Configure Workflow Step')
        self.setSubTitle('Setup the configuration for the workflow step.')

        self._ui = Ui_Config()
        self._ui.setupUi(self)

        self._ui.identifierCheckBox.setChecked(True)

        horizontal_header = self._ui.configTableWidget.horizontalHeader()
        horizontal_header.setStretchLastSection(True)
#         self._addConfigurationRow()
#         self._ui.configTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem('Identifier'))
#         self._ui.configTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(''))

        self._updateUi()
        self._makeConnections()

    def _defineFields(self):
        self.registerField(IDENTIFIER_CHECKBOX, self._ui.identifierCheckBox)

    def _makeConnections(self):
        self._ui.addButton.clicked.connect(self._addConfigurationRow)
        self._ui.removeButton.clicked.connect(self._removeConfigurationRow)
        self._ui.configTableWidget.itemSelectionChanged.connect(self._updateUi)

    def _updateUi(self):
        have_selected_rows = len(self._ui.configTableWidget.selectedIndexes()) > 0
        self._ui.removeButton.setEnabled(have_selected_rows)

    def _addConfigurationRow(self):
        next_row = self._ui.configTableWidget.rowCount()
        self._ui.configTableWidget.insertRow(next_row)

    def _removeConfigurationRow(self):
        indexes = self._ui.configTableWidget.selectedIndexes()
        reversed_rows = indexes[::2]
        reversed_rows.reverse()
        for row in reversed_rows:
            self._ui.configTableWidget.removeRow(row.row())


class MiscWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent=None):
        super(MiscWizardPage, self).__init__(parent)

        self.setTitle('Miscellaneous Options')
        self.setSubTitle('Specify miscellaneous options for the plugin.')

        self._ui = Ui_Misc()
        self._ui.setupUi(self)

        self.registerField(AUTHOR_NAME_FIELD, self._ui.authorNameLineEdit)
        self.registerField(CATEGORY_FIELD, self._ui.categoryLineEdit)
        self.registerField(PLUGIN_LOCATION_FIELD, self._ui.pluginLocationEdit)

    def initializePage(self):
        predefinedName = self.field(PREDEFINED_IMAGE_FIELD)
        filename = getPredefinedImageLocation(predefinedName)
        icon_filename = self.field(IMAGE_FILE_FIELD)
        if filename == icon_filename and predefinedName != 'Default':
            self._ui.categoryLineEdit.setText(predefinedName)


class OutputWizardPage(QtWidgets.QWizardPage):

    def __init__(self, parent=None):
        super(OutputWizardPage, self).__init__(parent)

        self.setTitle('Output Files')
        self.setSubTitle('Specify where you want the wizard to put the generated skeleton code.')

        self._ui = Ui_Output()
        self._ui.setupUi(self)

        self._invalidPixmap = QtGui.QPixmap(':wizard/images/cross.png')
        self._invalidDirectoryLabel = QtWidgets.QLabel(self)
        self._invalidDirectoryLabel.setStyleSheet('border: none; padding: 0px;')

        self.registerField(OUTPUT_DIRECTORY_FIELD + '*', self._ui.directoryLineEdit)

        self._makeConnections()

    def _makeConnections(self):
        self._ui.directoryLineEdit.textChanged.connect(self.completeChanged)
        self._ui.directoryButton.clicked.connect(self._chooseDirectory)

    def _chooseDirectory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Select Output Directory', dir=self._ui.directoryLineEdit.text(), options=QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks | QtWidgets.QFileDialog.ReadOnly)
        if len(directory) > 0:
            self._ui.directoryLineEdit.setText(directory)

    def setDirectory(self, location):
        self._ui.directoryLineEdit.setText(location)

    def resizeEvent(self, event):
        rect = self._ui.directoryLineEdit.rect()
        pos = self._ui.directoryLineEdit.pos()
        self._invalidDirectoryLabel.setPixmap(self._invalidPixmap.scaledToHeight(rect.height() / 2))
        self._invalidDirectoryLabel.move(pos.x() - rect.height() / 2, pos.y() + rect.height() / 4)
        self._invalidDirectoryLabel.setFixedSize(self._invalidDirectoryLabel.sizeHint())

    def isComplete(self):
        status = False
        directory = self._ui.directoryLineEdit.text()
        if os.path.isdir(directory) and os.access(directory, os.W_OK | os.X_OK):
            status = True

        self._invalidDirectoryLabel.setVisible(not status)

        return status


def isIdentifier(ident):
    """Determines, if string is valid Python identifier."""

    if not isinstance(ident, str):
        return False

    # Resulting AST of simple identifier is <Module [<Expr <Name "foo">>]>
    try:
        root = ast.parse(ident)
    except SyntaxError:
        return False

    if not isinstance(root, ast.Module):
        return False

    if len(root.body) != 1:
        return False

    if not isinstance(root.body[0], ast.Expr):
        return False

    if not isinstance(root.body[0].value, ast.Name):
        return False

    if root.body[0].value.id != ident:
        return False

    return True


def getPredefinedImageLocation(predefinedName):
    filename = imageNameMap[predefinedName]
    if is_frozen():
        image_file_dir = os.path.join(sys._MEIPASS, 'res', 'images')
    else:
        image_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'qt', 'images')
    return os.path.join(image_file_dir, filename)
