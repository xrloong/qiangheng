import sys
import Constant
import yaml

from model.element.SubstituteRule import SubstituteRule
from model.element.CharacterDescription import CharacterDescription
from model.helper import StructureDescriptionGenerator

from injector import inject

from parser import TreeParser

class QHSubstituteRuleParser:
	@inject
	def __init__(self):
		pass

	def loadSubstituteRules(self, filename):
		node=yaml.load(open(filename), yaml.SafeLoader)
		ruleSetNode=node.get(Constant.TAG_RULE_SET)

		if not ruleSetNode:
			return []

		substituteRules=[]
		for node in ruleSetNode:
			matchPattern=node.get(Constant.TAG_MATCH)
			replacePattern=node.get(Constant.TAG_SUBSTITUTE)

			substitueRule=SubstituteRule(matchPattern, replacePattern)
			substituteRules.append(substitueRule)

		return substituteRules

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

