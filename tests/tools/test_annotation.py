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
import re, os

from PySide import QtGui

from tests import utils
from mapclient.tools.annotation.annotationtool import AnnotationTool, _SECTION_HEADER_RE, _NAMESPACE_RE
from mapclient.tools.annotation.annotationdialog import AnnotationDialog

utils.createTestApplication()

DISABLE_GUI_TESTS = False

class AnnotationToolTestCase(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testReadVocab(self):
        a = AnnotationTool()

        self.assertEqual(10, len(a.getTerms()))
        self.assertEqual('1.0', a._vocab._version)
        self.assertEqual('http://physiomeproject.org/workflow', a._vocab._namespace)

    def testSectionHeaderRe(self):
        s = re.compile(_SECTION_HEADER_RE)

        test_1 = '[hello]'
        r = s.match(test_1)
        self.assertEqual('hello', r.group(1))

    def testPhysiomeNamespaceRe(self):
        s = re.compile(_NAMESPACE_RE.format('http://physiomeproject.org/workflow', '1.0'))
        test_1 = '<http://physiomeproject.org/workflow/1.0/rdf-schema#port> <http://physiomeproject.org/workflow/1.0/rdf-schema#port> <http://physiomeproject.org/workflow/1.0/rdf-schema#port>.'
        test_2 = '<http://physiomeproject.org/workflow/1.0/rdf-schema#uses> <http://physiomeproject.org/workflow/1.0/rdf-schema#pointcloud> <http://physiomeproject.org/workflow/1.0/rdf-schema#port>.'

        r_1 = s.match(test_1)
        self.assertEqual('port', r_1.group(1))
        self.assertEqual('port', r_1.group(2))
        self.assertEqual('port', r_1.group(3))

        r_2 = s.match(test_2)
        self.assertEqual('uses', r_2.group(1))
        self.assertEqual('pointcloud', r_2.group(2))
        self.assertEqual('port', r_2.group(3))


    if not DISABLE_GUI_TESTS:
        def testAnnotationDialog(self):
            QtGui.QApplication.instance()
            to_path = os.path.join(os.path.dirname(utils.__file__), 'test_resources/annotation_test/')
            if not os.path.exists(to_path):
                os.mkdir(to_path)

            dlg = AnnotationDialog(to_path)
            dlg.setModal(True)
            # if dlg.exec_():
            #    pass
#            shutil.rmtree(to_path)



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
