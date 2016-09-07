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

class UndoManager(object):
    """
    This class is the undo redo manager for multiple undo stacks. It is a
    singleton class. 
    
    Don't inherit from this class.
    """
    _instance = None
    _stack = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(UndoManager, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def setCurrentStack(self, stack):
        self._stack = stack

    def currentStack(self):
        return self._stack

    def undo(self):
        self._stack.undo()

    def redo(self):
        self._stack.redo()

