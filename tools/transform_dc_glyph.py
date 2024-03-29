#!/usr/bin/env python3
# coding=utf8

import ruamel.yaml as yaml

from collections import OrderedDict

from xie.graphics import StrokeSpec
from xie.graphics import StrokeFactory

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

class GlyphDescriptionInterpreter(IfGlyphDescriptionInterpreter):
	def __init__(self):
		self.strokeFactory = StrokeFactory()

	def interpretElement(self, element: GlyphElementDescription):
		result = FlowStyleOrderedDict({GlyphTags.METHOD: element.method})
		if element.isDefinition:
			strokeType = element.strokeType
			startPoint = element.startPoint
			params = element.params
			splinePointsList = element.splinePointsList

			result[GlyphTags.TYPE] = strokeType
			if splinePointsList:
				result[GlyphTags.SPLINE_POINTS_LIST] = splinePointsList
				result[GlyphTags.START_POINT] = startPoint
				strokeSpec = StrokeSpec(strokeType, splinePointsList = splinePointsList)
			else:
				result[GlyphTags.START_POINT] = startPoint
				result[GlyphTags.PARAMETER] = params
				strokeSpec = StrokeSpec(strokeType, params)

			stroke = self.strokeFactory.generateStrokeBySpec(strokeSpec, startPoint = startPoint)
			result[GlyphTags.POSITION] = list(stroke.getStatePane().boundary)
			return result
		if element.isAnchor:
			result[GlyphTags.NAME] = element.name
			result[GlyphTags.REFRENCE_NAME] = QuotedString(element.referenceName)
			if element.position:
				result[GlyphTags.POSITION] = element.position
			return result
		if element.isReference:
			result[GlyphTags.REFRENCE_NAME] = QuotedString(element.referenceName)
			if element.order:
				result[GlyphTags.ORDER] = element.order
			if element.position:
				result[GlyphTags.POSITION] = element.position
			return result
		return result

	def interpretStroke(self, stroke: GlyphStrokeDescription):
		strokeDict = OrderedDict({GlyphTags.NAME: QuotedString(stroke.name)})
		strokeDict[GlyphTags.COMMENT] = stroke.comment

		elementDict = self.interpretElement(stroke.element)
		strokeDict[GlyphTags.STROKE] = elementDict
		return strokeDict

	def interpretComponent(self, component: GlyphComponentDescription):
		componentDicts = OrderedDict({GlyphTags.NAME: QuotedString(component.name)})
		if component.comment:
			componentDicts[GlyphTags.COMMENT] = component.comment

		elementDicts = [self.interpretElement(element) for element in component.elements]
		componentDicts[GlyphTags.STROKE] = elementDicts
		return componentDicts

	def interpretDataSet(self, dataSet: GlyphDataSetDescription):
		strokes = [self.interpretStroke(stroke) for stroke in dataSet.strokes]
		parts = [self.interpretComponent(part) for part in dataSet.parts]
		components = [self.interpretComponent(component) for component in dataSet.components]

		resultRootNode = OrderedDict({
			GlyphTags.STROKE_SET: strokes,
			GlyphTags.PART_SET: parts,
			GlyphTags.COMPONENT_SET: components,
			})
		return resultRootNode

glyphParser = GlyphParser()
interpreter = GlyphDescriptionInterpreter()

glyphDataSet = glyphParser.load(CodingTemplateFile)
resultRootNode = interpreter.interpretDataSet(glyphDataSet)
print(yaml.dump(resultRootNode, Dumper=IndentWorkAroundDumper,
    allow_unicode=True, width=200,
    explicit_start=True, explicit_end=True,
    ), end='')
