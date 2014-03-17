import sys
import Constant

from description.CharacterDescription import CharacterDescription
from description.StructureDescription import HangerStructureDescription
from description.TemplateDescription import TemplateDescription
from description.TemplateDescription import TemplateSubstitutionDescription

from parser import TreeParser
import yaml

class QHParser:
	def __init__(self, operatorGenerator):
		self.operatorGenerator=operatorGenerator

		def generateNode(structInfo=['龜', []]):
			operatorName, CompList=structInfo
			operator=operatorGenerator(operatorName)

			structDesc=HangerStructureDescription.generate(operator, CompList)
			return structDesc
		self.g=generateNode

	def loadTemplateByParsingYAML(self, node):
		templateDB={}
		templateGroupNode=node.get(Constant.TAG_TEMPLATE_SET)
		for node in templateGroupNode:
			templateName=node.get(Constant.TAG_NAME)
			parameterNameList=node.get(Constant.TAG_PARAMETER_LIST)
			structureExpression=node.get(Constant.TAG_STRUCTURE)

			comp=self.parseStructure(structureExpression)
			substitutionList=[TemplateSubstitutionDescription(comp), ]

			templateDesc=TemplateDescription(templateName, parameterNameList, substitutionList)
			templateDB[templateName]=templateDesc
		return templateDB

	def loadTemplates(self, filename):
		node=yaml.load(open(filename), yaml.CLoader)
		return self.loadTemplateByParsingYAML(node)

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

