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

from mayaviviewerobjects import MayaviViewerSceneObject, MayaviViewerObject, colours
import numpy as np
from mayavi import mlab

class MayaviViewerGiasScanSceneObject(MayaviViewerSceneObject):

    typeName = 'giasscan'

    def __init__(self, name, slicerWidget, ISrc):
        self.name = name
        self.slicerWidget = slicerWidget
        self.ISrc = ISrc

    def setVisibility(self, visible):
        if self.slicerWidget:
            self.slicerWidget.visible = visible

    def remove(self):
        if self.slicerWidget:
            self.slicerWidget.remove()
            self.slicerWidget = None

        if self.ISrc:
            self.ISrc.remove()
            self.ISrc = None

class MayaviViewerGiasScan(MayaviViewerObject):

    typeName = 'giasscan'
    _vmax = 1800
    _vmin = -200
    _colourMap = 'black-white'
    _slicePlane = 'y_axes'

    def __init__(self, name, scan, renderArgs=None):
        self.name = name
        self.scan = scan
        self.sceneObject = None

        if renderArgs==None:
            self.renderArgs = {'vmin':self._vmin, 'vmax':self._vmax}
        else:
            self.renderArgs = renderArgs
            if 'vmax' not in self.renderArgs.keys():
                self.renderArgs['vmax'] = self._vmax
            if 'vmin' not in self.renderArgs.keys():
                self.renderArgs['vmin'] = self._vmin
            if 'colormap' not in self.renderArgs.keys():
                self.renderArgs['colormap'] = self._colourMap

    def setScalarSelection(self, fieldName):
        pass

    def setVisibility(self, visible):
        self.sceneObject.setVisibility(visible)

    def remove(self):
        self.sceneObject.remove()
        self.sceneObject = None
        self.scan = None

    def draw(self, scene):
        scene.disable_render = True
        
        try:
            I = self.scan.I
        except AttributeError:
            print 'scan is None:', self.name

        ISrc = mlab.pipeline.scalar_field(I, colormap=self.renderArgs['colormap'])
        slicerWidget = scene.mlab.pipeline.image_plane_widget(ISrc,
                                                            plane_orientation=self._slicePlane,
                                                            slice_index=0,
                                                            **self.renderArgs
                                                            )
        mlab.outline()
        self.sceneObject = MayaviViewerGiasScanSceneObject(self.name, slicerWidget, ISrc)
        scene.disable_render = False

        return self.sceneObject

    def changeSlicePlane(self, plane):
        self.sceneObject.slicerWidget.widgets[0].set(plane_orientation=plane)
        self._slicePlane = plane