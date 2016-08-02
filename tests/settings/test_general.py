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

from PySide import QtCore

from mapclient.settings.general import getLogDirectory
from tests.utils import createTestApplication

createTestApplication()

class GeneralTestCase(unittest.TestCase):


    def tearDown(self):
        ll = getLogDirectory()
        if os.path.exists(ll):
            os.rmdir(ll)
            
        cf = QtCore.QSettings().fileName()
        if os.path.exists(cf):
            os.remove(cf)
            
        cd, _ = os.path.splitext(cf)
        if os.path.exists(cd):
            os.rmdir(cd)
            
    def testGetLogLocation(self):
        ll = getLogDirectory()
        self.assertTrue(os.path.exists(ll))
        self.assertTrue(os.access(ll, os.W_OK | os.X_OK))
        
        