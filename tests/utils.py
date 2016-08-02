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

import re, sys


class ConsumeOutput(object):
    def __init__(self):
        self.messages = list()

    def write(self, message):
        self.messages.append(message)

    def flush(self):
        pass


def parseUnitTestOutput(filename):
    """
    Function for parsing unittest output for gathering pass and fail counts.
    """
    f = open(filename)
    lines = f.readlines()

    rc = 1
    passed = 0
    failed = 0
    lines.reverse()
    while len(lines) >= 3:
        statusLine = lines[0].rstrip('\r\n')
        totalLine = lines[2].rstrip('\r\n')

        m = re.match('Ran (\d+)', totalLine)
        if m:
            lines = []
            total = int(m.group(1))
            if statusLine.startswith('OK'):
                passed = total
                if total > 0:
                    rc = 0
            else:
                errorDesc = ['failures', 'errors']
                for errorType in errorDesc:
                    m = re.match('.*{0}=(\d+)'.format(errorType), statusLine)
                    if m:
                        failed += int(m.group(1))

                passed = total - failed
        else:
            del lines[0]

    return rc, passed, failed


def createTestApplication():
    from PySide import QtCore, QtGui

    from mapclient.settings.info import ORGANISATION_DOMAIN, ORGANISATION_NAME, APPLICATION_NAME, ABOUT

    test_app = QtGui.QApplication.instance()
    if test_app is None:
        test_app = QtGui.QApplication(sys.argv)

    def setApplicationsSettings(app):

        app.setOrganizationDomain(ORGANISATION_DOMAIN)
        app.setOrganizationName(ORGANISATION_NAME)
        app.setApplicationName(APPLICATION_NAME + '-TEST')
        app.setApplicationVersion(ABOUT['version'])
        QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)

    setApplicationsSettings(test_app)

    return test_app

