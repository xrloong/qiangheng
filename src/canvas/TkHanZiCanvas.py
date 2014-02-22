# coding=utf8

from . import HanZiCanvas
import tkinter

class TkHanZiCanvas(HanZiCanvas.HanZiCanvas):
	def __init__(self, tkcanvas, width, height):
		super().__init__(width, height)

		self.canvas=tkcanvas

		self.clear()
		self.point_list=[]
		self.lastp=None
		self.drawoption={'smooth':True, 'width':20, 'capstyle':tkinter.ROUND,}

	def clear(self):
		self.canvas.delete("all")

	def moveTo(self, p):
		self.setLastPoint(p)

	def lineTo(self, p, drawoption=None):
		if drawoption==None:
			drawoption=self.drawoption
		self.canvas.create_line(self.lastp[0], self.lastp[1], p[0], p[1], drawoption)
		self.lastp=p

	def qCurveTo(self, cp, p):
		self.canvas.create_line(self.lastp[0], self.lastp[1], cp[0], cp[1], p[0], p[1], self.drawoption)
		self.setLastPoint(p)

	def setLastPoint(self, p):
		self.lastp=p

