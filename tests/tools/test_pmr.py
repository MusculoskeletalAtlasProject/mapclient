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
import sys

if sys.version_info < (2, 7):
    try:
        from unittest2 import TestCase, main, skipUnless
    except ImportError:
        print('Go install unittest2 in python2.6, all tests are skipped.')
        main = TestCase = object
        def skipUnless(cond, reason):
            def decorator(obj):
                return obj
            return decorator
else:
    from unittest import TestCase, main, skipUnless


REQUESTS_TESTADAPTER = True
try:
    from requests_testadapter import TestAdapter, TestSession
except:
    print('Missing `requests_testadapter`; all requests tests are skipped')
    REQUESTS_TESTADAPTER = False

import json
import tempfile
import os
import shutil

from requests import HTTPError
from requests import Session
from requests_oauthlib import OAuth1Session
from PySide.QtCore import QSettings

from mapclient.tools.pmr.pmrtool import PMRTool
from mapclient.tools.pmr.pmrtool import PMRToolError
from mapclient.tools.pmr.settings.general import PMR

workspace_home = json.dumps({
    u'workspace-home': {
        u'target': u'http://example.com/dashboard/home',
        u'label': u'Workspace home'
    },
    u'workspace-add': {
        u'target': u'http://example.com/dashboard/addWorkspace',
        u'label': u'Create workspace in workspace home',
    },
})


@skipUnless(REQUESTS_TESTADAPTER, 'No need to create workspaces all the time.')
class PMRToolTestCase(TestCase):

    test_level = 1

    def setUp(self):
        self.working_dir = tempfile.mkdtemp()

        # Because uh, QSettings has very nice API so we need this
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)

        # and this line, which include
        QSettings.setPath(
            QSettings.Format.IniFormat,  # this arg
            QSettings.Scope.SystemScope,
            self.working_dir,
        )

        # to have our test settings isolated from the real application.
        # Insert profanity here: ________________

        # now we make our info
        info = PMR()

        self.endpoints = [
            (info.host() + '/pmr2-dashboard',
                TestAdapter(stream=workspace_home)),

            ('http://example.com/dashboard/addworkspace',
                TestAdapter(
                    stream='',
                    headers={
                        'Location': 'http://example.com/w/+/addworkspace',
                    }
                )
            ),

            ('http://example.com/w/+/addworkspace',
                TestAdapter(
                    # XXX need to make this a real thing when we test that
                    # responses from server matters.
                    stream='',
                    headers={
                        'Location': 'http://example.com/w/1',
                    }
                )
            ),

            ('http://example.com/hgrepo',
                TestAdapter(
                    # XXX need to make this a real thing when we test that
                    # responses from server matters.
                    stream='{"url": "http://example.com/hgrepo", '
                        '"storage": "git"}',
                )
            ),

            ('http://example.com/w/1',
                TestAdapter(
                    # XXX need to make this a real thing when we test that
                    # responses from server matters.
                    stream='{"url": "http://example.com/w/1", '
                        '"storage": "git"}',
                )
            ),

            ('http://example.com/w/1/request_temporary_password',
                TestAdapter(
                    stream='{"user": "tester", "key": "secret"}',
                )
            ),

            (info.host() + '/search',
                TestAdapter(
                    stream='[{"title": "Test Workspace", '
                           '"target": "http://example.com/w/1"}]',
                )
            ),

        ]

        # and tool, with the end points.
        self._tool = self.make_tool()

    def tearDown(self):
        shutil.rmtree(self.working_dir)

    def make_tool(self, endpoints=None):
        if endpoints is None:
            endpoints = self.endpoints

        def make_session(pmr_info=None):
            session = TestSession()
            for url, adapter in endpoints:
                session.mount(url, adapter)
            return session
        
        pmr_info = PMR()
        tool = PMRTool(pmr_info)
        tool.make_session = make_session
        return tool

    def test_make_session_no_access(self):
        pmr_info = PMR()
        tool = PMRTool(pmr_info)
        session = tool.make_session()
        self.assertFalse(isinstance(session, OAuth1Session))
        # Make sure this really is a requests.Session
        self.assertTrue(isinstance(session, Session))

    def test_make_session_with_access(self):
        pmr_info = PMR()
        tool = PMRTool(pmr_info)
        info = PMR()
        info.update_token('test', 'token')
        session = tool.make_session()
        self.assertTrue(isinstance(session, OAuth1Session))
        info.update_token('', '')

    def test_hasDVCS(self):
        # this is actually a wrapper around the pmr.wfctrl workspace
        # auto detection
        self.assertFalse(self._tool.hasDVCS(self.working_dir))

    def testAddWorkspace(self):
#         info = PMR()
        location = self._tool.addWorkspace('my title', 'my description')
        self.assertTrue(location.startswith('http://'))

    def testGetDashboard(self):
#         info = PMR()
        d = self._tool.getDashboard()
        self.assertTrue('workspace-home' in d)
        self.assertTrue('workspace-add' in d)

    def test_requestTemporaryPassword(self):
        # Available with access
        info = PMR()
        info.update_token('test', 'token')

        result = self._tool.requestTemporaryPassword('http://example.com/w/1')
        self.assertEqual(result['user'], 'tester')
        self.assertEqual(result['key'], 'secret')

        info.update_token('', '')
        result = self._tool.requestTemporaryPassword('http://example.com/w/1')
        self.assertTrue(result is None)

    def test_linkWorkspaceDirToUrl_hg_success(self):
        self._tool.linkWorkspaceDirToUrl(
            self.working_dir, 'http://example.com/hgrepo')
        with open(os.path.join(self.working_dir, '.hg', 'hgrc')) as fd:
            self.assertTrue('default = http://example.com/hgrepo' in fd.read())

    def test_search_success(self):
        results = self._tool.search('')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Test Workspace')

    def test_search_failure(self):
        info = PMR()
        tool = self.make_tool(endpoints=[
            (info.host() + '/search',
                TestAdapter(stream='Invalid', status=403)
            ),
        ])
        # the private method exposes exceptions
        self.assertRaises(HTTPError, tool._search, '')
        # the real method traps all exceptions
        self.assertRaises(PMRToolError, tool.search, '')

    def test_cloneWorkspace(self):
        # We have tested the password retrival works.

        # In pmr.wfctrl the pull is tested to work.

        # Network test should be done, but that's really ensuring the
        # correct values are instantiated to be sent as arguments to the
        # binary call.

        # Ideally we should be able to replace the command call with a
        # mock.
        pass

    def test_hasAccess(self):
        # update tokens using another instance
        info = PMR()
        t = PMRTool(info)

        # Fresh token should have no access
        self.assertFalse(t.hasAccess())

        info.update_token('test', 'token')
        # Now it's true
        self.assertTrue(t.hasAccess())

        # revoke access again.
        info.update_token('', '')
        # Now it's false again.
        self.assertFalse(t.hasAccess())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    main()
