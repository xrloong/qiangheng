#!/usr/bin/env python3
# coding=utf8

from optparse import OptionParser
import re

try:
	import xie
except ImportError:
	print("Please install the libary Xie (https://github.com/xrloong/Xie.git) first")
	import sys
	sys.exit()
try:
	import wx
except ImportError:
	print("Please install the libary wxPython")
	import sys
	sys.exit()

from xie.graphics.utils import TextCodec
from xie.graphics.stroke import StrokeGroup
from xie.graphics.stroke import Character
from xie.graphics.factory import ShapeFactory
from xie.graphics.canvas import CanvasController

class GlyphManager:
	def __init__(self):
		self.characterDB={}
		self.strokeCount={}
		self.textCodec=TextCodec()
		self.shapeFactory=ShapeFactory()

	def loadFont(self, fontfile):
		for line in open(fontfile).readlines():
			line=line.strip()
			if (not line) or line[0]=='#':
				continue
			else:
				ll=line.split('\t')

				if len(ll)>=2:
					charName=ll[0]
					description=ll[1]
					character=self.computeCharacterByDescription(charName, description)
					character.description=description
					self.characterDB[charName]=character

	def getCharacter(self, strIndex):
		return self.characterDB.get(strIndex, "")

	def getCharacters(self):
		return self.characterDB.keys()

	def computeCharacterByDescription(self, charName, description):
		strokes=self.computeStrokesByDescription(description)
		strokeGroup=self.shapeFactory.generateStrokeGroupByStrokeList(strokes)
		return Character(charName, strokeGroup)

	def computeStrokesByDescription(self, description):
		strokeDescriptionList=self.textCodec.decodeCharacterExpression(description)
		strokes=[]
		for strokeDescription in strokeDescriptionList:
			stroke=self.computeStrokeByDescription(strokeDescription)
			strokes.append(stroke)
		return strokes

	def computeStrokeByDescription(self, strokeDescription):
		textCodec=self.textCodec
		def_list=textCodec.decodeStrokeExpression(strokeDescription)

		assert len(def_list) >= 2
		assert textCodec.isStartPoint(def_list[0])
		assert textCodec.isEndPoint(def_list[-1])

		d=def_list[0]
		point=textCodec.decodePointExpression(d)
		startPoint=point
		lastPoint=point
		segments=[]
		point_list=[point]

		from xie.graphics.segment import SegmentFactory
		from xie.graphics.segment import StrokePath
		from xie.graphics.stroke import Stroke
		from xie.graphics.stroke_info import StrokeInfo
		segmentFactory = SegmentFactory()

		is_curve=False
		for d in def_list[1:]:
			point=textCodec.decodePointExpression(d)
			if textCodec.isEndPoint(d):
				tmpLastPoint=point
				point=[point[0]-lastPoint[0], point[1]-lastPoint[1]]
				point_list.append(point)
				if is_curve:
					segment=segmentFactory.generateSegment_QCurve(point_list[-2], point_list[-1])
				else:
					segment=segmentFactory.generateSegment_Beeline(point_list[-1])
				lastPoint=tmpLastPoint
				segments.append(segment)
				is_curve=False
			elif textCodec.isControlPoint(d):
				point=[point[0]-lastPoint[0], point[1]-lastPoint[1]]
				point_list.append(point)
				is_curve=True

		strokeName=""
		strokePath=StrokePath(segments)
		strokeInfo=StrokeInfo(strokeName, strokePath)
		stroke=Stroke(startPoint, strokeInfo)
		return stroke

class WxCanvasController(CanvasController):
	def __init__(self, canvas, width, height):
		super().__init__(width, height)

		self.canvas = canvas
		self.clear()
		self.point_list = []
		self.lastp = None

		self.pathOptions = {"LineWidth": 20, "LineColor": "Black"}

	def clear(self):
		self.canvas.ClearAll()
		self.canvas.ZoomToBB()

	def moveTo(self, p):
		self.setLastPoint(p)

	def lineTo(self, p):
		points = (self.lastp, p)
		self.canvas.AddLine(points, **self.pathOptions)
		self.canvas.ZoomToBB()

		self.setLastPoint(p)

	def qCurveTo(self, cp, p):
		points = (self.lastp, cp, p)
		self.canvas.AddSpline(points, **self.pathOptions)
		self.canvas.ZoomToBB()

		self.setLastPoint(p)

	def setLastPoint(self, p):
		self.lastp=p


class ShowHanziWidget():
	def __init__(self):
		self.canvasWidth=512
		self.canvasHeight=512

		self.root = wx.App(False)

		sizer = wx.GridBagSizer(3, 1)

		frame = wx.Frame(None, title='秀漢字程式', size=(520, 800))
		frame.SetBackgroundColour("gray")
		frame.SetAutoLayout(True)
		frame.SetSizer(sizer)

		charSBox = wx.StaticBox(frame, label='字符')
		charSBoxSizer = wx.StaticBoxSizer(charSBox, wx.HORIZONTAL)

		tcInputChar = wx.TextCtrl(frame)
		tcInputChar.SetEditable(True)
		charSBoxSizer.Add(tcInputChar, proportion=1, flag=wx.ALIGN_TOP)

		charSBoxSizer.AddSpacer(10)

		vBoxSizer = wx.BoxSizer(wx.VERTICAL)
		btnInputCharOK = wx.Button(frame, label='載入')
		btnInputCharOK.Bind(wx.EVT_BUTTON, self.onInputCharOkClicked)
		vBoxSizer.Add(btnInputCharOK)

		btnInputCharClear = wx.Button(frame, label='清除')
		btnInputCharClear.Bind(wx.EVT_BUTTON, self.onInputCharClearClicked)
		vBoxSizer.Add(btnInputCharClear)
		charSBoxSizer.Add(vBoxSizer)

		sizer.Add(charSBoxSizer, pos=(0, 0), border=5, flag=wx.EXPAND|wx.ALL)



		glyphSBox = wx.StaticBox(frame, label='字形描述')
		glyphSBoxSizer = wx.StaticBoxSizer(glyphSBox, wx.HORIZONTAL)

		tcInputGlyph = wx.TextCtrl(frame)
		tcInputGlyph.SetEditable(True)
		glyphSBoxSizer.Add(tcInputGlyph, proportion=1, flag=wx.EXPAND)

		glyphSBoxSizer.Add((10, 100))

		vBoxSizer = wx.BoxSizer(wx.VERTICAL)
		btnInputGlyphOk = wx.Button(frame, label='確定')
		btnInputGlyphOk.Bind(wx.EVT_BUTTON, self.onInputGlyphOkClicked)
		vBoxSizer.Add(btnInputGlyphOk)

		btnInputGlyphClear = wx.Button(frame, label='清除')
		btnInputGlyphClear.Bind(wx.EVT_BUTTON, self.onInputGlyphClearClicked)
		vBoxSizer.Add(btnInputGlyphClear)
		glyphSBoxSizer.Add(vBoxSizer)

		sizer.Add(glyphSBoxSizer, pos=(1, 0), border=5, flag=wx.EXPAND|wx.ALL)


		self.tcInputChar = tcInputChar
		self.tcInputGlyph = tcInputGlyph

		from wx.lib.floatcanvas import FloatCanvas
		self.canvas = FloatCanvas.FloatCanvas(frame,
				ProjectionFun = lambda x: (1, -1),
				size = (self.canvasWidth, self.canvasHeight))
		canvasLayoutFlag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER
		sizer.Add(self.canvas, pos=(2, 0), flag=canvasLayoutFlag)
		sizer.AddGrowableRow(2)

		frame.Show()

		canvasController = WxCanvasController(self.canvas, self.canvasWidth, self.canvasHeight)
		from xie.graphics.drawing import DrawingSystem
		self.dh = DrawingSystem(canvasController)

		self.drawFrame()

		fontfile=options.fontfile
		glyphManager.loadFont(fontfile)

	def mainloop(self):
		self.root.MainLoop()

	def onInputCharOkClicked(self, event):
		ch=self.tcInputChar.GetValue()
		character=glyphManager.getCharacter(ch)
		self.tcInputGlyph.SetValue(character.description)

		from xie.graphics.shape import Boundary
		descriptionBoundary = Boundary(0, 0, 256, 256)

		self.drawFrame()

		self.dh.save()
		self.dh.setSourceBoundary(descriptionBoundary)
		self.dh.draw(character)
		self.dh.restore()

	def onInputCharClearClicked(self, event):
		self.clearChar()

	def onInputGlyphClearClicked(self, event):
		self.clearGlyph()

	def onInputGlyphOkClicked(self, event):
		self.byKnownChar()

	def drawFrame(self):
		from xie.graphics.shape import Rectangle
		frame=Rectangle(0, 0, self.dh.getWidth(), self.dh.getHeight())
		self.dh.draw(frame)

	def clearChar(self):
		self.tcInputChar.Clear()

	def clearGlyph(self):
		self.tcInputGlyph.Clear()

	def byKnownChar(self):
		self.dh.canvasController.clear()
		self.drawFrame()

		string=self.tcInputGlyph.GetValue()
		table={
			ord(" "): None,
			ord("\t"): None,
			ord("\n"): None,
		}
		description=string.translate(table)
		character=glyphManager.computeCharacterByDescription("", description)
		from xie.graphics.shape import Boundary
		descriptionBoundary = Boundary(0, 0, 256, 256)

		self.drawFrame()

		self.dh.save()
		self.dh.setSourceBoundary(descriptionBoundary)
		self.dh.draw(character)
		self.dh.restore()

def makeSureDirCreated(filename):
	import os
	dirname = os.path.dirname(filename)
	if not os.path.exists(dirname):
		os.makedirs(dirname)

def generateSVG(dirname):
	import os
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	emsize=500
	width=emsize
	height=emsize

	from xie.graphics.canvas import SvgCanvasController
	canvasController = SvgCanvasController(width, height)

	from xie.graphics.drawing import DrawingSystem
	drawSystem = DrawingSystem(canvasController)

	strokeWidth=5

	import lxml.etree as ET

	characters=sorted(glyphManager.getCharacters())
	print("總共有 %s 個字符"%len(characters))
	for index, ch in enumerate(characters):
		if index%100==0:
			print("正在描繪 %s 到 %s 個字符"%(index*1, index+100))

		character=glyphManager.getCharacter(ch)

		from xie.graphics.shape import Boundary
		descriptionBoundary = Boundary(0, 0, 256, 256)

		drawSystem.save()
		drawSystem.setSourceBoundary(descriptionBoundary)
		drawSystem.draw(character)
		drawSystem.restore()

		attrib={
			"width": str(width),
			"height": str(height),
			}
		rootNode=ET.Element("svg", attrib)

		expression=canvasController.getExpression()
		canvasController.clear()

		attrib={
			"x": "0",
			"y": "0",
			"width": str(width),
			"height": str(height),
			"stroke": "none",
			"stroke-width": str(strokeWidth),
			"fill": "white",
			}
		rectNode=ET.SubElement(rootNode, "rect", attrib)

		attrib={
			"stroke": "black",
			"stroke-width": str(strokeWidth),
			"fill": "none",
			"d": expression
			}
		pathNode=ET.SubElement(rootNode, "path", attrib)

		xmlNode=ET.ElementTree(rootNode)

		filename="%x.svg"%ord(ch)
		f=open(dirname + os.sep + filename, "w")
		print(ET.tounicode(xmlNode, pretty_print=True), file=f)

def generateTTF(filename):
	emsize=1024
	width=emsize
	height=emsize

	from xie.graphics.canvas import TrueTypeGlyphCanvasController
	canvas=TrueTypeGlyphCanvasController(width, height)

	from xie.graphics.drawing import DrawingSystem
	drawSystem = DrawingSystem(canvas)

	import fontforge
	f=fontforge.font()
	f.is_quadratic=True
#	f.strokedfont=True
#	f.strokewidth=50
	f.em=emsize

	characters=sorted(glyphManager.getCharacters())
	print("總共有 %s 個字符"%len(characters))
	for index, ch in enumerate(characters):
		if index%100==0:
			print("正在描繪 %s 到 %s 個字符"%(index*1, index+100))

		o=ord(ch)
		g=f.createChar(o)
		g.left_side_bearing=100
		g.right_side_bearing=100
		canvas.changeGlyph(g)

		character=glyphManager.getCharacter(ch)

		from xie.graphics.shape import Boundary
		descriptionBoundary = Boundary(0, 0, 256, 256)

		drawSystem.save()
		drawSystem.setSourceBoundary(descriptionBoundary)
		drawSystem.draw(character)
		drawSystem.restore()

		# stroke(penType, strokeWidth, lineCap, lineJoin)
		# stroke(circular|calligraphic|polygon, strokeWidth, square|round|butt, miter|round|bevel)
		g.stroke("circular",30, "round", "miter")
		g.correctDirection()
		g.removeOverlap()
		g.correctDirection()

	makeSureDirCreated(filename)
	f.generate(filename)
	print('結束')

oparser = OptionParser()
oparser.add_option("-s", action="store_true", dest="show_font", help="秀出字形", default=False)
oparser.add_option("-g", dest="font_format", help="產生字型檔", default="svg")
oparser.add_option("-i", "--in-fontfile", dest="fontfile", help="字型來源檔", default="tables/puretable/qhdc-standard.txt")
oparser.add_option("-o", "--out-fontfile", dest="outfile", help="字型輸出檔", default="font/qhdc.ttf")
oparser.add_option("-d", "--out-fontdir", dest="outdir", help="字型輸出檔", default="font/svg")
(options, args) = oparser.parse_args()

glyphManager = GlyphManager()

if options.show_font:
	fontfile=options.fontfile

	app=ShowHanziWidget()
	app.mainloop()
elif options.font_format:
	fontfile=options.fontfile
	glyphManager.loadFont(fontfile)

	font_format=options.font_format
	if font_format=="svg":
		outdir=options.outdir
		generateSVG(outdir)
	elif font_format=="ttf":
		outfile=options.outfile
		generateTTF(outfile)
else:
	oparser.print_usage()

