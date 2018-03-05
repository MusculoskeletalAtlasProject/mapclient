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
import unittest

import os
import shutil
import tempfile

from PySide import QtGui

from mapclient.tools.pluginwizard import wizarddialog
from mapclient.tools.pluginwizard.skeleton import SkeletonOptions, Skeleton
from mapclient.tools.pluginwizard.skeleton import PLUGIN_NAMESPACE

from tests.utils import createTestApplication
from mapclient.core.utils import which
import subprocess

createTestApplication()
# import mapclient.widgets.resources_rc

from tests import utils

test_path = os.path.join(os.path.dirname(utils.__file__), 'test_resources', 'wizard_test')
IMAGE_FILE_NAME = 'logo.png'
PLUGIN_WRITE_TO_DIRECTORY = test_path
PLUGIN_PACKAGE_NAME = 'abcdalphastep'
PLUGIN_NAME = 'Abcd Alpha'
PLUGIN_IMAGE_FILE = os.path.join(test_path, IMAGE_FILE_NAME)
CATEGORY = 'Viewer'
AUTHOR_NAME = 'Prince of Persia'


# ... just use unittest2 for backward compatibility?  or just use assertTrue?
class _TestCase(unittest.TestCase):

    def assertIn(self, a, b, *args, **kwargs):
        """Python < v2.7 compatibility.  Assert "a" in "b" """
        try:
            f = super(_TestCase, self).assertIn
        except AttributeError:
            self.assertTrue(a in b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)

    def assertNotIn(self, a, b, *args, **kwargs):
        """Python < v2.7 compatibility.  Assert "a" NOT in "b" """
        try:
            f = super(_TestCase, self).assertNotIn
        except AttributeError:
            self.assertFalse(a in b, *args, **kwargs)
        else:
            f(a, b, *args, **kwargs)


class WizardTestCase(_TestCase):

    def setUp(self):
        self.working_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.working_dir, ignore_errors=True)

#     def testRunWizard(self):
#         """
#         Visual test for wizard, uncomment to manually test.
#         """
#         dlg = wizarddialog.WizardDialog()
#         result = dlg.exec_()
#         self.assertTrue(result == dlg.Accepted or result == dlg.Rejected)
    def testWizard(self):
        dlg = wizarddialog.WizardDialog()

        p1 = dlg.page(1)
        p1._ui.nameLineEdit.setText(PLUGIN_NAME)
        p1._ui.iconLineEdit.setText(PLUGIN_IMAGE_FILE)
        p2 = dlg.page(2)
        p2._ui.portTableWidget.insertRow(0)
        cb = QtGui.QComboBox()
        cb.addItems(['provides', 'uses'])
        p2._ui.portTableWidget.setCellWidget(0, 0, cb)
        p2._ui.portTableWidget.setItem(0, 1, QtGui.QTableWidgetItem('http://my.example.org/1.0/workflowstep#octopus'))
        p3 = dlg.page(3)
        p3._ui.configTableWidget.setItem(0, 1, QtGui.QTableWidgetItem('xxx'))
        p4 = dlg.page(4)
        p4._ui.authorNameLineEdit.setText(AUTHOR_NAME)
        p4._ui.categoryLineEdit.setText(CATEGORY)
        p5 = dlg.page(5)
        p5._ui.directoryLineEdit.setText(self.working_dir)

        dlg.accept()

        options = dlg.getOptions()
        self.assertEqual(PLUGIN_NAME, options.getName())
        self.assertEqual(IMAGE_FILE_NAME, options.getImageFile())
        self.assertEqual(PLUGIN_PACKAGE_NAME, options.getPackageName())
        self.assertEqual(self.working_dir, options.getOutputDirectory())
        self.assertEqual(1, options.portCount())
        self.assertEqual([u'http://physiomeproject.org/workflow/1.0/rdf-schema#provides', u'http://my.example.org/1.0/workflowstep#octopus'], options.getPort(0))
        self.assertEqual(1, options.configCount())
        self.assertEqual([u'identifier', u''], options.getConfig(0))
        self.assertEqual(CATEGORY, options.getCategory())
        self.assertEqual(AUTHOR_NAME, options.getAuthorName())

    def testSkeleton1(self):

        local_package_name = PLUGIN_PACKAGE_NAME
        package_full_name = PLUGIN_NAMESPACE + '.' + PLUGIN_PACKAGE_NAME
        package_dir = os.path.join(self.working_dir, package_full_name)
        step_dir = os.path.join(
            package_dir, PLUGIN_NAMESPACE, local_package_name)

        options = SkeletonOptions()
        options.setImageFile(IMAGE_FILE_NAME)
        options.setIcon(QtGui.QPixmap(PLUGIN_IMAGE_FILE))
        options.setName(PLUGIN_NAME + str(1))
        options.setPackageName(local_package_name)
        options.setOutputDirectory(self.working_dir)
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'object')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'http://my.example.org/1.0/workflowstep#octopus')
        options.addConfig('identifier', '')
        options.setAuthorName(AUTHOR_NAME)
        options.setCategory(CATEGORY)
        pyside_rcc = determinePysideURccExecutable()

        s = Skeleton(options, pyside_rcc)
        s.write()

        step_file = os.path.join(step_dir, 'step.py')
        self.assertTrue(os.path.exists(step_file))

        file_contents = open(step_file).read()
        self.assertIn('octopus', file_contents)
        self.assertIn('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', file_contents)
        self.assertIn('return self._config[', file_contents)
        self.assertIn('] = identifier', file_contents)
        self.assertIn('self._category = \'' + CATEGORY + '\'', file_contents)
        self.assertNotIn('{setidentifiercontent}', file_contents)
        self.assertNotIn('{serializecontent}', file_contents)
        self.assertNotIn('{serializesetvalues}', file_contents)


        resources_file = os.path.join(step_dir, 'resources_rc.py')
        self.assertTrue(os.path.exists(resources_file))

        config_file = os.path.join(step_dir, 'configuredialog.py')
        self.assertTrue(os.path.exists(config_file))

        config_contents = open(config_file).read()
        self.assertIn('validate', config_contents)

    def testSkeleton2(self):

        local_package_name = PLUGIN_PACKAGE_NAME
        package_full_name = PLUGIN_NAMESPACE + '.' + PLUGIN_PACKAGE_NAME
        package_dir = os.path.join(self.working_dir, package_full_name)
        step_dir = os.path.join(
            package_dir, PLUGIN_NAMESPACE, local_package_name)

        options = SkeletonOptions()
        options.setImageFile(IMAGE_FILE_NAME)
        options.setIcon(QtGui.QPixmap(PLUGIN_IMAGE_FILE))
        options.setName(PLUGIN_NAME + str(2))
        options.setPackageName(local_package_name)
        options.setOutputDirectory(self.working_dir)
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'object')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'number')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'http://my.example.org/1.0/workflowstep#octopus')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'int')

        pyside_rcc = determinePysideURccExecutable()

        s = Skeleton(options, pyside_rcc)
        s.write()

        step_file = os.path.join(step_dir, 'step.py')
        self.assertTrue(os.path.exists(step_file))

        file_contents = open(step_file).read()
        self.assertIn('octopus', file_contents)
        self.assertIn('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', file_contents)
        self.assertIn('# TODO: The string must be replaced with', file_contents)
        self.assertIn('# TODO: Must actually set the step', file_contents)
        self.assertNotIn('{setidentifiercontent}', file_contents)
        self.assertNotIn('{serializecontent}', file_contents)
        self.assertNotIn('{serializesetvalues}', file_contents)

        resources_file = os.path.join(step_dir, 'resources_rc.py')
        self.assertTrue(os.path.exists(resources_file))

    def testSkeleton3(self):

        local_package_name = PLUGIN_PACKAGE_NAME
        package_full_name = PLUGIN_NAMESPACE + '.' + PLUGIN_PACKAGE_NAME
        package_dir = os.path.join(self.working_dir, package_full_name)
        step_dir = os.path.join(
            package_dir, PLUGIN_NAMESPACE, local_package_name)

        options = SkeletonOptions()
        options.setImageFile(IMAGE_FILE_NAME)
        options.setIcon(QtGui.QPixmap(PLUGIN_IMAGE_FILE))
        options.setName(PLUGIN_NAME + str(3))
        options.setPackageName(local_package_name)
        options.setOutputDirectory(self.working_dir)
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'object')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'number')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'http://my.example.org/1.0/workflowstep#octopus')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'int')
        options.addConfig('identifier', '')
        options.addConfig('Cabbage', 'Brown')
        options.addConfig('Path', '')
        options.addConfig('Carrot', 'tis a long way down')

        pyside_rcc = determinePysideURccExecutable()

        s = Skeleton(options, pyside_rcc)
        s.write()

        step_file = os.path.join(step_dir, 'step.py')
        self.assertTrue(os.path.exists(step_file))

        file_contents = open(step_file).read()
        self.assertIn('octopus', file_contents)
        self.assertIn('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', file_contents)
        self.assertIn('Cabbage', file_contents)
        self.assertIn('Carrot', file_contents)
        self.assertNotIn('{setidentifiercontent}', file_contents)
        self.assertNotIn('{serializecontent}', file_contents)
        self.assertNotIn('{serializesetvalues}', file_contents)

        resources_file = os.path.join(step_dir, 'resources_rc.py')
        self.assertTrue(os.path.exists(resources_file))

        config_file = os.path.join(step_dir, 'configuredialog.py')
        self.assertTrue(os.path.exists(config_file))

    def testSkeleton4(self):

        local_package_name = PLUGIN_PACKAGE_NAME
        package_full_name = PLUGIN_NAMESPACE + '.' + PLUGIN_PACKAGE_NAME
        package_dir = os.path.join(self.working_dir, package_full_name)
        step_dir = os.path.join(
            package_dir, PLUGIN_NAMESPACE, local_package_name)

        options = SkeletonOptions()
        options.setImageFile(IMAGE_FILE_NAME)
        options.setIcon(QtGui.QPixmap(PLUGIN_IMAGE_FILE))
        options.setName(PLUGIN_NAME + str(4))
        options.setPackageName(local_package_name)
        options.setOutputDirectory(self.working_dir)
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'object')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'number')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'http://my.example.org/1.0/workflowstep#octopus')
        options.addPort('http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'int')
        options.addConfig('Cabbage', 'Brown')
        options.addConfig('Path', '')
        options.addConfig('Carrot', 'tis a long way down')

        pyside_rcc = determinePysideURccExecutable()

        s = Skeleton(options, pyside_rcc)
        s.write()

        self.assertTrue(os.path.exists(package_dir))
        step_file = os.path.join(step_dir, 'step.py')
        self.assertTrue(os.path.exists(step_file))

        file_contents = open(step_file).read()
        self.assertIn('octopus', file_contents)
        self.assertIn('http://physiomeproject.org/workflow/1.0/rdf-schema#provides', file_contents)
        self.assertIn('Cabbage', file_contents)
        self.assertIn('Carrot', file_contents)
        self.assertNotIn('{setidentifiercontent}', file_contents)
        self.assertNotIn('{serializecontent}', file_contents)
        self.assertNotIn('{serializesetvalues}', file_contents)

        resources_file = os.path.join(step_dir, 'resources_rc.py')
        self.assertTrue(os.path.exists(resources_file))

        config_file = os.path.join(step_dir, 'configuredialog.py')
        self.assertTrue(os.path.exists(config_file))


def determinePysideURccExecutable():
        pyside_rcc_potentials = ['pyside-rcc']
        return which(pyside_rcc_potentials[0])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
