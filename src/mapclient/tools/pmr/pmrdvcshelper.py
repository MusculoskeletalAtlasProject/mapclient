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
import os

from subprocess import Popen, PIPE

from mapclient.core.utils import which


def isHgRepository(location):
    return os.path.exists(os.path.join(location, '.hg'))


def isGitRepository(location):
    return os.path.exists(os.path.join(location, '.git'))


def repositoryIsUpToDate(location):
    result = True
    if isGitRepository(location):
        dvcs_cmd = which('git')
        if len(dvcs_cmd) > 0:
            process = Popen([dvcs_cmd[0], "status", location], stdout=PIPE, stderr=PIPE)
            outputs = process.communicate()
            stdout = outputs[0]
            stderr = outputs[1]
            if len(stdout) > 0 or len(stderr) > 0:
                result = False
        
    return result
