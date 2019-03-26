import sys
import Constant

from model.element.CharacterDescription import CharacterDescription

from parser import TreeParser
import yaml

class QHParser:
	def __init__(self):
		pass

	def parseStructure(self, structureExpression):
		return TreeParser.parse(structureExpression)

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

