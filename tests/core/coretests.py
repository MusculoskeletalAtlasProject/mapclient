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

def suite():
    tests = unittest.TestSuite()

    from tests.core.test_pluginframework import PluginFrameworkTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginFrameworkTestCase))

    from tests.core.test_mainapplication import MainApplicationTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(MainApplicationTestCase))

    from tests.core.test_workflowscene import WorkflowSceneTestCase, WorkflowDependencyGraphTestCase, DictUtilsTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(WorkflowSceneTestCase))
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(WorkflowDependencyGraphTestCase))
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(DictUtilsTestCase))

    from tests.core.test_threadcommandmanager import ThreadCommandManagerTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(ThreadCommandManagerTestCase))

    return tests

def load_tests(loader, tests, pattern):
    return suite()

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
