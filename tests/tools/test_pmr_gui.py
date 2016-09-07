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
import unittest, sys

from utils import createTestApplication

DISABLE_GUI_TESTS = True

createTestApplication()


class PMRSearchDialogTestCase(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass

    if sys.version < '2.7.0':
        @unittest.skipIf(DISABLE_GUI_TESTS, 'GUI tests are disabled')
        def testPMRSearchDialog(self):        
            from mapclient.tools.pmr.pmrsearchdialog import PMRSearchDialog
            dlg = PMRSearchDialog()
            dlg.setModal(True)
            if dlg.exec_():
                ws = dlg.getSelectedWorkspace()
                print('the winner has selected:')
                print(ws)
            
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
