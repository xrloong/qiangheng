import sys
import Constant

from description.CharacterDescription import CharacterDescription
from description.StructureDescription import StructureDescription

from parser import TreeParser
import yaml

class QHParser:
	def __init__(self, operatorGenerator):
		self.operatorGenerator=operatorGenerator

		def generateNode(structInfo=['龜', []]):
			operatorName, CompList=structInfo
			operator=operatorGenerator(operatorName)

			structDesc=StructureDescription.generate(operator, CompList)
			return structDesc
		self.g=generateNode

	def parseStructure(self, structureExpression):
		return TreeParser.parse(structureExpression, self.g)

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
		node=yaml.load(open(filename), yaml.CLoader)
		return self.loadCharDescriptionByParsingYAML(node)

