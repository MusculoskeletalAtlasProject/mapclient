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

from mapclient.settings import info

class InfoTestCase(unittest.TestCase):


    def testABOUT(self):
        assert(len(info.ABOUT.keys()) == 4)
        assert('name' in info.ABOUT)
        assert('version' in info.ABOUT)
        assert('license' in info.ABOUT)
        assert('description' in info.ABOUT)
        
    def testCREDITS(self):
        assert(len(info.CREDITS.keys()) == 3)
        assert('programming' in info.CREDITS)
        assert('artwork' in info.CREDITS)
        assert('documentation' in info.CREDITS)
        for contributor in info.CREDITS['programming']:
            assert(len(contributor.keys()) == 2)
            assert('name' in contributor)
            assert('email' in contributor)
        for contributor in info.CREDITS['artwork']:
            assert(len(contributor.keys()) == 2)
            assert('name' in contributor)
            assert('email' in contributor)
        for contributor in info.CREDITS['documentation']:
            assert(len(contributor.keys()) == 2)
            assert('name' in contributor)
            assert('email' in contributor)
            
    def testNames(self):
        assert(info.APPLICATION_NAME == 'MAP Client')
        assert(info.ORGANISATION_NAME == 'Musculo Skeletal')
        assert(info.ORGANISATION_DOMAIN == 'musculoskeletal.org')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInfo']
    unittest.main()
