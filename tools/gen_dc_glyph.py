#!/usr/bin/env python3
# coding=utf8

import ruamel.yaml as yaml

from collections import OrderedDict

from xie.graphics import Pane
from xie.graphics import Component
from xie.graphics import StrokeSpec
from xie.graphics import StrokeFactory
from xie.graphics import ShapeFactory

from xie.graphics import DrawingSystem
from xie.graphics import BaseTextCanvasController

from parser.GlyphParser import GlyphTags
from parser.GlyphParser import GlyphParser
from parser.GlyphParser import IfGlyphDescriptionInterpreter
from parser.GlyphParser import GlyphElementDescription
from parser.GlyphParser import GlyphStrokeDescription, GlyphComponentDescription
from parser.GlyphParser import GlyphDataSetDescription

CodingTemplateFile="qhdata/dc/radix/template.yaml"

class IndentWorkAroundDumper(yaml.Dumper):
	def increase_indent(self, flow=False, *args, **kwargs):
		return super().increase_indent(flow=flow, indentless=False)

# just subclass the built-in str
class QuotedString(str): pass
class FlowStyleOrderedDict(OrderedDict): pass

def quoted_presenter(dumper, data):
	return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
def ordered_dict(dumper, data):
	return dumper.represent_mapping('tag:yaml.org,2002:map', data.items(), style='|')
yaml.add_representer(QuotedString, quoted_presenter)
yaml.add_representer(FlowStyleOrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items(), flow_style=True))
yaml.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))

class YamlCanvasController(BaseTextCanvasController):
	def __init__(self):
		super().__init__()
		self.strokes = []

	def getStrokes(self):
		return self.strokes

	def onPreDrawCharacter(self, character):
		self.strokes=[]

	def onPreDrawStroke(self, stroke):
		self.clearStrokeExpression()

	def onPostDrawStroke(self, stroke):
		e=self.getStrokeExpression()
		if e:
			attrib={
				"名稱": stroke.getName(),
				"描繪": e,
				}
			self.strokes.append(attrib)

class GlyphDescriptionInterpreter(IfGlyphDescriptionInterpreter):
	def __init__(self):
		self.strokeFactory = StrokeFactory()
		self.shapeFactory = ShapeFactory()

		self.anchors = {}
		self.templates = {}

	def getStroke(self, name, index):
		component=self.templates.get(name)
		return component.getStrokeList()[index]

	def applyComponentWithTransformation(self, component, position):
		if position != None:
			pane = Pane(*position)
			component = self.shapeFactory.generateComponentByComponentPane(component, pane)
		return component

	def getComponent(self, name):
		component = self.anchors.get(name)
		if not component:
			component = self.templates.get(name)
		return component

	def interpretStrokeByDefinition(self, element):
		strokeType = element.strokeType
		params = element.params
		startPoint = element.startPoint
		position = element.position
		pane = Pane(*position)
		splinePointsList = element.splinePointsList
		if splinePointsList:
			strokeSpec = StrokeSpec(strokeType, splinePointsList = splinePointsList)
		else:
			strokeSpec = StrokeSpec(strokeType, params)
		stroke = self.strokeFactory.generateStrokeBySpec(strokeSpec, strokeBoundPane = pane)
		return stroke

	def interpretStrokeByReference(self, element: GlyphElementDescription):
		referenceName = element.referenceName
		order = element.order
		position = element.position

		referencedComponent = self.getComponent(referenceName)
		strokes = self.retrieveStrokesOfComponentIntoPosition(referencedComponent, order, position)
		return strokes

	def retrieveStrokesOfComponentIntoPosition(self, referencedComponent: Component, order: [int], position):
		strokes = list((referencedComponent.getStroke(index) for index in order))
		component = self.shapeFactory.generateComponentByStrokes(strokes)

		component = self.applyComponentWithTransformation(component, position)
		return component.getStrokeList()

	def interpretElement(self, element: GlyphElementDescription):
		strokes = []

		if element.isReference:
			strokes = self.interpretStrokeByReference(element)
		elif element.isAnchor:
			anchorName = element.name
			referenceName = element.referenceName
			position = element.position

			referencedComponent = self.getComponent(referenceName)
			component = self.applyComponentWithTransformation(referencedComponent, position)

			self.anchors[anchorName] = component
		elif element.isDefinition:
			stroke = self.interpretStrokeByDefinition(element)
			strokes = [stroke]
		else:
			assert False
		return strokes

	def getDrawResult(self, component: Component):
		controller = YamlCanvasController()
		ds = DrawingSystem(controller)

		ds.clear()
		ds.draw(component)

		drawStrokes = controller.getStrokes()
		return drawStrokes

	def interpretStroke(self, stroke: GlyphStrokeDescription):
		name = stroke.name

		self.anchors.clear()
		strokes = self.interpretElement(stroke.element)

		component = self.shapeFactory.generateComponentByStrokes(strokes)
		self.templates[name] = component

		drawStrokes = self.getDrawResult(component)

		strokeDicts = OrderedDict({"字符": QuotedString(name)})
		strokeDicts["類型"] = "標準"
		strokeDicts["字圖"] = drawStrokes
		return strokeDicts

	def interpretComponent(self, component: GlyphComponentDescription):
		name = component.name

		self.anchors.clear()
		strokes = []
		for element in component.elements:
			subStrokes = self.interpretElement(element)
			strokes.extend(subStrokes)

		component = self.shapeFactory.generateComponentByStrokes(strokes)
		self.templates[name] = component

		drawStrokes = self.getDrawResult(component)

		componentDicts = OrderedDict({"字符": QuotedString(name)})
		componentDicts["類型"] = "標準"
		componentDicts["字圖"] = drawStrokes
		return componentDicts

	def interpretDataSet(self, dataSet: GlyphDataSetDescription):
		strokes = [self.interpretStroke(stroke) for stroke in dataSet.strokes]
		parts = [self.interpretComponent(component) for component in dataSet.parts]
		components = [self.interpretComponent(component) for component in dataSet.components]

		doc = OrderedDict({"編碼類型": "描繪法"})
		doc["編碼集"] = strokes + parts + components
		return doc

glyphParser = GlyphParser()
interpreter = GlyphDescriptionInterpreter()

glyphDataSet = glyphParser.load(CodingTemplateFile)
resultRootNode = interpreter.interpretDataSet(glyphDataSet)
print(yaml.dump(resultRootNode, Dumper=IndentWorkAroundDumper,
	allow_unicode=True, width=60, default_flow_style=False,
	explicit_start=True, explicit_end=True,
	), end='')
