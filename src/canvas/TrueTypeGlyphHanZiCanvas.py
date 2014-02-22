# coding=utf8

#import fontforge
from . import HanZiCanvas

class TrueTypeGlyphHanZiCanvas(HanZiCanvas.HanZiCanvas):
	def __init__(self, glyph, width, height):
		HanZiCanvas.HanZiCanvas.__init__(self, width, height)

		self.glyph=glyph
		self.glyphPen=glyph.glyphPen()
		self.clear()

	def clear(self):
		self.hasDraw=False
		self.glyph.clear()

	def moveTo(self, p):
		if self.hasDraw:
			self.glyphPen.endPath()
		self.glyphPen.moveTo(self.converCoordinate(p))
		self.hasDraw=True

	def lineTo(self, p):
		self.glyphPen.lineTo(self.converCoordinate(p))

	def qCurveTo(self, cp, p):
		self.glyphPen.qCurveTo(self.converCoordinate(cp), self.converCoordinate(p))

	def converCoordinate(self, p):
		return (p[0], self.height-p[1])

