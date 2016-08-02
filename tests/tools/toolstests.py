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

def suite():
    tests = unittest.TestSuite()

    from tests.tools.test_annotation import AnnotationToolTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(AnnotationToolTestCase))
    
    from tests.tools.test_plugin_updater import PluginUpdaterTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(PluginUpdaterTestCase))
    
    from tests.tools.test_pmr_core import TokenHelperTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(TokenHelperTestCase))
    
    from tests.tools.test_pmr_gui import PMRSearchDialogTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(PMRSearchDialogTestCase))
    
    from tests.tools.test_pmr_settings import PMRToolSettingsTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(PMRToolSettingsTestCase))
    
    from tests.tools.test_pmr import PMRToolTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(PMRToolTestCase))
    
    from tests.tools.test_wizard import WizardTestCase
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(WizardTestCase))
    
    return tests

def load_tests(loader, tests, pattern):
    return suite()

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
