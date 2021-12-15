#!/usr/bin/env python3
# coding=utf8

import abc
import ruamel.yaml as yaml

from collections import OrderedDict

from xie.graphics import Pane
from xie.graphics import BaseTextCanvasController
from xie.graphics import DrawingSystem
from xie.graphics import Component
from xie.graphics import Character
from xie.graphics import StrokeSpec
from xie.graphics import StrokeFactory

class IndentWorkAroundDumper(yaml.Dumper):
	def increase_indent(self, flow=False, *args, **kwargs):
		return super().increase_indent(flow=flow, indentless=False)

class QuotedString(str):  # just subclass the built-in str
	pass

class FlowStyleOrderedDict(OrderedDict):
	pass

def quoted_presenter(dumper, data):
	return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
def ordered_dict(dumper, data):
	return dumper.represent_mapping('tag:yaml.org,2002:map', data.items(), style='|')
yaml.add_representer(QuotedString, quoted_presenter)
yaml.add_representer(FlowStyleOrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items(), flow_style=True))
yaml.add_representer(OrderedDict, lambda dumper, data: dumper.represent_mapping('tag:yaml.org,2002:map', data.items()))

CodingTemplateFile="qhdata/dc/radix/template.yaml"

class GlyphElementDescription:
	def __init__(self, method):
		self.method = method

		self.name = None
		self.referenceName = None
		self.order = None

		self.strokeType = None
		self.startPoint = None
		self.params = None

		self.position = None

	@property
	def isAnchor(self):
		return self.method == GlyphTags.METHOD__ANCHOR

	@property
	def isReference(self):
		return self.method == GlyphTags.METHOD__REFERENCE

	@property
	def isDefinition(self):
		return self.method == GlyphTags.METHOD__DEFINITION

class GlyphComponentDescription:
	def __init__(self, name, comment = None):
		self.name = name
		self.comment = comment
		self.elements = None

class GlyphDataSetDescription:
	def __init__(self, components: [GlyphComponentDescription]):
		self.components = components

class GlyphTags(object):
	TEMPLATE_SET = "樣式集"
	STROKE_GROUP='筆劃組'
	STROKE='筆劃'
	NAME='名稱'
	COMMENT='註記'

	METHOD='方式'
	TYPE='類型'
	START_POINT='起始點'
	PARAMETER='參數'

	METHOD__DEFINITION='定義'
	METHOD__REFERENCE='引用'
	METHOD__ANCHOR='錨點'

	REFRENCE_NAME='引用名稱'
	ORDER='順序'

	POSITION='定位'

class IfGlyphDescriptionInterpreter(object, metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def interpretElement(self, element: GlyphElementDescription):
		pass

	@abc.abstractmethod
	def interpretComponent(self, component: GlyphComponentDescription):
		pass

	@abc.abstractmethod
	def interpretDataSet(self, dataSet: GlyphDataSetDescription):
		pass

class GlyphDescriptionInterpreter(IfGlyphDescriptionInterpreter):
	def __init__(self):
		self.strokeFactory = StrokeFactory()

	def interpretElement(self, element: GlyphElementDescription):
		result = FlowStyleOrderedDict({GlyphTags.METHOD: element.method})
		if element.isDefinition:
			strokeType = element.strokeType
			startPoint = element.startPoint
			params = element.params

			result[GlyphTags.TYPE] = strokeType
			result[GlyphTags.START_POINT] = startPoint
			result[GlyphTags.PARAMETER] = params

			strokeSpec = StrokeSpec(strokeType, params)
			stroke = self.strokeFactory.generateStrokeBySpec(strokeSpec, startPoint = startPoint)
			result[GlyphTags.POSITION] = list(stroke.getStatePane().boundary)
			return result

		if element.name:
			result[GlyphTags.NAME] = element.name
		result[GlyphTags.REFRENCE_NAME] = QuotedString(element.referenceName)

		if element.order:
			result[GlyphTags.ORDER] = element.order
		if element.position:
			result[GlyphTags.POSITION] = element.position
		return result

	def interpretComponent(self, component: GlyphComponentDescription):
		componentDicts = OrderedDict({GlyphTags.NAME: QuotedString(component.name)})
		if component.comment:
			componentDicts[GlyphTags.COMMENT] = component.comment

		elementDicts = [self.interpretElement(element) for element in component.elements]
		componentDicts[GlyphTags.STROKE_GROUP] = {GlyphTags.STROKE: elementDicts}
		return componentDicts

	def interpretDataSet(self, dataSet: GlyphDataSetDescription):
		result = [self.interpretComponent(component) for component in dataSet.components]
		resultRootNode = {GlyphTags.TEMPLATE_SET: result}
		return resultRootNode

class TemplateManager(object):
	def __init__(self):
		super().__init__()

	def load(self, filename):
		rootNode = yaml.load(open(filename), Loader=yaml.SafeLoader)
		dataSet = self.parseDataSet(rootNode)
		return dataSet

	def save(self, dataSet):
		interpreter = GlyphDescriptionInterpreter()
		resultRootNode = interpreter.interpretDataSet(dataSet)
		print(yaml.dump(resultRootNode, Dumper=IndentWorkAroundDumper,
			allow_unicode=True, width=200,
			explicit_start=True, explicit_end=True,
			), end='')

	def parseElement(self, elementNode):
		method = elementNode.get(GlyphTags.METHOD)
		element = GlyphElementDescription(method)
		elementDict = FlowStyleOrderedDict({GlyphTags.METHOD: method})
		if element.isReference:
			referenceName = elementNode.get(GlyphTags.REFRENCE_NAME)
			order = elementNode.get(GlyphTags.ORDER)
			position = elementNode.get(GlyphTags.POSITION)

			element.referenceName = referenceName
			element.order = order
			if position:
				element.position = position
		elif element.isAnchor:
			name = elementNode.get(GlyphTags.NAME)
			referenceName = elementNode.get(GlyphTags.REFRENCE_NAME)
			position = elementNode.get(GlyphTags.POSITION)

			element.name = name
			element.referenceName = referenceName
			if position:
				element.position = position
		elif element.isDefinition:
			strokeType = elementNode.get(GlyphTags.TYPE)
			startPoint = elementNode.get(GlyphTags.START_POINT)
			params = elementNode.get(GlyphTags.PARAMETER)
			position = elementNode.get(GlyphTags.POSITION)

			element.strokeType = strokeType
			element.startPoint = startPoint
			element.params = params
			element.position = position
		return element

	def parseComponent(self, componentNode):
		componentName = componentNode.get(GlyphTags.NAME)
		componentComment = componentNode.get(GlyphTags.COMMENT)
		strokeGroupNode = componentNode.get(GlyphTags.STROKE_GROUP)

		component = GlyphComponentDescription(componentName, componentComment)

		elements = []
		for elementNode in strokeGroupNode.get(GlyphTags.STROKE):
			element = self.parseElement(elementNode)
			elements.append(element)

		component.elements = elements
		return component

	def parseDataSet(self, rootNode):
		dataSetNode=rootNode.get(GlyphTags.TEMPLATE_SET)

		components = []
		for componentNode in dataSetNode:
			component = self.parseComponent(componentNode)
			components.append(component)

		dataSet = GlyphDataSetDescription(components)
		return dataSet

templateManager = TemplateManager()
dataSet = templateManager.load(CodingTemplateFile)
templateManager.save(dataSet)

