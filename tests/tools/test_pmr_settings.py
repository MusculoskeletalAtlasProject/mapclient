"""
Created on Feb 26, 2015

@author: hsorby
"""
import unittest

from mapclient.tools.pmr.settings.general import PMR

class PMRToolSettingsTestCase(unittest.TestCase):


    def testPMR(self):
        info = PMR()
        host = info.host()

        self.assertIsInstance(host, unicode)

        self.assertTrue(info.addHost('garbage'))
        self.assertIn('garbage', info._instances)

        self.assertFalse(info.setActiveHost('rubbish'))
        self.assertTrue(info.setActiveHost('garbage'))


        self.assertTrue(info.removeHost('garbage'))
        self.assertTrue(info.host() is None)
        self.assertFalse(info.removeHost('garbage'))

#         info.writeSettings()




if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
