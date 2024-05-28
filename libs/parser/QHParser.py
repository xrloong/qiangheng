import sys
import Constant
import ruamel.yaml

from .model import SubstituteRuleSetModel
from .model import RadicalSetModel

from model.element.CharacterDescription import CharacterDescription
from model.element.StructureDescription import StructureDescription
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
		from .model import CharacterDecompositionModel

		model = CharacterDecompositionModel(**charNode)
		structures = tuple(StructureDescription.generate(structureModel, self.structureParser) for structureModel in model.structureSet)
		return structures

	def loadCharacters(self, filename):
		node = self.yaml.load(open(filename))
		return self.loadCharDescriptionByParsingYAML(node)
