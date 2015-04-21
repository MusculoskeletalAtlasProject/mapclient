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
import os
import shutil
import tempfile
import unittest
import logging

from mapclient.core.pluginframework import PluginManager
from mapclient.core.pluginframework import PluginSiteManager
from tests.utils import ConsumeOutput

class PluginFrameworkTestCase(unittest.TestCase):

    def testLoadPlugins(self):

        redirectstdout = ConsumeOutput()
        redirect_handler = logging.StreamHandler(redirectstdout)
        logger = logging.getLogger('mapclient.core.pluginframework')
        logger.setLevel(logging.INFO)
        for handler in logger.handlers:
            logger.removeHandler(handler)

        logger.addHandler(redirect_handler)

        pm = PluginManager()
        pm.load()

        redirect_handler.flush()

        features = [True for msg in redirectstdout.messages if "Loaded plugin 'pointcloudserializerstep' version [0.3.0] by Hugh Sorby" in msg]
        self.assertEqual(1, len(features))

        logger.removeHandler(redirect_handler)
        redirect_handler.close()


class PluginSiteTestCase(unittest.TestCase):

    def setUp(self):
        self.working_dir = tempfile.mkdtemp()
        self.manager = PluginSiteManager()

    def tearDown(self):
        shutil.rmtree(self.working_dir, ignore_errors=True)

    def generate_package(self, package_name):
        extras = package_name.split('.')
        os.mkdir(os.path.join(self.working_dir, package_name))
        for f in range(1, len(extras) + 1):
            target = os.path.join(self.working_dir, package_name, *extras[:f])
            os.mkdir(target)
            with open((os.path.join(target, '__init__.py')), 'w'):
                pass

    def test_site_pth_empty(self):
        pth = self.manager.generate_pth_entries(self.working_dir)
        self.assertEqual(pth, [])

        # plain files should be ignore, too.
        with open(os.path.join(self.working_dir, 'dummy_file'), 'w'):
            pass

        self.assertEqual(pth, [])

    def test_site_pth_with_packages(self):
        self.generate_package('testing.package')
        pth = self.manager.generate_pth_entries(self.working_dir)
        self.assertEqual(pth, [
            os.path.join(self.working_dir, 'testing.package'),
        ])

    def test_load_site_base(self):
        self.generate_package('testing.package')
        self.manager.build_site(self.working_dir)
        self.manager.load_site(self.working_dir)
        module = __import__('testing.package').package
        self.assertEqual(module.__file__, os.path.join(
            self.working_dir, 'testing.package', 'testing', 'package',
            '__init__.py'))

    def test_load_site_just_a_dir(self):
        # what if it's just a random dir?
        os.mkdir(os.path.join(self.working_dir, 'testing.notapackage'))
        pth = self.manager.generate_pth_entries(self.working_dir)
        # XXX note how it still thinks this is a package
        self.assertEqual(pth, [
            os.path.join(self.working_dir, 'testing.notapackage'),
        ])

        # shouldn't really cause any ill effects though, but test this
        # to be sure.
        self.manager.build_site(self.working_dir)
        self.manager.load_site(self.working_dir)
        # this should be an import error.
        self.assertRaises(ImportError, __import__, 'testing.notapackage')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testLoadPlugins']
    unittest.main()
