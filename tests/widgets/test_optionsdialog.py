"""
Created on Jun 9, 2015

@author: hsorby
"""
import unittest

from tests.utils import createTestApplication

createTestApplication()

class OptionsDialogTestCase(unittest.TestCase):


    def testOptionsDialogEmptyOptions(self):
        from mapclient.view.managers.options.optionsdialog import OptionsDialog
        d = OptionsDialog()
        options = {}
        d.load(options)
        self.assertTrue(d.isModified())
        saved_options = d.save()
        self.assertNotEqual(options, saved_options)

    def testOptionsDialogNonEmptyOptions(self):
        from mapclient.view.managers.options.optionsdialog import OptionsDialog
        d = OptionsDialog()
        options = {u'lineEditGitExecutable': u'', u'lineEditPySideRCC': u'', u'lineEditVirtualEnvironmentPath': u'', u'lineEditPySideUIC': u'', u'checkBoxShowStepNames': True}
        d.load(options)
        self.assertFalse(d.isModified())
        saved_options = d.save()
        self.assertEqual(options, saved_options)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testOptionsDialog']
    unittest.main()

