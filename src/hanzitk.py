#!/usr/bin/env python3
# coding=utf8

import tkinter

from canvas import TkHanZiCanvas
from canvas import TrueTypeGlyphHanZiCanvas
from gear.shape import *


class HanZiDrawingSystem():
    def __init__(self, canvas, rm):
        self.canvas=canvas
        self.rm=rm

        # 描述檔預計的長寬
        self.dh=256
        self.dw=256

    def drawCharacter(self, canvas, shape, def_list):
        [ x, y, cw, ch, ]=[ shape.x, shape.y, shape.w, shape.h, ]

        point_list=[]
        is_curve=False
        for d in def_list:
            [tx, ty]=[int(d[4:6], 16), int(d[6:8], 16)]
            if d[3]=='0':
                point_list=[(x + tx*cw/self.dw, y + ty*ch/self.dh)]
                canvas.moveTo(point_list[-1])
            elif d[3]=='1':
                point_list.append((x + tx*cw/self.dw, y + ty*ch/self.dh))
                if is_curve:
                    canvas.qCurveTo(point_list[-2], point_list[-1])
                else:
                    canvas.lineTo(point_list[-1])
                is_curve=False
            elif d[3]=='2':
                point_list.append((x + tx*cw/self.dw, y + ty*ch/self.dh))
                is_curve=True

    def draw(self, def_list, canvas=None, shape=None):
        if not def_list:
            return

        if not canvas:
            canvas=self.canvas

        if not canvas:
            print("沒有畫布")
            return

        if not shape:
            shape=Rectangle(0, 0, canvas.width, canvas.height)

        canvas.clear()
        self.drawCharacter(canvas, shape, def_list)

class ShowHanziWidget():
	def __init__(self, master, rm):
		self.rm=rm

		self.canvasH=512
		self.canvasW=512

		frame=tkinter.Frame(master)
		frame.pack()

		self.entryInput=tkinter.Entry(frame)
		self.entryInput.grid(row=0, column=0)
		self.entryInput.insert(0, '王')

		self.buttonInputOK=tkinter.Button(frame, text='確定', command=self.byKnownChar)
		self.buttonInputOK.grid(row=0, column=1)

		self.ttfFilename=tkinter.Entry(frame)
		self.ttfFilename.grid(row=2, column=0)

		self.buttonGenFont=tkinter.Button(frame, text='確定', command=self.genTTF)
		self.buttonGenFont.grid(row=2, column=1)

		self.canvasHanzi=tkinter.Canvas(master=frame, width=self.canvasW, height=self.canvasH)
		self.canvasHanzi.grid(row=3, columnspan=2)

		canvas=TkHanZiCanvas.TkHanZiCanvas(self.canvasHanzi, self.canvasW, self.canvasH)
		self.dh=HanZiDrawingSystem(canvas, rm)

		self.byKnownChar()

	def genTTF(self):
		return
		emsize=1024

		filename=self.ttfFilename.get()
		if not filename:
			print('沒有指定檔名')
			return

		f=fontforge.font()
		f.is_quadratic=True
		f.strokedfont=True
		f.strokewidth=50
		f.em=emsize

		start, end=0x4E00, 0x9FA6 # 全部
#		start, end=0x4E00, 0x4EFF #
#		start, end=0x4E00, 0x4E00 # 一
#		start, end=0x738B, 0x738B # 王
#		start, end=0x738B, 0x738B # 王
#		start, end=0x76EE, 0x76EE # 目
#		start, end=0x4E3F, 0x4E3F # 丿
#		start, end=0x9F9C, 0x9F9C # 龜
#		start, end=0x4E56, 0x4E56 # 乖

		for o in range(start, end+1):
			g=f.createChar(o)
			canvas=TrueTypeGlyphHanziCanvas(g, emsize, emsize)

			if o%256==0:
				print("U+%04X"%o)

			ct=rm.getDesc(unichr(o))
			self.dh.draw(ct, canvas=canvas)

		f.save(filename)
		print('結束')

	def byKnownChar(self):
		string=self.entryInput.get()
		def_list=rm.getFont(string)
		self.dh.draw(def_list)

class RadicalManager:
	def __init__(self):
		self.fontDB={}
		self.strokeCount={}

		fontfile='_dc.xxxx'

		for line in open(fontfile).readlines():
			line=line.strip()
			if (not line) or line[0]=='#':
				continue
			else:
				ll=line.split('\t')

				if len(ll)>=2:
					def_char=ll[0]
					def_list=def_char.split(',')

					self.setFont(ll[1], def_list)

	def setFont(self, strIndex, f):
		self.fontDB[strIndex]=f

	def getFont(self, strIndex):
		return self.fontDB.get(strIndex, "")

rm=RadicalManager()

root=tkinter.Tk()
app=ShowHanziWidget(root, rm)
root.mainloop()
