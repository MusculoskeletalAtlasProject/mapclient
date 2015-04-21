#!/usr/bin/python
'''
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
'''

import unittest

from utils import parseUnitTestOutput

class UnitTestOutputTestCase(unittest.TestCase):

    def test1(self):
        [rc, p, f] = parseUnitTestOutput('test_resources/utils/utoutput1.log')
        self.assertEqual(rc, 0)
        self.assertEqual(p, 9)
        self.assertEqual(f, 0)

    def test2(self):
        [rc, p, f] = parseUnitTestOutput('test_resources/utils/utoutput2.log')
        self.assertEqual(rc, 1)
        self.assertEqual(p, 8)
        self.assertEqual(f, 1)

    def test3(self):
        [rc, p, f] = parseUnitTestOutput('test_resources/utils/utoutput3.log')
        self.assertEqual(rc, 1)
        self.assertEqual(p, 12)
        self.assertEqual(f, 2)

    def test4(self):
        [rc, p, f] = parseUnitTestOutput('test_resources/utils/utoutput4.log')
        self.assertEqual(rc, 1)
        self.assertEqual(p, 13)
        self.assertEqual(f, 1)
        
    def test5(self):
        [rc, p, f] = parseUnitTestOutput('test_resources/utils/utoutput5.log')
        self.assertEqual(rc, 0)
        self.assertEqual(p, 21)
        self.assertEqual(f, 0)
      
    def test6(self):
        [rc, p, f] = parseUnitTestOutput('test_resources/utils/utoutput6.log')
        self.assertEqual(rc, 1)
        self.assertEqual(p, 0)
        self.assertEqual(f, 0)
      
    def test7(self):
        [rc, p, f] = parseUnitTestOutput('test_resources/utils/utoutput7.log')
        self.assertEqual(rc, 0)
        self.assertEqual(p, 31)
        self.assertEqual(f, 0)
      
def suite():
    tests = unittest.TestSuite()
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(UnitTestOutputTestCase))
    return tests

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())

