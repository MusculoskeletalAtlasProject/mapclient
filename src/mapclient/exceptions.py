
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
class ClientRuntimeError(RuntimeError):
    """
    Generic error for indicating errors that should be notified to the
    user running the client.
    """

    def __init__(self, title='Error', description=''):
        super(ClientRuntimeError, self).__init__(description)
        self.title = title
        self.description = description

    def __str__(self):
        return '%s: %s' % (self.title, self.description)
