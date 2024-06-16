#!/usr/bin/env python3
# coding=utf8

from optparse import OptionParser
import sys

try:
    import xie
    from xie.graphics import WxCanvasController
    from xie.graphics import DrawingSystem
    from xie.graphics import Rectangle
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


class ShowHanziWidget:
    def __init__(self):
        canvasSize = (512, 512)

        self.root = wx.App(False)

        sizer = wx.GridBagSizer(3, 1)

        frame = wx.Frame(None, title="秀漢字程式", size=(520, 800))
        frame.SetBackgroundColour("gray")
        frame.SetAutoLayout(True)
        frame.SetSizer(sizer)

        charSBox = wx.StaticBox(frame, label="字符")
        charSBoxSizer = wx.StaticBoxSizer(charSBox, wx.HORIZONTAL)

        tcInputChar = wx.TextCtrl(frame)
        tcInputChar.SetEditable(True)
        charSBoxSizer.Add(tcInputChar, proportion=1, flag=wx.ALIGN_TOP)

        charSBoxSizer.AddSpacer(10)

        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        btnInputCharOK = wx.Button(frame, label="載入")
        btnInputCharOK.Bind(wx.EVT_BUTTON, self.onInputCharOkClicked)
        vBoxSizer.Add(btnInputCharOK)

        btnInputCharClear = wx.Button(frame, label="清除")
        btnInputCharClear.Bind(wx.EVT_BUTTON, self.onInputCharClearClicked)
        vBoxSizer.Add(btnInputCharClear)
        charSBoxSizer.Add(vBoxSizer)

        sizer.Add(charSBoxSizer, pos=(0, 0), border=5, flag=wx.EXPAND | wx.ALL)

        tcInputChar.Disable()
        btnInputCharOK.Disable()
        btnInputCharClear.Disable()

        glyphSBox = wx.StaticBox(frame, label="字形描述")
        glyphSBoxSizer = wx.StaticBoxSizer(glyphSBox, wx.HORIZONTAL)

        tcInputGlyph = wx.TextCtrl(frame, style=wx.TE_MULTILINE)
        tcInputGlyph.SetEditable(True)
        tcInputGlyph.OSXDisableAllSmartSubstitutions()
        glyphSBoxSizer.Add(tcInputGlyph, proportion=1, flag=wx.EXPAND)

        glyphSBoxSizer.Add((10, 100))

        vBoxSizer = wx.BoxSizer(wx.VERTICAL)
        btnInputGlyphOk = wx.Button(frame, label="確定")
        btnInputGlyphOk.Bind(wx.EVT_BUTTON, self.onInputGlyphOkClicked)
        vBoxSizer.Add(btnInputGlyphOk)

        btnInputGlyphClear = wx.Button(frame, label="清除")
        btnInputGlyphClear.Bind(wx.EVT_BUTTON, self.onInputGlyphClearClicked)
        vBoxSizer.Add(btnInputGlyphClear)
        glyphSBoxSizer.Add(vBoxSizer)

        sizer.Add(glyphSBoxSizer, pos=(1, 0), border=5, flag=wx.EXPAND | wx.ALL)

        self.tcInputChar = tcInputChar
        self.tcInputGlyph = tcInputGlyph

        canvasController = WxCanvasController(frame, canvasSize)
        sizer.Add(
            canvasController.canvas,
            pos=(2, 0),
            flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER,
        )
        sizer.AddGrowableRow(2)

        frame.Show()

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
        ch = self.tcInputChar.GetValue()
        character = glyphManager.getCharacter(ch)
        self.tcInputGlyph.SetValue(character.description)

        self.drawFrame()

        self.dh.draw(character)

    def onInputCharClearClicked(self, event):
        self.clearChar()

    def onInputGlyphClearClicked(self, event):
        self.clearGlyph()

    def onInputGlyphOkClicked(self, event):
        self.byKnownChar()

    def drawFrame(self):
        frame = Rectangle(0, 0, self.dh.getWidth(), self.dh.getHeight())
        self.dh.draw(frame)

    def clearChar(self):
        self.tcInputChar.Clear()

    def clearGlyph(self):
        self.tcInputGlyph.Clear()

    def byKnownChar(self):
        self.dh.canvasController.clear()
        self.drawFrame()

        stringGlyphDescription = self.tcInputGlyph.GetValue()

        character = glyphManager.computeCharacterByStringDescription(
            stringGlyphDescription
        )
        if not character:
            return

        self.drawFrame()

        self.dh.draw(character)


oparser = OptionParser()
oparser.add_option(
    "-i",
    "--in-fontfile",
    dest="fontfile",
    help="字型來源檔",
    default="tables/yaml/qhdc.yaml",
)
(options, args) = oparser.parse_args()

glyphManager = GlyphManager(options.fontfile)

app = ShowHanziWidget()
app.mainloop()
