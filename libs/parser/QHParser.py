import sys
import Constant
import ruamel.yaml

from coding.Base import CodingRadixParser
from coding.Base import CodeInfo

from .model import SubstituteRuleSetModel
from .model import RadicalSetModel

from model.element.enum import FontVariance

from model.element.CharacterDescription import CharacterDescription
from model.element.radix import RadixDescription
from model.helper import StructureDescriptionGenerator

from parser import constant
from parser import TreeParser

class QHTreeParser:
	def __init__(self, nodeGenerator: StructureDescriptionGenerator):
		self.treeParser = TreeParser
		self.treeParser.nodeGenerator = nodeGenerator

	def parse(self, expression):
		return self.treeParser.parse(expression)

class QHSubstituteRuleParser:
	def __init__(self, yaml: ruamel.yaml.YAML):
		self.yaml = yaml

	def loadSubstituteRuleSet(self, filename) -> SubstituteRuleSetModel:
		node = self.yaml.load(open(filename))
		return SubstituteRuleSetModel(**node)

class QHParser:
	def __init__(self, treeParser: QHTreeParser, yaml: ruamel.yaml.YAML):
		self.treeParser = TreeParser
		self.yaml = yaml

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
		structureList = []
		if Constant.TAG_STRUCTURE_SET in charNode:
			nodeStructureList = charNode.get(Constant.TAG_STRUCTURE_SET)

			for structureDict in nodeStructureList:
				structureExpression = structureDict[Constant.TAG_STRUCTURE]

				fontVariance = FontVariance.All
				if Constant.TAG_FONT_VARIANCE in structureDict:
					fontVarianceDescription = structureDict[Constant.TAG_FONT_VARIANCE]
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

class QHRadixParser:
	def __init__(self, codingRadixParser: CodingRadixParser, yaml: ruamel.yaml.YAML):
		self.codingRadixParser = codingRadixParser
		self.yaml = yaml

	def loadRadicalSet(self, filename) -> RadicalSetModel:
		node = self.yaml.load(open(filename))
		return RadicalSetModel(**node)

	def convertRadixDescToCodeInfoList(self, radixDesc):
		radixCodeInfoList = []
		tmpRadixCodeInfoList = radixDesc.getRadixCodeInfoDescriptionList()
		for radixInfo in tmpRadixCodeInfoList:
			codeInfo = self.convertRadixDescToCodeInfoWithAttribute(radixInfo)
			if codeInfo:
				radixCodeInfoList.append(codeInfo)
		return radixCodeInfoList

	def convertRadixDescToCodeInfoWithAttribute(self, radixDesc):
		codeInfo = self.codingRadixParser.convertRadixDescToCodeInfo(radixDesc)

		codeVariance = radixDesc.codeVariance
		isSupportRadixCode = radixDesc.isSupportRadixCode
		codeInfo.setCodeInfoAttribute(codeVariance, isSupportRadixCode)

		return codeInfo

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo = CodeInfo()
		return codeInfo

