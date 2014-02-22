import sys
import Constant

from gear.CharacterProperty import CharacterProperty
from description.CharacterDescription import CharacterDescription
from description.StructureDescription import HangerStructureDescription
from description.TemplateDescription import TemplateDescription
from description.TemplateDescription import TemplateSubstitutionDescription

class QHParser:
	def __init__(self, operatorGenerator):
		self.operatorGenerator=operatorGenerator

	def generateStructureDescription(self, structInfo=['龜', []]):
		operatorName, CompList=structInfo
		operator=self.operatorGenerator(operatorName)

		structDesc=HangerStructureDescription.generate(operator, CompList)
		return structDesc

	def getDesc_Radix(self, node):
		name=node.get(Constant.TAG_REPLACEMENT)
		structDesc=self.generateStructureDescription()
		structDesc.setReferenceExpression(name)
		return structDesc

	def getDesc_AssembleChar(self, assembleChar):
		structDescList=[]
		filter_lambda=lambda x: x.tag in [Constant.TAG_RADIX, Constant.TAG_COMPOSITION]
		targetChildNodes=filter(filter_lambda , assembleChar.iterchildren())
		for node in targetChildNodes:
			if node.tag==Constant.TAG_RADIX:
				structDesc=self.getDesc_Radix(node)
			elif node.tag==Constant.TAG_COMPOSITION:
				structDesc=self.getDesc_AssembleChar(node)
			else:
				print("getDesc_AssembleChar: 預期外的標籤。", file=sys.stderr)
			structDescList.append(structDesc)

		operatorName=assembleChar.get(Constant.TAG_OPERATOR)
		if operatorName:
			comp=self.generateStructureDescription([operatorName, structDescList])
		else:
			comp=self.generateStructureDescription()

		return comp

	def getDesc_StructureList(self, nodeCharacter):
		assembleCharList=nodeCharacter.findall(Constant.TAG_COMPOSITION)
		compList=[]
		for assembleChar in assembleCharList:
			comp=self.getDesc_AssembleChar(assembleChar)

			comp.setStructureProperties(assembleChar.attrib)

			compList.append(comp)
		return compList

	def getDesc_ParameterList(self, nodeParameter):
		parameterList=[]
		targetParameterNodes=nodeParameter.findall(Constant.TAG_PARAMETER)
		for node in targetParameterNodes:
			charName=node.get(Constant.TAG_NAME)
			parameterList.append(charName)
		return parameterList

	def getDesc_Template_Substitution(self, nodeStructure):
		assembleChar=nodeStructure.find(Constant.TAG_COMPOSITION)
		comp=self.getDesc_AssembleChar(assembleChar)
		return TemplateSubstitutionDescription(comp)

	def getDesc_Template(self, nodeTemplate):
		templateName=nodeTemplate.get(Constant.TAG_NAME)

		parameterNodeList=nodeTemplate.find(Constant.TAG_PARAMETER_LIST)
		parameterNameList=self.getDesc_ParameterList(parameterNodeList)

		substitutionList=[]
		structureNodes=nodeTemplate.findall(Constant.TAG_COMPOSITION_STRUCTURE)
		for node in structureNodes:
			substitution=self.getDesc_Template_Substitution(node)
			substitutionList.append(substitution)

		return TemplateDescription(templateName, parameterNameList, substitutionList)

	def loadTemplateByParsingXML__0_3(self, rootNode):
		# 用於 0.3 版
		templateGroupNode=rootNode.find(Constant.TAG_TEMPLATE_SET)
		templateDB={}
		if None!=templateGroupNode:
			targetChildNodes=templateGroupNode.findall(Constant.TAG_TEMPLATE)
			for node in targetChildNodes:
				templateName=node.get(Constant.TAG_NAME)
				templateDesc=self.getDesc_Template(node)
				templateDB[templateName]=templateDesc
		return templateDB

	def loadCharDescriptionByParsingXML__0_3(self, rootNode):
		# 用於 0.3 版
		charGroupNode=rootNode.find(Constant.TAG_CHARACTER_SET)
		targetChildNodes=charGroupNode.findall(Constant.TAG_CHARACTER)

		charDescList=[]
		for node in targetChildNodes:
			structureList=self.getDesc_StructureList(node)
			charName=node.get(Constant.TAG_NAME)

			charProp=CharacterProperty(node.attrib)
			charDesc=CharacterDescription(charName, charProp)
			charDesc.setStructureList(structureList)

			charDescList.append(charDesc)
		return charDescList

	def loadTemplateByParsingXML(self, node):
		version=node.get(Constant.TAG_VERSION)
		templateDB={}
		if version=='0.3':
			templateDB=self.loadTemplateByParsingXML__0_3(node)
		return templateDB

	def loadCharDescriptionByParsingXML(self, node):
		version=node.get(Constant.TAG_VERSION)
		charDescList=[]
		if version=='0.3':
			charDescList=self.loadCharDescriptionByParsingXML__0_3(node)
		return charDescList

