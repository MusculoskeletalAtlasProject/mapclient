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

import json
import logging
import os.path

from requests import HTTPError
from requests import Session
from requests_oauthlib import OAuth1Session

from pmr2.wfctrl.core import get_cmd_by_name
from pmr2.wfctrl.core import CmdWorkspace

# This ensures the get_cmd_by_name will work, as any classes that needs
# to be registered has to be imported first, usually at the module level.
import pmr2.wfctrl.cmd

from mapclient.exceptions import ClientRuntimeError

logger = logging.getLogger(__name__)

ontological_search_string = 'Ontological term'
plain_text_search_string = 'Plain text'
workflow_search_string = 'Workflow'
search_domains = [ontological_search_string, plain_text_search_string, workflow_search_string]

endpoints = {
    '': {
        'dashboard': 'pmr2-dashboard',
        'search': 'search',
        'ricordo': 'pmr2_ricordo/query',
        'map': 'map_query',
    },

    'WorkspaceContainer': {
        'add-workspace': '+/addWorkspace',
    },

    'Workspace': {
        'temppass': 'request_temporary_password',
    },

}


def make_form_request(action_=None, **kw):
    return json.dumps({
        'fields': kw,
        'actions': {action_: 1},
    })


class PMRToolError(ClientRuntimeError):
    pass


class JSONDecodeError(ValueError):
    """Subclass of ValueError with the following additional properties:

    msg: The unformatted error message
    doc: The JSON document being parsed
    pos: The start index of doc where parsing failed
    end: The end index of doc where parsing failed (may be None)
    lineno: The line corresponding to pos
    colno: The column corresponding to pos
    endlineno: The line corresponding to end (may be None)
    endcolno: The column corresponding to end (may be None)

    """
    # Note that this exception is used from _speedups
    def __init__(self, msg, doc, pos, end=None):
        ValueError.__init__(self, errmsg(msg, doc, pos, end=end))
        self.msg = msg
        self.doc = doc
        self.pos = pos
        self.end = end
        self.lineno, self.colno = linecol(doc, pos)
        if end is not None:
            self.endlineno, self.endcolno = linecol(doc, end)
        else:
            self.endlineno, self.endcolno = None, None


def linecol(doc, pos):
    lineno = doc.count('\n', 0, pos) + 1
    if lineno == 1:
        colno = pos + 1
    else:
        colno = pos - doc.rindex('\n', 0, pos)
    return lineno, colno


def errmsg(msg, doc, pos, end=None):
    lineno, colno = linecol(doc, pos)
    msg = msg.replace('%r', repr(doc[pos:pos + 1]))
    if end is None:
        fmt = '%s: line %d column %d (char %d)'
        return fmt % (msg, lineno, colno, pos)
    endlineno, endcolno = linecol(doc, end)
    fmt = '%s: line %d column %d - line %d column %d (char %d - %d)'
    return fmt % (msg, lineno, colno, endlineno, endcolno, pos, end)


class PMRTool(object):

    PROTOCOL = 'application/vnd.physiome.pmr2.json.0'
    UA = 'pmr.jsonclient.Client/0.2'

    def __init__(self, pmr_info=None, use_external_git=False):
        self._termLookUpLimit = 32
        self.set_info(pmr_info)
        self.set_use_external_git(use_external_git)

    def set_info(self, info):
        self._pmr_info = info

    def set_use_external_git(self, use_external_git):
        self._git_implementation = 'git' if use_external_git else 'dulwich'

    def make_session(self):

        if self.hasAccess():
            kwargs = self._pmr_info.get_session_kwargs()
            session = OAuth1Session(**kwargs)
        else:
            # normal session without OAuth requirements.
            session = Session()

        session.headers.update({
            'Accept': self.PROTOCOL,
            'Content-Type': self.PROTOCOL,
            'User-Agent': self.UA,
        })
        return session

    def hasAccess(self):
        return self._pmr_info.has_access()

    def isActive(self):
        return True if self._pmr_info.activeHost() else False

    def deregister(self):
        self._pmr_info.update_token(None, None)

    # also workaround the resigning redirections by manually resolving
    # redirects while using allow_redirects=False when making all requests

    def _search(self, text, search_type):
        session = self.make_session()

        if search_type == ontological_search_string:
            r = session.post('/'.join((self._pmr_info.host(), endpoints['']['ricordo'])),
                data=make_form_request('search',
                    simple_query=text,
                ),
                allow_redirects=False)
        elif search_type == workflow_search_string:
            r = session.post('/'.join((self._pmr_info.host(), endpoints['']['map'])),
                data=make_form_request('search',
                    workflow_object='Workflow Project',
                    ontological_term=text
                ),
                allow_redirects=False)
        else:
            data = json.dumps({'SearchableText': text, 'portal_type': 'Workspace'})
            r = session.post(
                '/'.join((self._pmr_info.host(), endpoints['']['search'])),
                data=data,
            )
        r.raise_for_status()
        print(r.json())
        return r.json()

    def search(self, text, search_type=plain_text_search_string):
        """
        Search PMR for the given text, the search type
        can be either 'plain' for plain text searching or
        'ontological' for ricordo knowledge base searching.
        """
        try:
            return self._search(text, search_type)
        except HTTPError as e:
            msg_403 = 'The configured PMR server may have disallowed searching.'
            if self.hasAccess():
                msg_403 = (
                    'Access credentials are no longer valid.  Please '
                    'deregister and register the application to renew access '
                    'and try again.'
                )
            if e.response.status_code == 403:
                raise PMRToolError('Permission Error', msg_403)
            else:
                raise PMRToolError('Web Service Error',
                    'The PMR search service may be misconfigured and/or '
                    'is unavailable at this moment.  Please check '
                    'configuration settings and try again.'
                )
        except JSONDecodeError:
            raise PMRToolError('Unexpected Server Response',
                'The server returned an unexpected response and MAP Client is '
                'unable to proceed.'
            )
        except Exception as e:
            raise PMRToolError('Unexpected exception', str(e))

    def _getObjectInfo(self, target_url):
        session = self.make_session()
        r = session.get(target_url)
        r.raise_for_status()
        return r.json()

    def getObjectInfo(self, target_url):
        try:
            return self._getObjectInfo(target_url)
        except HTTPError as e:
            raise PMRToolError('Remote server error',
                'Server responded with an error message and MAP Client is '
                'unable to continue the action.')
        except JSONDecodeError:
            raise PMRToolError('Unexpected Server Response',
                'The server returned an unexpected response that MAP Client '
                'cannot process.')
        except Exception as e:
            raise PMRToolError('Unexpected exception', str(e))

    def requestTemporaryPassword(self, workspace_url):
        if not self.hasAccess():
            return None

        session = self.make_session()
        r = session.post(
            '/'.join((workspace_url, endpoints['Workspace']['temppass'])),
            data='{}',
        )
        r.raise_for_status()
        return r.json()

    def authorizationUrl(self, key):
        return self._client.authorizationUrl(key)

    def getDashboard(self):
        session = self.make_session()
        target = '/'.join([self._pmr_info.host(), endpoints['']['dashboard']])
        r = session.get(target)
        r.raise_for_status()
        return r.json()

    def isValidHost(self, host):
        session = Session()

        session.headers.update({
            'Accept': self.PROTOCOL,
            'Content-Type': self.PROTOCOL,
            'User-Agent': self.UA,
        })

        target = '/'.join([host, endpoints['']['dashboard']])
        r = session.get(target)
        r.raise_for_status()
        json_response = r.json()
        return 'workspace-home' in json_response and 'workspace-add' in json_response

    def addWorkspace(self, title, description, storage='git'):
        session = self.make_session()

        dashboard = self.getDashboard()
        option = dashboard.get('workspace-add', {})
        target = option.get('target')

        if target is None:
            # XXX exception?
            return

        # XXX until requests and requests_oauthlib work together to
        # provide a fix for the redirection and OAuth signature
        # regeneration, we have to handle all redirects manually.
        r = session.get(target, allow_redirects=False)
        target = r.headers.get('Location')

        # the real form get
        # XXX I need to get PMR to generate IDs if the autoinc isn't
        # enabled.
        # XXX should verify the contents of the fields.
        # r = session.get(target, allow_redirects=False)

        # For now, just post
        r = session.post(target,
            data=make_form_request('add',
                title=title,
                description=description,
                storage=storage,
            ),
            allow_redirects=False)

        workspace_target = r.headers.get('Location')
        # verify that this is an actual workspace by getting it.
        r = session.get(workspace_target)
        return r.json().get('url')

    def cloneWorkspace(self, remote_workspace_url, local_workspace_dir):
        # XXX target_dir is assumed to exist, so we can't just clone
        # but we have to instantiate that as a new repo, define the
        # remote and pull.

        # link
        self.linkWorkspaceDirToUrl(
            local_workspace_dir=local_workspace_dir,
            remote_workspace_url=remote_workspace_url,
        )

        workspace = CmdWorkspace(local_workspace_dir, get_cmd_by_name(self._git_implementation))

        # Another caveat: that workspace is possibly private.  Acquire
        # temporary password.
        creds = self.requestTemporaryPassword(remote_workspace_url)
        if creds:
            result = workspace.cmd.pull(workspace,
                username=creds['user'], password=creds['key'])
        else:
            # no credentials
            logger.info('not using credentials as none are detected')
            result = workspace.cmd.pull(workspace)

        # TODO trap this result too?
        workspace.cmd.reset_to_remote(workspace)
        return result

    def addFileToIndexer(self, local_workspace_dir, workspace_file):
        """
        Add the given workspace file in the remote workspace to the
        indexer for ontological searching.
        """
        if not self.hasAccess():
            return

        workspace = CmdWorkspace(local_workspace_dir, get_cmd_by_name(self._git_implementation))
        cmd = workspace.cmd
        remote_workspace_url = cmd.read_remote(workspace)
        target = '/'.join([remote_workspace_url, 'rdf_indexer'])
#         {u'fields': {u'paths': {u'items': None, u'error': None, u'description': u'Paths that will be indexed as RDF.', u'value': u'', u'klass': u'textarea-widget list-field'}}, u'actions': {u'apply': {u'title': u'Apply'}, u'export_rdf': {u'title': u'Apply Changes and Export To RDF Store'}}}
        session = self.make_session()
        r = session.post(target,
            data=make_form_request('export_rdf',
                paths=[workspace_file],
            ),
            allow_redirects=False)

        r.raise_for_status()
        return r.json()

    def linkWorkspaceDirToUrl(self, local_workspace_dir, remote_workspace_url):
        # links a non-pmr workspace dir to a remote workspace url.
        # prereq is that the remote must be new.

        workspace_obj = self.getObjectInfo(remote_workspace_url)
        cmd_cls = get_cmd_by_name(self._git_implementation)
        if cmd_cls is None:
            raise PMRToolError('Remote storage format unsupported',
                'The remote storage `%(storage)s` is not one of the ones that '
                'the MAP Client currently supports.' % workspace_obj)

        # brand new command module for init.
        new_cmd = cmd_cls()
        workspace = CmdWorkspace(local_workspace_dir, new_cmd)

        # Add the remote using a new command
        cmd = cmd_cls(remote=remote_workspace_url)

        # Do the writing.
        cmd.write_remote(workspace)

    def hasDVCS(self, local_workspace_dir):
        git_dir = os.path.join(local_workspace_dir, '.git')
        if os.path.isdir(git_dir):
            bob = get_cmd_by_name(self._git_implementation)
            workspace = CmdWorkspace(local_workspace_dir, bob)
            return workspace.cmd is not None
        else:
            return False


    def commitFiles(self, local_workspace_dir, message, files):
        workspace = CmdWorkspace(local_workspace_dir, get_cmd_by_name(self._git_implementation))
        cmd = workspace.cmd
        if cmd is None:
            logger.info('skipping commit, no underlying repo detected')
            return

        logger.info('Using `%s` for committing files.', cmd.__class__.__name__)

        for fn in files:
            sout, serr = cmd.add(workspace, fn)
            # if serr has something we need to handle?

        # XXX committer will be a problem if unset in git.
        return cmd.commit(workspace, message)

    def pushToRemote(self, local_workspace_dir, remote_workspace_url=None):
        workspace = CmdWorkspace(local_workspace_dir, get_cmd_by_name(self._git_implementation))
        cmd = workspace.cmd

        if remote_workspace_url is None:
            remote_workspace_url = cmd.read_remote(workspace)
        # Acquire temporary creds
        creds = self.requestTemporaryPassword(remote_workspace_url)

        stdout, stderr = cmd.push(workspace,
            username=creds['user'], password=creds['key'])

        if stdout:
            logger.info(stdout)
        if stderr:
            logger.error(stderr)
#             raise PMRToolError('Error pushing changes to PMR',
#                 'The command line tool gave us this error message:\n\n' +
#                     stderr)

        return stdout, stderr

    def pullFromRemote(self, local_workspace_dir):
        workspace = CmdWorkspace(local_workspace_dir, get_cmd_by_name(self._git_implementation))
        cmd = workspace.cmd

        remote_workspace_url = cmd.read_remote(workspace)
        creds = self.requestTemporaryPassword(remote_workspace_url)
        stdout, stderr = cmd.pull(workspace,
            username=creds['user'], password=creds['key'])

        if stdout:
            logger.info(stdout)
        if stderr:
            logger.info(stderr)

        return stdout, stderr

