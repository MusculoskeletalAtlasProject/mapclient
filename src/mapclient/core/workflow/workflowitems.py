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
import uuid

from PySide6 import QtCore


class Item(object):

    def __init__(self):
        self._selected = True

    def getSelected(self):
        return self._selected

    def setSelected(self, selected):
        self._selected = selected


class MetaStep(Item):
    Type = 'Step'

    def __init__(self, step):
        Item.__init__(self)
        self._step = step
        self._pos = QtCore.QPointF(10, 10)
        self._uid = str(uuid.uuid1())
        self._id = step.getIdentifier()

    def getPos(self):
        return self._pos

    def setPos(self, pos):
        self._pos = pos

    def getStep(self):
        return self._step

    def getName(self):
        return self._step.getName()

    def getIdentifier(self):
        if self._id:
            return self._id
        return self._uid

    def setIdentifier(self, identifier):
        self._step.setIdentifier(identifier)
        self._id = identifier

    def getStepIdentifier(self):
        identifier = self._step.getIdentifier()
        if identifier:
            return identifier
        return self._uid

    def hasIdentifierChanged(self):
        return not (self.getIdentifier() == self.getStepIdentifier())

    def syncIdentifier(self):
        self._id = self._step.getIdentifier()

    def getUniqueIdentifier(self):
        return self._uid

    def setUniqueIdentifier(self, uniqueIdentifier):
        # Awesome QSettings appears to be changing my string into a
        # uuid.UUID class
        if type(uniqueIdentifier) == uuid.UUID:
            self._uid = str(uniqueIdentifier)
        else:
            self._uid = uniqueIdentifier


class Connection(Item):
    Type = 'Connection'

    def __init__(self, source, source_index, destination, destination_index):
        Item.__init__(self)
        self._source = source
        self._sourceIndex = source_index
        self._destination = destination
        self._destinationIndex = destination_index

    def source(self):
        return self._source

    def sourceIndex(self):
        return self._sourceIndex

    def destination(self):
        return self._destination

    def destinationIndex(self):
        return self._destinationIndex
