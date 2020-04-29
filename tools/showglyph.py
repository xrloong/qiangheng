#!/usr/bin/env python3
# coding=utf8

from optparse import OptionParser
import re
import sys

try:
	import xie
	from xie.graphics.canvas import CanvasController
	from xie.graphics.drawing import DrawingSystem
	from xie.graphics.shape import Boundary
	from xie.graphics.shape import Rectangle
except ImportError:
	print("Please install the libary Xie (https://github.com/xrloong/Xie.git) first")
	sys.exit()
try:
	import wx
	from wx.lib.floatcanvas import FloatCanvas
except ImportError:
	print("Please install the libary wxPython")
	sys.exit()


from glyph import GlyphManager

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

		tcInputChar.Disable()
		btnInputCharOK.Disable()
		btnInputCharClear.Disable()


		glyphSBox = wx.StaticBox(frame, label='字形描述')
		glyphSBoxSizer = wx.StaticBoxSizer(glyphSBox, wx.HORIZONTAL)

		tcInputGlyph = wx.TextCtrl(frame, style=wx.TE_MULTILINE)
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

		self.canvas = FloatCanvas.FloatCanvas(frame,
				ProjectionFun = lambda x: (1, -1),
				size = (self.canvasWidth, self.canvasHeight))
		canvasLayoutFlag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER
		sizer.Add(self.canvas, pos=(2, 0), flag=canvasLayoutFlag)
		sizer.AddGrowableRow(2)

		frame.Show()

		canvasController = WxCanvasController(self.canvas, self.canvasWidth, self.canvasHeight)
		self.dh = DrawingSystem(canvasController)

		self.drawFrame()

		def onLoadComplete():
			tcInputChar.Enable()
			btnInputCharOK.Enable()
			btnInputCharClear.Enable()
		glyphManager.asyncLoadFont(onLoadComplete)

	def mainloop(self):
		self.root.MainLoop()

	def onInputCharOkClicked(self, event):
		ch=self.tcInputChar.GetValue()
		character=glyphManager.getCharacter(ch)
		self.tcInputGlyph.SetValue(character.description)

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
		frame=Rectangle(0, 0, self.dh.getWidth(), self.dh.getHeight())
		self.dh.draw(frame)

	def clearChar(self):
		self.tcInputChar.Clear()

	def clearGlyph(self):
		self.tcInputGlyph.Clear()

	def byKnownChar(self):
		self.dh.canvasController.clear()
		self.drawFrame()

		stringGlyphDescription = self.tcInputGlyph.GetValue()

		character = glyphManager.computeCharacterByStringDescription(stringGlyphDescription)
		if not character:
			return

		descriptionBoundary = Boundary(0, 0, 256, 256)

		self.drawFrame()

		self.dh.save()
		self.dh.setSourceBoundary(descriptionBoundary)
		self.dh.draw(character)
		self.dh.restore()

oparser = OptionParser()
oparser.add_option("-i", "--in-fontfile", dest="fontfile", help="字型來源檔", default="tables/yaml/qhdc.yaml")
(options, args) = oparser.parse_args()

glyphManager = GlyphManager(options.fontfile)

app=ShowHanziWidget()
app.mainloop()

