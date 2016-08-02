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

from mayaviviewerobjects import MayaviViewerSceneObject, MayaviViewerObject
import numpy as np

class MayaviViewerFieldworkMeasurementsSceneObject(MayaviViewerSceneObject):

    typeName = 'fieldworkmeasurements'

    def __init__(self, name, sceneObject=None):
        self.name = name
        if sceneObject==None:
        	self.sceneObject = {}
        else:
        	self.sceneObject = sceneObject

    def addSceneObject(self, name, obj):
    	self.sceneObject[name] = obj

    def setVisibility(self, visible):
        for obj in self.sceneObject.values():
        	obj.visible = visible

    def remove(self):
    	for name in self.sceneObject.keys():
    		self.sceneObject[name].remove()
    		del self.sceneObject[name]

# object for femur measurements
class MayaviViewerFemurMeasurements(MayaviViewerObject):

	typeName = 'fieldworkmeasurements'
	textMeasurements = ('head_diameter', 'neck_width', 'neck_shaft_angle', 'femoral_axis_length', 'subtrochanteric_width')
	tubeRadius = 2.0
	textLineRadius = 0.5
	charWidth = 0.015
	textColour = (1,1,1)

	def __init__(self, name, measurements, drawWidthTubes=False, text2d=False):
		self.name = name
		self._M = measurements
		self._drawWidthTubes = drawWidthTubes
		self._text2d = text2d
		self.sceneObject = None

		print 'FEMUR MEASUREMENT INITIALISED'

	def setVisibility(self, visible):
		self.sceneObject.setVisibility(visible)

	def remove(self):

		if self.sceneObject:
			self.sceneObject.remove()
			self.sceneObject = None

		self._M = None

	def draw(self, scene):

		print 'DRAWING MEASUREMENTS'
		self.sceneObject = MayaviViewerFieldworkMeasurementsSceneObject(self.name)

    	# draw axes
		self._drawAxes(scene)		
		# plot head sphere
		self._drawHead(scene)		
		# draw femoral axis length intercepts
		self._drawFemoralAxisLength(scene)			
		# draw neck width and tube
		self._drawNeckWidth(scene)
		# draw neck shaft angle
		self._drawNeckShaftAngle(scene)
		# draw subtrochanteric width
		self._drawSubTrochantericWidth(scene)
		# draw midshaft width and tube
		self._drawMidshaftWidth(scene)
		# draw epicondyle intercepts
		self._drawEpicondyleWidth(scene)		
		# add text of measurements
		if self._text2d:
			self._drawText2D(scene)

	def _drawText2D(self, scene):
		tx = 0.02
		ty = 0.02
		tspacing = 0.05
		for m in self.textMeasurements:
			value = self._M.measurements[m].value
			mString = '{m}: {v:5.0f}'.format(m=m, v=value)
			sObj = scene.mlab.text(tx, ty, mString, width=len(mString)*self.charWidth, name='text2d_'+m, color=self.textColour)
			self.sceneObject.addSceneObject('text2d_'+m, sObj)
			ty += tspacing

	def _addText3D(self, scene, name, value, unit, mOrigin, offset):

		print 'DRAWING 3D TEXT'

		textOrigin = np.array(mOrigin)+np.array(offset)
		textLine = np.array([mOrigin, textOrigin]).T
		mStr = '{}: {:5.0f} {}'.format(name, value, unit)
		texts = scene.mlab.text(textOrigin[0], textOrigin[1], mStr, z=textOrigin[2], width=len(mStr)*self.charWidth, name='text3d_'+name, color=self.textColour)
		self.sceneObject.addSceneObject('text3d_'+name, texts)
		lines = scene.mlab.plot3d(textLine[0], textLine[1], textLine[2], tube_radius=self.textLineRadius, name='text3dline_'+name)
		self.sceneObject.addSceneObject('text3dline_'+name, lines)

	def _drawAxes(self, scene):
		tubeRadius = 2.0
		saPoints = self._M.shaftAxis.eval(np.array([-300,300])).T
		saSObj = scene.mlab.plot3d(saPoints[0], saPoints[1], saPoints[2], name='axis_shaft', tube_radius=self.tubeRadius )
		self.sceneObject.addSceneObject('axis_shaft', saSObj)

		naPoints = self._M.neckAxis.eval(np.array([-100,100])).T
		naSObj = scene.mlab.plot3d(naPoints[0], naPoints[1], naPoints[2], name='axis_neck', tube_radius=self.tubeRadius )
		self.sceneObject.addSceneObject('axis_neck', naSObj)

		ecPoints = self._M.epicondylarAxis.eval(np.array([-100,100])).T
		ecSObj = scene.mlab.plot3d(ecPoints[0], ecPoints[1], ecPoints[2], name='axis_epicondylar', tube_radius=self.tubeRadius )	
		self.sceneObject.addSceneObject('axis_epicondylar', ecSObj)

	def _drawHead(self, scene):
		headM = self._M.measurements['head_diameter']
		C = headM.centre
		headSphere = scene.mlab.points3d( C[0], C[1], C[2], mode='sphere', scale_factor=headM.value, resolution=16, name='glyph_headSphere', color=(0.0,1.0,0.0), opacity=0.3 )
		self.sceneObject.addSceneObject('glyph_headSphere', headSphere)
		self._addText3D(scene, 'head diameter', headM.value, 'mm', C, [70.0,0,250])

	def _drawNeckWidth(self, scene):

		# width
		NW = self._M.measurements['neck_width']
		NWC = NW.centre
		NWSup = NW.interceptSup
		NWInf = NW.interceptInf
		# NWMin = NW.searchMin
		# NWMax = NW.searchMax
		# NWPoints = np.array([NWSup, NWC, NWInf, NWMin, NWMax]).T
		NWPoints = np.array([NWSup, NWInf]).T
		NWPoints = scene.mlab.points3d( NWPoints[0], NWPoints[1], NWPoints[2], name='glyph_neckWidthPoints', mode='sphere', scale_factor=5, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObject.addSceneObject('glyph_neckWidthPoints', NWPoints)

		NWLinePoints = np.array([NWSup, NWInf]).T
		NWLine = scene.mlab.plot3d(NWLinePoints[0], NWLinePoints[1], NWLinePoints[2], name='glyph_neckWidthLine', tube_radius=self.tubeRadius )
		self.sceneObject.addSceneObject('glyph_neckWidthLine', NWLine)

		self._addText3D(scene, 'neck width', NW.value, 'mm', NWInf, [80.0,0.0,-80])

		# tube
		if self._drawWidthTubes:
			neckRadiusM = self._M.measurements['neck_width']
			# neckEnds = M.neckAxis.eval(np.array([-50,10])).T
			# NW = M.measurements['neck_width']
			# neckEnds = np.array([NW.searchMin, NW.searchMax]).T
			neckEnds = self._M.neckAxis.eval(np.array([-30,20])).T
			NWTube = scene.mlab.plot3d(neckEnds[0], neckEnds[1], neckEnds[2], name='glyph_neckWidthTube', tube_radius=neckRadiusM.value/2.0, tube_sides=16, color=(0.0,0.0,1.0), opacity=0.3 )
			self.sceneObject.addSceneObject('glyph_neckWidthTube', NWTube)

	def _drawFemoralAxisLength(self, scene):
		FAL = self._M.measurements['femoral_axis_length']
		H = FAL.headIntercept[1]
		G = FAL.gTrocIntercept[1]
		FALPoints = scene.mlab.points3d( [H[0], G[0]], [H[1], G[1]], [H[2], G[2]], name='glyph_FALPoints', mode='sphere', scale_factor=5, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObject.addSceneObject('glyph_FALPoints', FALPoints)
		self._addText3D(scene, 'femoral axis length', FAL.value, 'mm', G, [-220.0,0.0,220.0])

	def _drawNeckShaftAngle(self, scene):
		
		NSA = self._M.measurements['neck_shaft_angle']
		angleDegrees = NSA.value*180.0/np.pi
		if angleDegrees < 90.0:
			angleDegrees = 180 - angleDegrees
		
		# find closest approach between shaft axis and neck axis
		saPoints = self._M.shaftAxis.eval(np.linspace(0,300,200))
		naPoints = self._M.neckAxis.eval(np.linspace(-100,100,200))

		closestSAPoint = saPoints[np.argmin([self._M.neckAxis.calcDistanceFromPoint(p) for p in saPoints])]
		closestNAPoint = naPoints[np.argmin([self._M.shaftAxis.calcDistanceFromPoint(p) for p in naPoints])]

		# mid point of closest points is where glyph is drawn
		O = (closestNAPoint + closestSAPoint)*0.5
		NSAPoint = scene.mlab.points3d( [O[0]], [O[1]], [O[2]], name='glyph_NSAPoint', mode='sphere', scale_factor=15, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObject.addSceneObject('glyph_NSAPoint', NSAPoint)
		self._addText3D(scene, 'neck shaft angle', angleDegrees, 'degrees', O, [100.0,0.0,-150.0])

	def _drawSubTrochantericWidth(self, scene):
		sTW = self._M.measurements['subtrochanteric_width']
		points = np.array([sTW.p1, sTW.p2]).T
		centre = (sTW.p1+sTW.p2)*0.5
		
		sTWPoints = scene.mlab.points3d( points[0], points[1], points[2], name='glyph_sTWPoints', mode='sphere', scale_factor=5, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObject.addSceneObject('glyph_sTWPoints', sTWPoints)

		sTWLine = scene.mlab.plot3d(points[0], points[1], points[2], name='glyph_sTWLine', tube_radius=self.tubeRadius )
		self.sceneObject.addSceneObject('glyph_sTWLine', sTWLine)

		self._addText3D(scene, 'subtrochanteric width', sTW.value, 'mm', sTW.p1, [100.0,0.0,-160.0])

	def _drawMidshaftWidth(self, scene):
		mSW = self._M.measurements['midshaft_width']
		points = np.array([mSW.p1, mSW.p2]).T
		centre = (mSW.p1+mSW.p2)*0.5
		
		mSWPoints = scene.mlab.points3d( points[0], points[1], points[2], name='glyph_midshaftWidthPoints', mode='sphere', scale_factor=5, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObject.addSceneObject('glyph_midshaftWidthPoints', mSWPoints)

		mSWLine = scene.mlab.plot3d(points[0], points[1], points[2], name='glyph_midshaftWidthLine', tube_radius=self.tubeRadius )
		self.sceneObject.addSceneObject('glyph_midshaftWidthLine', mSWLine)

		self._addText3D(scene, 'midshaft width', mSW.value, 'mm', mSW.p1, [100.0,0.0,-140.0])

		# draw midshaft tube
		if self._drawWidthTubes:
			midshaftEnds = self._M.shaftAxis.eval(np.array([-20,20])).T
			mSWTube = scene.mlab.plot3d(midshaftEnds[0], midshaftEnds[1], midshaftEnds[2], name='glyph_midshaftWidthTube', tube_radius=mSW.value/2.0, tube_sides=16, color=(0.0,0.0,1.0), opacity=0.3 )
			self.sceneObject.addSceneObject('glyph_midshaftWidthTube', mSWTube)

	def _drawEpicondyleWidth(self, scene):
		ECW = self._M.measurements['epicondylar_width']
		# l = EP[ ECW.p1[0] ]
		l = ECW.p1[1]
		# m = EP[ ECW.p2[0] ]
		m = ECW.p2[1]
		c = (l+m)*0.5
		ECWPoints = scene.mlab.points3d( [l[0], m[0]], [l[1], m[1]], [l[2], m[2]], name='glyph_epicondylarWidthPoints', mode='sphere', scale_factor=5, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObject.addSceneObject('glyph_epicondylarWidthPoints', ECWPoints)
		self._addText3D(scene, 'epicondylar width', ECW.value, 'mm', m, [70.0,0.0,-70.0])