import sys
import Constant

from model.element.CharacterDescription import CharacterDescription
from model.element.StructureDescription import StructureDescriptionGenerator

from injector import inject
from parser import TreeParser
import yaml

class QHParser:
	@inject
	def __init__(self, nodeGenerator: StructureDescriptionGenerator):
		self.treeParser = TreeParser
		self.treeParser.nodeGenerator = nodeGenerator

	def parseStructure(self, structureExpression):
		return self.treeParser.parse(structureExpression)

	def loadCharDescriptionByParsingYAML(self, rootNode):
		charDescList=[]
		charGroupNode=rootNode.get(Constant.TAG_CHARACTER_SET)
		for node in charGroupNode:
			charName=node.get(Constant.TAG_NAME)

			charDesc=CharacterDescription(charName)

			if Constant.TAG_STRUCTURE in node:
				structureExpression=node.get(Constant.TAG_STRUCTURE)
				comp=self.parseStructure(structureExpression)
				structureList=[comp, ]
				charDesc.setStructureList(structureList)

			charDescList.append(charDesc)
		return charDescList

	def loadCharacters(self, filename):
		node=yaml.load(open(filename), yaml.SafeLoader)
		return self.loadCharDescriptionByParsingYAML(node)

