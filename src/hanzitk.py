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

def computeCharacterDefList(name, def_list):
	from xie.graphics.shape import Rectangle
	targetRect = Rectangle(0, 0, 512, 512)
	sourceRect = Rectangle(0, 0, 256, 256)

	from xie.graphics.stroke import Segment
	from xie.graphics.stroke import BeelineSegment
	from xie.graphics.stroke import QCurveSegment
	from xie.graphics.stroke import StrokePath
	from xie.graphics.stroke import Stroke
	from xie.graphics.stroke import Character

	[ tx, ty, tw, th, ]=[ targetRect.x, targetRect.y, targetRect.w, targetRect.h, ]
	[ sx, sy, sw, sh, ]=[ sourceRect.x, sourceRect.y, sourceRect.w, sourceRect.h, ]

	point_list=[]
	is_curve=False

	startPoint=None
	lastPoint=None
	segments=[]

	strokes=[]
	for d in def_list:
		[x, y]=[int(d[4:6], 16), int(d[6:8], 16)]
		if d[3]=='0':
			point=(tx + (x-sx)*tw/sw, ty + (y-sy)*th/sh)

			if startPoint:
				strokePath=StrokePath(segments)
				stroke=Stroke(startPoint, strokePath)
				strokes.append(stroke)
			startPoint=point
			lastPoint=point
			segments=[]
			point_list=[point]
		elif d[3]=='1':
			point=(tx + (x-sx)*tw/sw, ty + (y-sy)*th/sh)
			tmpLastPoint=point
			point=[point[0]-lastPoint[0], point[1]-lastPoint[1]]
			point_list.append(point)
			if is_curve:
				segment=QCurveSegment(point_list[-2], point_list[-1])
			else:
				segment=BeelineSegment(point_list[-1])
			lastPoint=tmpLastPoint
			segments.append(segment)
			is_curve=False
		elif d[3]=='2':
			point=(tx + (x-sx)*tw/sw, ty + (y-sy)*th/sh)
			point=[point[0]-lastPoint[0], point[1]-lastPoint[1]]
			point_list.append(point)
			is_curve=True
	if startPoint:
		strokePath=StrokePath(segments)
		stroke=Stroke(startPoint, strokePath)
		strokes.append(stroke)
	return Character(name, strokes)

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
		frame.draw(self.dh)

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
		string=string.translate(table)
		def_list=re.split(',|;', string)

		self.drawFrame()

		character=computeCharacterDefList("", def_list)
		character.draw(self.dh)

class RadicalManager:
	def __init__(self, fontfile):
		self.fontDB={}
		self.strokeCount={}

		for line in open(fontfile).readlines():
			line=line.strip()
			if (not line) or line[0]=='#':
				continue
			else:
				ll=line.split('\t')

				if len(ll)>=2:
					def_char=ll[1]
					def_list=re.split(',|;', def_char)

					self.setFont(ll[0], def_list)

	def setFont(self, strIndex, f):
		self.fontDB[strIndex]=f

	def getFont(self, strIndex):
		return self.fontDB.get(strIndex, "")

	def getCharacters(self):
		return self.fontDB.keys()

def makeSureDirCreated(filename):
	import os
	dirname = os.path.dirname(filename)
	if not os.path.exists(dirname):
		os.makedirs(dirname)

def generateSVG(dirname):
	import os
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	emsize=100
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

		def_list=rm.getFont(ch)

		character=computeCharacterDefList("", def_list)
		character.draw(drawSystem)

		attrib={
			"width": str(width),
			"height": str(height),
			}
		rootNode=ET.Element("svg", attrib)

		expression=canvasController.getExpression()
		canvasController.clear()

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

		ct=rm.getFont(ch)
		def_list=rm.getFont(ch)

		character=computeCharacterDefList("", def_list)
		character.draw(drawSystem)

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

if options.show_font:
	app=ShowHanziWidget()
	app.mainloop()
elif options.font_format:
	fontfile=options.fontfile
	rm=RadicalManager(fontfile)

	font_format=options.font_format
	if font_format=="svg":
		outdir=options.outdir
		generateSVG(outdir)
	elif font_format=="ttf":
		outfile=options.outfile
		generateTTF(outfile)
else:
	oparser.print_usage()

