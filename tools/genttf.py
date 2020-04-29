#!/usr/bin/env python3
# coding=utf8

from optparse import OptionParser
import re
import sys
import os

try:
	import xie
	from xie.graphics.canvas import TrueTypeGlyphCanvasController
	from xie.graphics.drawing import DrawingSystem
	from xie.graphics.shape import Boundary
except ImportError:
	print("Please install the libary Xie (https://github.com/xrloong/Xie.git) first")
	sys.exit()

try:
	import fontforge
except ImportError:
	print("Please install the Python extention for fontforge")
	sys.exit()

from glyph import GlyphManager

def makeSureDirCreated(filename):
	dirname = os.path.dirname(filename)
	if not os.path.exists(dirname):
		os.makedirs(dirname)

def generateTTF(filename):
	emsize = 1024
	canvasSize = (emsize, emsize)

	canvasController = TrueTypeGlyphCanvasController(canvasSize)
	drawSystem = DrawingSystem(canvasController)

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
		canvasController.changeGlyph(g)

		character=glyphManager.getCharacter(ch)

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
oparser.add_option("-i", "--in-fontfile", dest="fontfile", help="字型來源檔", default="tables/yaml/qhdc.yaml")
oparser.add_option("-o", "--out-fontfile", dest="outfile", help="字型輸出檔", default="font/qhdc.ttf")
(options, args) = oparser.parse_args()

glyphManager = GlyphManager(options.fontfile)
glyphManager.loadFont()

outfile=options.outfile
generateTTF(outfile)

