'''
Created on Feb 27, 2013

@author: hsorby
'''
from __future__ import absolute_import

import os, sys
import unittest

from PySide import QtGui
try:
    from PySide.QtTest import QTest
    HAVE_QTTEST = True
except ImportError:
    HAVE_QTTEST = False

DISABLE_GUI_TESTS = True

class PointCloudSerializerTestCase(unittest.TestCase):


    def setUp(self):
        if os.name == 'posix' and 'DISPLAY' not in os.environ:
            self.pixmap_unavailable = True
        else:
            self.pixmap_unavailable = False
            self.my_test_app = QtGui.QApplication.instance()
            if self.my_test_app is None:
                self.my_test_app = QtGui.QApplication(sys.argv)

    def tearDown(self):
        if not self.pixmap_unavailable:
            del self.my_test_app

    def testStep(self):
        if self.pixmap_unavailable:
            return

        from mapclientplugins.pointcloudserializerstep.step import PointCloudSerializerStep
        mystep = PointCloudSerializerStep('empty')

        self.assertFalse(mystep.isConfigured())

    def testStepStatus(self):
        from mapclientplugins.pointcloudserializerstep.widgets.configuredialog import ConfigureDialogState
        state = ConfigureDialogState()

        self.assertEqual(state.identifier(), '')

        newstate = ConfigureDialogState('here')
        self.assertEqual(newstate.identifier(), 'here')

    if sys.version_info >= (2, 7, 0):
        @unittest.skipIf(DISABLE_GUI_TESTS, 'GUI tests are disabled')
        def testConfigure(self):
            if self.pixmap_unavailable:
                return

            from mapclientplugins.pointcloudserializerstep.step import PointCloudSerializerStep
            mystep = PointCloudSerializerStep()
            mystep.configure()

    if HAVE_QTTEST:
        def testConfigureDialog(self):
            if self.pixmap_unavailable:
                return

            from mapclientplugins.pointcloudserializerstep.widgets.configuredialog import ConfigureDialog, ConfigureDialogState
            state = ConfigureDialogState()
            d = ConfigureDialog(state)

            self.assertEqual(d._ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).isEnabled(), False)
            QTest.keyClicks(d._ui.identifierLineEdit, 'hello')
            self.assertEqual(d._ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).isEnabled(), True)
            # QTest.mouseClick(d._ui.buttonBox.button(QtGui.QDialogButtonBox.Ok), QtCore.Qt.LeftButton)
            newstate = d.getState()
            self.assertEqual(newstate.identifier(), 'hello')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
