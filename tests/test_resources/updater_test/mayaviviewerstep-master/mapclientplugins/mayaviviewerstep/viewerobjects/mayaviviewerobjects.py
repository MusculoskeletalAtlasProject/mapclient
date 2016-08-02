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
os.environ['ETS_TOOLKIT'] = 'qt4'

colours = {'bone':(0.84705882, 0.8, 0.49803922)}

class MayaviViewerObject(object):

    def __init__(self):
        pass

    def draw(self, scene):
        pass

    def setScalarSelection(self, scalarName):
        self.scalarName = scalarName

    def setVisibility(self, visible):
        pass

    def updateGeometry(self, params):
        pass

    def updateScalar(self, scalarName):
        pass

    def remove(self):
        pass


class MayaviViewerSceneObject(object):

    def __init__(self):
        pass

class MayaviViewerObjectsContainer(object):
    """
    stores objects to be rendered in the viewer
    """
    def __init__(self):
        self._objects = {}

    def addObject(self, name, obj):
        # if name in self._objects.keys():
        #     raise ValueError, 'name must be unique'

        if not isinstance(obj, MayaviViewerObject):
            raise TypeError, 'obj must a MayaviViewerObject'

        self._objects[name] = obj

    def getObjectAll(self, name):
        return self._objects[name]

    def getObjectType(self, name):
        return self._objects[name].typeName

    def getObject(self, name):
        return self._objects[name]

    def getObjectNamesOfType(self, typeName):
        ret = []
        for name, o in self._objects.items():
            if o.typeName==t:
                ret.append(name)

        return ret

    def getObjectNames(self):
        return self._objects.keys()

    def getNumberOfObjects(self):
        return len(self._objects.keys())
