import abc

import ruamel.yaml as yaml

from collections import OrderedDict

from xie.graphics import Pane
from xie.graphics import BaseTextCanvasController
from xie.graphics import DrawingSystem
from xie.graphics import Component
from xie.graphics import Character
from xie.graphics import ShapeFactory

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

class TemplateManager(object):
	TAG_TEMPLATE_SET = "樣式集"
	TAG_STROKE_GROUP='筆劃組'
	TAG_STROKE='筆劃'
	TAG_NAME='名稱'
	TAG_COMMENT='註記'

	TAG_METHOD='方式'
	TAG_TYPE='類型'
	TAG_START_POINT='起始點'
	TAG_PARAMETER='參數'

	TAG_METHOD__DEFINITION='定義'
	TAG_METHOD__REFERENCE='引用'
	TAG_METHOD__ANCHOR='錨點'

	TAG_REFRENCE_NAME='引用名稱'
	TAG_ORDER='順序'
	TAG_TRANSFORMATION='變換'

	TAG_POSITION='定位'

	def __init__(self, shapeFactory):
		super().__init__()
		self.shapeFactory=shapeFactory
		self.templates={}
		self.load()

	def put(self, name, template):
		assert isinstance(template, Component)
		self.templates[name]=template

	def get(self, name):
		return self.templates.get(name)

	def getStroke(self, name, index):
		component=self.templates.get(name)
		return component.getStrokeList()[index]

	def getStrokes(self, name, start, end):
		component=self.templates.get(name)
		return component.getStrokeList()[start, end+1]

	def load(self):
		template_file = CodingTemplateFile
		self.parseTemplateFromYAML(template_file)

	def parseTemplateFromYAML(self, filename):
		rootNode = yaml.load(open(filename), Loader=yaml.SafeLoader)
		resultRootNode = self.convertTemplateSet(rootNode)
		print(yaml.dump(resultRootNode, Dumper=IndentWorkAroundDumper,
			allow_unicode=True, width=200,
			explicit_start=True, explicit_end=True,
			), end='')

	def convertTemplateSet(self, rootNode):
		templateSetNode=rootNode.get(TemplateManager.TAG_TEMPLATE_SET)
		resultTemplateNodes = []
		for templateNode in templateSetNode:
			templateName=templateNode.get(TemplateManager.TAG_NAME)
			templateComment=templateNode.get(TemplateManager.TAG_COMMENT)
			componentNode=templateNode.get(TemplateManager.TAG_STROKE_GROUP)

			resultTemplateNode = OrderedDict({TemplateManager.TAG_NAME: QuotedString(templateName)})
			if templateComment:
				resultTemplateNode[TemplateManager.TAG_COMMENT] = templateComment
			resultTemplateNode[TemplateManager.TAG_STROKE_GROUP] = self.convertComponent(componentNode)
			resultTemplateNodes.append(resultTemplateNode)

		resultRootNode = {TemplateManager.TAG_TEMPLATE_SET: resultTemplateNodes}
		return resultRootNode

	def convertComponent(self, componentNode):
		resultComponentNode = {}

		strokes=[]
		for strokeNode in componentNode.get(TemplateManager.TAG_STROKE):
			method = strokeNode.get(TemplateManager.TAG_METHOD)
			resultStrokeNoe = FlowStyleOrderedDict({TemplateManager.TAG_METHOD: method})
			if method==TemplateManager.TAG_METHOD__REFERENCE:
				referenceName = strokeNode.get(TemplateManager.TAG_REFRENCE_NAME)
				order = strokeNode.get(TemplateManager.TAG_ORDER)
				position = strokeNode.get(TemplateManager.TAG_POSITION)

				resultStrokeNoe[TemplateManager.TAG_REFRENCE_NAME] = QuotedString(referenceName)
				resultStrokeNoe[TemplateManager.TAG_ORDER] = order
				if position:
					resultStrokeNoe[TemplateManager.TAG_POSITION] = position
			elif method==TemplateManager.TAG_METHOD__ANCHOR:
				name = strokeNode.get(TemplateManager.TAG_NAME)
				referenceName = strokeNode.get(TemplateManager.TAG_REFRENCE_NAME)
				position = strokeNode.get(TemplateManager.TAG_POSITION)

				resultStrokeNoe[TemplateManager.TAG_NAME] = name
				resultStrokeNoe[TemplateManager.TAG_REFRENCE_NAME] = QuotedString(referenceName)
				if position:
					resultStrokeNoe[TemplateManager.TAG_POSITION] = position
			elif method==TemplateManager.TAG_METHOD__DEFINITION:
				strokeType = strokeNode.get(TemplateManager.TAG_TYPE)
				startPoint = strokeNode.get(TemplateManager.TAG_START_POINT)
				params = strokeNode.get(TemplateManager.TAG_PARAMETER)

				resultStrokeNoe[TemplateManager.TAG_TYPE] = strokeType
				resultStrokeNoe[TemplateManager.TAG_START_POINT] = startPoint
				resultStrokeNoe[TemplateManager.TAG_PARAMETER] = params

				stroke = self.shapeFactory.generateParameterBasedStroke(strokeType, params, startPoint)
			strokes.append(resultStrokeNoe)
		return {TemplateManager.TAG_STROKE: strokes}

shapeFactory = ShapeFactory()
templateManager = TemplateManager(shapeFactory)
