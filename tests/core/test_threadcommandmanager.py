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
import os
import shutil
from time import sleep

from mapclient.core.threadcommandmanager import CommandCopyDirectory, ThreadCommandManager, which
from tests import utils


class ThreadCommandManagerTestCase(unittest.TestCase):


    def setUp(self):
        self._command_finished = False


    def tearDown(self):
        '''
        Add a backup path removal if path still exists due to exception in test.
        '''
        to_path = os.path.join(os.path.dirname(utils.__file__), 'test_resources/utils_copy/')
        if os.path.exists(to_path):
            shutil.rmtree(to_path)


    def testCopyDirectory(self):
        # create to directory

        from_path = os.path.join(os.path.dirname(utils.__file__), 'test_resources/utils/')
        to_path = os.path.join(os.path.dirname(utils.__file__), 'test_resources/utils_copy/')

        os.mkdir(to_path)

        c = CommandCopyDirectory(from_path, to_path)
        c.run()
        self.assertTrue(os.path.exists(os.path.join(to_path, 'utoutput1.log')))

        shutil.rmtree(to_path)

    def testExecutetEmptyQueue(self):
        m = ThreadCommandManager()
        m.next()
        self.assertEqual(0, len(m._queue))

    def testAddCommand(self):

        c = CommandCopyDirectory('', '')
        m = ThreadCommandManager()
        m.addCommand(c)

    def testRunCommand(self):

        from_path = os.path.join(os.path.dirname(utils.__file__), 'test_resources/utils/')
        to_path = os.path.join(os.path.dirname(utils.__file__), 'test_resources/utils_copy/')

        os.mkdir(to_path)

        c = CommandCopyDirectory(from_path, to_path)
        m = ThreadCommandManager()
        m.queue_empty.connect(self.commandFinished)
        m.addCommand(c)

        m.next()
        count = 0
        while not self._command_finished and count < 200:
            sleep(0.001)
            count += 1

        shutil.rmtree(to_path)

    def commandFinished(self):
        self._command_finished = True

    def testWhichNotExists(self):
        result = which('blahblah')
        self.assertEqual(0, len(result))

#        self.assertTrue(os.path.exists(os.path.join(to_path, 'utoutput1.log')))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
