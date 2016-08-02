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

from mapclient.core.checks import WizardToolChecks
from mapclient.core.utils import which
import subprocess

class ChecksTestCase(unittest.TestCase):


    def testWizardToolChecks(self):
        pyside_rcc = which('pyside-rcc')
        pyside_uic = which('pyside-uic')
        options = {}
        options['lineEditPySideRCC'] = pyside_rcc
        options['lineEditPySideUIC'] = pyside_uic

        # Do some pretests on uic executable
        pyside_uic = options['lineEditPySideUIC']
        p = subprocess.Popen([pyside_uic, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if ((stdout and int(stdout) != 0) or not stdout) and 'SyntaxError' in stderr:
            # Try another executable
            pyside_uic = which('pyside-uic-py2')
            options['lineEditPySideUIC'] = pyside_uic

        c = WizardToolChecks(options)
        self.assertTrue(c.doCheck())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testCheckPySideTools']
    unittest.main()
