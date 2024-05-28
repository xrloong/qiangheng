import sys
import Constant
import ruamel.yaml

from .model import SubstituteRuleSetModel
from .model import RadicalSetModel

from model.element.CharacterDescription import CharacterDescription
from model.helper import StructureParser

class QHParser:
	def __init__(self, structureParser: StructureParser, yaml: ruamel.yaml.YAML):
		self.structureParser = structureParser
		self.yaml = yaml

	def loadSubstituteRuleSet(self, filename) -> SubstituteRuleSetModel:
		node = self.yaml.load(open(filename))
		return SubstituteRuleSetModel(**node)

	def loadRadicalSet(self, filename) -> RadicalSetModel:
		node = self.yaml.load(open(filename))
		return RadicalSetModel(**node)

	def parseStructure(self, structureExpression):
		return self.structureParser.parse(structureExpression)

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

				structureDesc = self.parseStructure(structureExpression)
				structureDesc.updateFontVariance(model.font)

				structureList.append(structureDesc)

		return structureList

	def loadCharacters(self, filename):
		node = self.yaml.load(open(filename))
		return self.loadCharDescriptionByParsingYAML(node)
