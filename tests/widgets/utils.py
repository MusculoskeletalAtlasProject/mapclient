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

class UtilsTestCase(unittest.TestCase):

    size = 60
    h = 10
    alpha = 5


    def portPosition(self, n, i):
#         print(self.size / 2.0 - self.h / 2.0, -(n - 1) * self.h - (n - 1) / 2 * self.alpha / 2.0, (self.h + self.alpha / 2.0) * i)
        return self.size / 2.0 - (n * self.h + (n - 1) * self.alpha) / 2.0 + (self.h + self.alpha) * i
#         return self.size / 2.0 - self.h / 2.0 - (n - 1) * self.h - (n - 1) / 2 * self.alpha / 2.0 + (self.h + self.alpha / 2.0) * i

    def testPortLocation_neq1(self):
        loc = self.portPosition(1, 0)
        self.assertEqual(25, loc)

    def testPortLocation_neq2(self):
        loc = self.portPosition(2, 0)
        self.assertEqual(17.5, loc)
        loc = self.portPosition(2, 1)
        self.assertEqual(32.5, loc)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
