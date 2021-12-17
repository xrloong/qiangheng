#!/usr/bin/env python3
# coding=utf8

import ruamel.yaml as yaml

from collections import OrderedDict

from xie.graphics import StrokeSpec
from xie.graphics import StrokeFactory

from parser.GlyphParser import GlyphTags
from parser.GlyphParser import GlyphParser
from parser.GlyphParser import IfGlyphDescriptionInterpreter
from parser.GlyphParser import GlyphElementDescription, GlyphComponentDescription
from parser.GlyphParser import GlyphDocumentDescription, GlyphDataSetDescription

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

	def interpretDocument(self, document: GlyphDocumentDescription):
		result = [self.interpretComponent(component) for component in document.components]
		resultRootNode = {GlyphTags.TEMPLATE_SET: result}
		return resultRootNode

	def interpretDataSet(self, dataSet: GlyphDataSetDescription):
		documentNodes = [self.interpretDocument(document) for document in dataSet.documents]
		return documentNodes

glyphParser = GlyphParser()
interpreter = GlyphDescriptionInterpreter()

glyphDataSet = glyphParser.load(CodingTemplateFile)
documentNodes = interpreter.interpretDataSet(glyphDataSet)
print(yaml.dump_all(documentNodes, Dumper=IndentWorkAroundDumper,
    allow_unicode=True, width=200,
    explicit_start=True, explicit_end=True,
    ), end='')
