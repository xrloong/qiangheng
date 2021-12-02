#!/usr/bin/env python3
# coding=utf8

try:
	import xie
except ImportError:
	print("Please install the libary Xie (https://github.com/xrloong/Xie.git) first")
	import sys
	sys.exit()
try:
	import ruamel.yaml as yaml
except ImportError:
	print("Please install the libary wxPython")
	import sys
	sys.exit()

from xie.graphics.utils import TextCodec
from xie.graphics import Component
from xie.graphics import Character
from xie.graphics.factory import ShapeFactory

class GlyphManager:
	TAG_ENCODING_SET = "編碼集"
	TAG_CHARACTER = "字符"
	TAG_GLYPH = "字圖"

	def __init__(self, fontFile):
		self.characterDB={}
		self.strokeCount={}
		self.textCodec=TextCodec()
		self.shapeFactory=ShapeFactory()
		self.fontFile=fontFile

	def loadFont(self):
		node=yaml.load(open(self.fontFile), yaml.cyaml.CSafeLoader)

		yamlNodeEncodingSet = node.get(GlyphManager.TAG_ENCODING_SET)
		for yamlNodeChar in yamlNodeEncodingSet:
			character = self.computeCharacterByYamlNode(yamlNodeChar)
			self.characterDB[character.getName()] = character

	def asyncLoadFont(self, completion):
		def job():
			self.loadFont()
			completion()

		import threading
		t = threading.Thread(target = job)
		t.start()

	def getCharacter(self, strIndex):
		return self.characterDB.get(strIndex, "")

	def getCharacters(self):
		return self.characterDB.keys()

	def computeCharacterByStringDescription(self, description):
		yamlNode = yaml.load(description, yaml.cyaml.CSafeLoader)

		character = None
		if isinstance(yamlNode, (dict, )):
			character = self.computeCharacterByYamlNode(yamlNode)
		elif isinstance(yamlNode, (list, tuple)):
			glyphDescriptions = yamlNode
			character = self.computeCharacterByGlyphDescriptions("", glyphDescriptions)
		return character

	def computeCharacterByYamlNode(self, yamlNodeChar):
		charName = yamlNodeChar.get(GlyphManager.TAG_CHARACTER)
		glyph = yamlNodeChar.get(GlyphManager.TAG_GLYPH)
		character = self.computeCharacterByGlyphDescriptions(charName, glyph)

		description = yaml.dump({GlyphManager.TAG_GLYPH: glyph},
				allow_unicode=True, default_flow_style=False)
		character.description = description.strip()

		return character

	def computeCharacterByGlyphDescriptions(self, charName, glyphDescriptionSet):
		strokes=[]
		for glyphDescription in glyphDescriptionSet:
			strokeName=glyphDescription.get('名稱')
			strokeDescription=glyphDescription.get('描繪')
			stroke=self.computeStrokeByDescription(strokeName, strokeDescription)
			strokes.append(stroke)
		component=self.shapeFactory.generateComponentByStrokeList(strokes)
		return Character(charName, component)

	def computeStrokeByDescription(self, strokeName, strokeDescription):
		textCodec=self.textCodec
		def_list=textCodec.decodeStrokeExpression(strokeDescription)

		assert len(def_list) >= 2
		assert textCodec.isStartPoint(def_list[0])
		assert textCodec.isEndPoint(def_list[-1])

		d=def_list[0]
		point=textCodec.decodePointExpression(d)
		startPoint=point
		lastPoint=point
		segments=[]
		point_list=[point]

		from xie.graphics.segment import SegmentFactory
		from xie.graphics.segment import StrokePath
		from xie.graphics import Stroke
		from xie.graphics import StrokeInfo
		segmentFactory = SegmentFactory()

		is_curve=False
		for d in def_list[1:]:
			point=textCodec.decodePointExpression(d)
			if textCodec.isEndPoint(d):
				tmpLastPoint=point
				point=[point[0]-lastPoint[0], point[1]-lastPoint[1]]
				point_list.append(point)
				if is_curve:
					segment=segmentFactory.generateSegment_QCurve(point_list[-2], point_list[-1])
				else:
					segment=segmentFactory.generateSegment_Beeline(point_list[-1])
				lastPoint=tmpLastPoint
				segments.append(segment)
				is_curve=False
			elif textCodec.isControlPoint(d):
				point=[point[0]-lastPoint[0], point[1]-lastPoint[1]]
				point_list.append(point)
				is_curve=True

		stroke=self.shapeFactory.generateSegmentBasedStroke(strokeName, segments, startPoint)
		return stroke

