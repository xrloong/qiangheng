#!/usr/bin/env python3
# coding=utf8

from optparse import OptionParser
import re
from xie.graphics.utils import TextCodec
from xie.graphics.stroke import StrokeGroup
from xie.graphics.stroke import Character
from xie.graphics.factory import ShapeFactory

try:
	import xie
except ImportError:
	print("Please install the libary Xie (https://github.com/xrloong/Xie.git) first")
	import sys
	sys.exit()

class RadicalManager:
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
					character=self.computeCharacterByDescription(description)
					character.setName(charName)
					self.characterDB[charName]=character

	def getCharacter(self, strIndex):
		return self.characterDB.get(strIndex, "")

	def getCharacters(self):
		return self.characterDB.keys()

	def computeCharacterByDescription(self, description):
		charName=""
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

class ShowHanziWidget():
	def __init__(self):
		self.canvasWidth=512
		self.canvasHeight=512

		import tkinter

		self.root=tkinter.Tk()

		master=self.root
		frame=tkinter.Frame(master)
		frame.pack()

		self.labelInput=tkinter.Label(frame, text='字符')
		self.labelInput.grid(row=0, column=0)

		self.entryInput=tkinter.Entry(frame)
		self.entryInput.grid(row=0, column=1)

		self.buttonInputOK=tkinter.Button(frame, text='確定', command=self.byKnownChar)
		self.buttonInputOK.grid(row=0, column=2)

		self.buttonInputOK=tkinter.Button(frame, text='清除', command=self.clearEntry)
		self.buttonInputOK.grid(row=0, column=3)

		self.canvas = tkinter.Canvas(master=frame, width=self.canvasWidth, height=self.canvasHeight)
		self.canvas.grid(row=1, columnspan=4)


		from xie.graphics.canvas import TkCanvasController
		canvasController = TkCanvasController(self.canvas, self.canvasWidth, self.canvasHeight)

		from xie.graphics.drawing import DrawingSystem
		self.dh = DrawingSystem(canvasController)

		self.drawFrame()

	def mainloop(self):
		self.root.mainloop()

	def drawFrame(self):
		from xie.graphics.shape import Rectangle
		frame=Rectangle(0, 0, self.dh.getWidth(), self.dh.getHeight())
		self.dh.draw(frame)

	def clearEntry(self):
		length=len(self.entryInput.get())
		self.entryInput.delete(0, length)

	def byKnownChar(self):
		self.dh.canvasController.clear()
		self.drawFrame()

		string=self.entryInput.get()
		table={
			ord(" "): None,
			ord("\t"): None,
			ord("\n"): None,
		}
		description=string.translate(table)
		rm=RadicalManager()
		character=rm.computeCharacterByDescription(description)
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

	characters=sorted(rm.getCharacters())
	print("總共有 %s 個字符"%len(characters))
	for index, ch in enumerate(characters):
		if index%100==0:
			print("正在描繪 %s 到 %s 個字符"%(index*1, index+100))

		character=rm.getCharacter(ch)

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

	characters=sorted(rm.getCharacters())
	print("總共有 %s 個字符"%len(characters))
	for index, ch in enumerate(characters):
		if index%100==0:
			print("正在描繪 %s 到 %s 個字符"%(index*1, index+100))

		o=ord(ch)
		g=f.createChar(o)
		g.left_side_bearing=100
		g.right_side_bearing=100
		canvas.changeGlyph(g)

		character=rm.getCharacter(ch)

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
oparser.add_option("-i", "--in-fontfile", dest="fontfile", help="字型來源檔")
oparser.add_option("-o", "--out-fontfile", dest="outfile", help="字型輸出檔", default="font/qhdc.ttf")
oparser.add_option("-d", "--out-fontdir", dest="outdir", help="字型輸出檔", default="font/svg")
(options, args) = oparser.parse_args()

rm=RadicalManager()

if options.show_font:
	app=ShowHanziWidget()
	app.mainloop()
elif options.font_format:
	fontfile=options.fontfile
	rm.loadFont(fontfile)

	font_format=options.font_format
	if font_format=="svg":
		outdir=options.outdir
		generateSVG(outdir)
	elif font_format=="ttf":
		outfile=options.outfile
		generateTTF(outfile)
else:
	oparser.print_usage()

