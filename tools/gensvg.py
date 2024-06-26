#!/usr/bin/env python3
# coding=utf8

from optparse import OptionParser
import sys
import os

try:
    import xie
    from xie.graphics import SvgCanvasController
    from xie.graphics import DrawingSystem
except ImportError:
    print("Please install the libary Xie (https://github.com/xrloong/Xie.git) first")
    sys.exit()

from glyph import GlyphManager
import lxml.etree as ET


def generateSVG(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    emsize = 500
    width = emsize
    height = emsize
    canvasSize = (width, height)

    canvasController = SvgCanvasController(canvasSize)
    drawSystem = DrawingSystem(canvasController)

    strokeWidth = 5

    characters = sorted(glyphManager.getCharacters())
    print("總共有 %s 個字符" % len(characters))
    for index, ch in enumerate(characters):
        if index % 100 == 0:
            print("正在描繪 %s 到 %s 個字符" % (index * 1, index + 100))

        character = glyphManager.getCharacter(ch)

        drawSystem.draw(character)

        attrib = {
            "width": str(width),
            "height": str(height),
        }
        rootNode = ET.Element("svg", attrib)

        expression = canvasController.getExpression()
        canvasController.clear()

        attrib = {
            "x": "0",
            "y": "0",
            "width": str(width),
            "height": str(height),
            "stroke": "none",
            "stroke-width": str(strokeWidth),
            "fill": "white",
        }
        ET.SubElement(rootNode, "rect", attrib)

        attrib = {
            "stroke": "black",
            "stroke-width": str(strokeWidth),
            "fill": "none",
            "d": expression,
        }
        ET.SubElement(rootNode, "path", attrib)

        xmlNode = ET.ElementTree(rootNode)

        filename = "%x.svg" % ord(ch)
        f = open(dirname + os.sep + filename, "w")
        print(ET.tounicode(xmlNode, pretty_print=True), file=f)


oparser = OptionParser()
oparser.add_option(
    "-i",
    "--in-fontfile",
    dest="fontfile",
    help="字型來源檔",
    default="tables/yaml/qhdc.yaml",
)
oparser.add_option(
    "-d", "--out-fontdir", dest="outdir", help="字型輸出檔", default="font/svg"
)
(options, args) = oparser.parse_args()

glyphManager = GlyphManager(options.fontfile)
glyphManager.loadFont()

outdir = options.outdir
generateSVG(outdir)
