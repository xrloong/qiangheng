#!/usr/bin/env python3
# coding=utf8

import io

try:
    import xie
except ImportError:
    print("Please install the libary Xie (https://github.com/xrloong/Xie.git) first")
    import sys

    sys.exit()
try:
    import ruamel.yaml
except ImportError:
    print("Please install the libary ruamel.yaml")
    import sys

    sys.exit()

from xie.graphics import TextCodec
from xie.graphics import ComponentFactory
from xie.graphics import SegmentFactory
from xie.graphics import StrokeFactory
from xie.graphics import StrokeSpec
from xie.graphics import Character
from xie.graphics import Stroke


class GlyphManager:
    TAG_ENCODING_SET = "編碼集"
    TAG_CHARACTER = "字符"
    TAG_GLYPH = "字圖"

    def __init__(self, fontFile):
        self.characterDB = {}
        self.strokeCount = {}
        self.textCodec = TextCodec()

        self.segmentFactory = SegmentFactory()
        self.strokeFactory = StrokeFactory()
        self.componentFactory = ComponentFactory()

        self.fontFile = fontFile

        yaml = ruamel.yaml.YAML()
        yaml.allow_unicode = True
        yaml.default_flow_style = False
        self.yaml = yaml

    def loadFont(self):
        node = self.yaml.load(open(self.fontFile))

        yamlNodeEncodingSet = node.get(GlyphManager.TAG_ENCODING_SET)
        for yamlNodeChar in yamlNodeEncodingSet:
            character = self.computeCharacterByYamlNode(yamlNodeChar)
            self.characterDB[character.getName()] = character

    def asyncLoadFont(self, completion):
        def job():
            self.loadFont()
            completion()

        import threading

        t = threading.Thread(target=job)
        t.start()

    def getCharacter(self, strIndex):
        return self.characterDB.get(strIndex, "")

    def getCharacters(self):
        return self.characterDB.keys()

    def computeCharacterByStringDescription(self, description):
        yamlNode = self.yaml.load(description)

        character = None
        if isinstance(yamlNode, (dict,)):
            character = self.computeCharacterByYamlNode(yamlNode)
        elif isinstance(yamlNode, (list, tuple)):
            glyphDescriptions = yamlNode
            character = self.computeCharacterByGlyphDescriptions("", glyphDescriptions)
        return character

    def computeCharacterByYamlNode(self, yamlNodeChar):
        charName = yamlNodeChar.get(GlyphManager.TAG_CHARACTER)
        glyph = yamlNodeChar.get(GlyphManager.TAG_GLYPH)
        character = self.computeCharacterByGlyphDescriptions(charName, glyph)

        text = io.StringIO()
        self.yaml.dump({GlyphManager.TAG_GLYPH: glyph}, text)
        description = text.getvalue()
        text.close()

        character.description = description.strip()

        return character

    def computeCharacterByGlyphDescriptions(
        self, charName, glyphDescriptionSet
    ) -> Character:
        strokes = []
        for glyphDescription in glyphDescriptionSet:
            strokeName = glyphDescription.get("名稱")
            strokeDescription = glyphDescription.get("描繪")
            stroke = self.computeStrokeByDescription(strokeName, strokeDescription)
            strokes.append(stroke)
        component = self.componentFactory.generateComponentByStrokes(strokes)
        return Character(charName, component)

    def computeStrokeByDescription(self, strokeName, strokeDescription) -> Stroke:
        textCodec = self.textCodec
        def_list = textCodec.decodeStrokeExpression(strokeDescription)

        assert len(def_list) >= 2
        assert textCodec.isStartPoint(def_list[0])
        assert textCodec.isEndPoint(def_list[-1])

        d = def_list[0]
        point = textCodec.decodePointExpression(d)
        startPoint = point
        lastPoint = point
        segments = []
        point_list = [point]

        segmentFactory = self.segmentFactory

        is_curve = False
        for d in def_list[1:]:
            point = textCodec.decodePointExpression(d)
            if textCodec.isEndPoint(d):
                tmpLastPoint = point
                point = [point[0] - lastPoint[0], point[1] - lastPoint[1]]
                point_list.append(point)
                if is_curve:
                    segment = segmentFactory.generateSegment_QCurve(
                        point_list[-2], point_list[-1]
                    )
                else:
                    segment = segmentFactory.generateSegment_Beeline(point_list[-1])
                lastPoint = tmpLastPoint
                segments.append(segment)
                is_curve = False
            elif textCodec.isControlPoint(d):
                point = [point[0] - lastPoint[0], point[1] - lastPoint[1]]
                point_list.append(point)
                is_curve = True

        strokeSpec = StrokeSpec(strokeName, segments=segments)
        stroke = self.strokeFactory.generateStrokeBySpec(strokeSpec, startPoint)
        return stroke
