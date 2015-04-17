#!/usr/bin/env python3
# coding=utf8

from optparse import OptionParser
from gear.shape import *
import re


class HanZiDrawingSystem():
    def __init__(self, canvas):
        self.canvas=canvas

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

    def drawFrame(self):
        canvas=self.canvas
        shape=Rectangle(0, 0, canvas.width, canvas.height)
        canvas.moveTo(self.convert(shape, [0, 0]))
        canvas.lineTo(self.convert(shape, [0, 0x100]))
        canvas.lineTo(self.convert(shape, [0x100, 0x100]))
        canvas.lineTo(self.convert(shape, [0x100, 0]))
        canvas.lineTo(self.convert(shape, [0, 0]))

    def convert(self, shape, point):
        [ x, y, cw, ch, ]=[ shape.x, shape.y, shape.w, shape.h, ]
        [tx, ty]=point
        return (x + tx*cw/self.dw, y + ty*ch/self.dh)

class ShowHanziWidget():
	def __init__(self, master, rm):
		self.rm=rm

		self.canvasH=512
		self.canvasW=512

		frame=tkinter.Frame(master)
		frame.pack()

		self.labelInput=tkinter.Label(frame, text='字符')
		self.labelInput.grid(row=0, column=0)

		self.entryInput=tkinter.Entry(frame)
		self.entryInput.grid(row=0, column=1)
#		self.entryInput.insert(0, '王')

		self.buttonInputOK=tkinter.Button(frame, text='確定', command=self.byKnownChar)
		self.buttonInputOK.grid(row=0, column=2)

		self.buttonInputOK=tkinter.Button(frame, text='清除', command=self.clearEntry)
		self.buttonInputOK.grid(row=0, column=3)

		self.canvasHanzi=tkinter.Canvas(master=frame, width=self.canvasW, height=self.canvasH)
		self.canvasHanzi.grid(row=3, columnspan=3)

		from canvas import TkHanZiCanvas
		canvas=TkHanZiCanvas.TkHanZiCanvas(self.canvasHanzi, self.canvasW, self.canvasH)
		self.dh=HanZiDrawingSystem(canvas)

#		self.byKnownChar()

	def clearEntry(self):
		length=len(self.entryInput.get())
		self.entryInput.delete(0, length)

	def genTTF(self):
		filename=self.ttfFilename.get()
		if not filename:
			print('沒有指定檔名')
			return

		generateTTF(filename)


	def byKnownChar(self):
#		string=self.entryInput.get()
#		def_list=self.rm.getFont(string)
		string=self.entryInput.get()
		def_list=re.split(',|;', string)
		self.dh.draw(def_list)
		self.dh.drawFrame()

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
					def_char=ll[0]
					def_list=re.split(',|;', def_char)

					self.setFont(ll[1], def_list)

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

def generateTTF(filename):
	import fontforge

	emsize=1024

	f=fontforge.font()
	f.is_quadratic=True
#	f.strokedfont=True
#	f.strokewidth=50
	f.em=emsize

	start, end=0x4E00, 0x9FA6 # 全部

	from canvas import TrueTypeGlyphHanZiCanvas

	characters=sorted(rm.getCharacters())
	print("總共有 %s 個字符"%len(characters))
	for index, ch in enumerate(characters):
		if index%100==0:
			print("正在描繪 %s 到 %s 個字符"%(index*1, index+100))

		o=ord(ch)
		g=f.createChar(o)
		g.left_side_bearing=100
		g.right_side_bearing=100

		canvas=TrueTypeGlyphHanZiCanvas.TrueTypeGlyphHanZiCanvas(g, emsize, emsize)
		drawSystem=HanZiDrawingSystem(canvas)

		ct=rm.getFont(ch)
		drawSystem.draw(ct, canvas=canvas)

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
oparser.add_option("-g", action="store_true", dest="gen_font", help="產生字型檔", default=False)
oparser.add_option("-i", "--in-fontfile", dest="fontfile", help="字型來源檔")
#oparser.add_option("-o", "--out-fontfile", dest="outfile", help="字型輸出檔", default="font/qhdc.sfd")
oparser.add_option("-o", "--out-fontfile", dest="outfile", help="字型輸出檔", default="font/qhdc.ttf")
(options, args) = oparser.parse_args()

fontfile=options.fontfile
rm=RadicalManager(fontfile)

if options.show_font:
	import tkinter

	root=tkinter.Tk()
	app=ShowHanziWidget(root, rm)
	root.mainloop()
elif options.gen_font:
	outfile=options.outfile
	generateTTF(outfile)
else:
	oparser.print_usage()

