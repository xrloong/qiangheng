import sys
import Constant
import ruamel.yaml

from .model import SubstituteRuleSetModel
from .model import RadicalSetModel

from model.element.enum import FontVariance

from model.element.CharacterDescription import CharacterDescription
from model.helper import StructureDescriptionGenerator

from tree.parser import TreeParser

class QHTreeParser:
	def __init__(self, nodeGenerator: StructureDescriptionGenerator):
		self.treeParser = TreeParser
		self.treeParser.nodeGenerator = nodeGenerator

	def parse(self, expression):
		return self.treeParser.parse(expression)

class QHParser:
	def __init__(self, treeParser: QHTreeParser, yaml: ruamel.yaml.YAML):
		self.treeParser = treeParser
		self.yaml = yaml

	def loadSubstituteRuleSet(self, filename) -> SubstituteRuleSetModel:
		node = self.yaml.load(open(filename))
		return SubstituteRuleSetModel(**node)

	def loadRadicalSet(self, filename) -> RadicalSetModel:
		node = self.yaml.load(open(filename))
		return RadicalSetModel(**node)

	def parseStructure(self, structureExpression):
		return self.treeParser.parse(structureExpression)

	def loadCharDescriptionByParsingYAML(self, rootNode):
		charGroupNode = rootNode.get(Constant.TAG_CHARACTER_SET)
		charGroupNode = charGroupNode if charGroupNode is not None else []

		charDescList = []
		for node in charGroupNode:
			charName = node.get(Constant.TAG_NAME)

			charDesc = CharacterDescription(charName)

			structureList = self.loadStructureSet(node)
			charDesc.setStructureList(structureList)

			charDescList.append(charDesc)
		return charDescList

	def loadStructureSet(self, charNode):
		from .model import StructureModel

		structureList = []
		if Constant.TAG_STRUCTURE_SET in charNode:
			nodeStructureList = charNode.get(Constant.TAG_STRUCTURE_SET)

			for structureDict in nodeStructureList:
				model = StructureModel(**structureDict)
				structureExpression = model.expression

				fontVariance = FontVariance.All
				if model.font:
					fontVarianceDescription = model.font
					fontVariance = self.convertDescriptionToFontVariance(fontVarianceDescription)

				structureDesc = self.parseStructure(structureExpression)
				structureDesc.changeFontVariance(fontVariance)

				structureList.append(structureDesc)

		return structureList

	def loadCharacters(self, filename):
		node = self.yaml.load(open(filename))
		return self.loadCharDescriptionByParsingYAML(node)

	def convertDescriptionToFontVariance(self, description):
		if not description:
			return FontVariance.All
		elif description in Constant.LIST__FONT_VARIANCE__TRADITIONAL:
			return FontVariance.Traditional
		elif description in Constant.LIST__FONT_VARIANCE__SIMPLIFIED:
			return FontVariance.Simplified
		else:
			return FontVariance.All
