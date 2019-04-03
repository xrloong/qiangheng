import sys
import Constant
import yaml

from model.BaseCoding import CodingRadixParser
from model.element.SubstituteRule import SubstituteRule
from model.element.CharacterDescription import CharacterDescription
from model.helper import StructureDescriptionGenerator
from model.helper import RadixDescription
from model.helper import RadixCodeInfoDescription
from model.manager import RadixDescriptionManager

from injector import inject

from parser import TreeParser

class QHTreeParser:
	@inject
	def __init__(self, nodeGenerator: StructureDescriptionGenerator):
		self.treeParser = TreeParser
		self.treeParser.nodeGenerator = nodeGenerator

	def parse(self, expression):
		return self.treeParser.parse(expression)

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
	def __init__(self, treeParser: QHTreeParser):
		self.treeParser = TreeParser

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

class QHRadixParser:
	TAG_CODE_INFORMATION='編碼資訊'
	TAG_CODE='編碼'

	@inject
	def __init__(self, codingRadixParser: CodingRadixParser, radixDescriptionManager: RadixDescriptionManager):
		self.codingRadixParser = codingRadixParser
		self.radixDescriptionManager = radixDescriptionManager
		self.radixCodeInfoDB = {}

	def loadRadix(self, radixFileList):
		self.parse(radixFileList)

		self.convert()
		return (self.radixDescriptionManager.getResetRadixList(), self.radixDescriptionManager.getCodeInfoDB())


	def getRadixDescription(self, radixName):
		return self.radixDescriptionManager.getDescription(radixName)


	def convert(self):
		radixDescList=self.radixDescriptionManager.getDescriptionList()

		for [charName, radixDesc] in radixDescList:
			radixCodeInfoList=self.convertRadixDescToCodeInfoList(radixDesc)
			self.radixDescriptionManager.addCodeInfoList(charName, radixCodeInfoList)

	def convertRadixDescToCodeInfoList(self, radixDesc):
		radixCodeInfoList=[]
		tmpRadixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		for radixInfo in tmpRadixCodeInfoList:
			codeInfo=self.convertRadixDescToCodeInfoWithAttribute(radixInfo)
			if codeInfo:
				radixCodeInfoList.append(codeInfo)
		return radixCodeInfoList

	def convertRadixDescToCodeInfoWithAttribute(self, radixDesc):
		codeInfo=self.codingRadixParser.convertRadixDescToCodeInfo(radixDesc)

		codeVariance=radixDesc.getCodeVarianceType()
		isSupportCharacterCode=radixDesc.isSupportCharacterCode()
		isSupportRadixCode=radixDesc.isSupportRadixCode()
		codeInfo.setCodeInfoAttribute(codeVariance, isSupportCharacterCode, isSupportRadixCode)

		return codeInfo

	def convertElementToRadixInfo(self, elementCodeInfo):
		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo

		codeElementCodeInfo=elementCodeInfo
		radixInfoDescription=RadixCodeInfoDescription(infoDict, codeElementCodeInfo)
		return radixInfoDescription

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=CodeInfo()
		return codeInfo

	def parse(self, toRadixList):
		for filename in toRadixList:
			self.parseRadixFromYAML(filename)

	def parseRadixFromYAML(self, filename):
		rootNode=yaml.load(open(filename), Loader=yaml.SafeLoader)

		self.parseRadixInfo(rootNode)

	def parseRadixInfo(self, rootNode):
		characterSetNode=rootNode.get(Constant.TAG_CHARACTER_SET)
		for characterNode in characterSetNode:
			charName=characterNode.get(Constant.TAG_NAME)
			radixDescription=self.parseRadixDescription(characterNode)

			self.radixDescriptionManager.addDescription(charName, radixDescription)

	def parseRadixDescription(self, nodeCharacter):
		radixCodeInfoDescList=[]
		toOverridePrev=("是" == nodeCharacter.get("覆蓋"))
		for elementCodeInfo in nodeCharacter.get(QHRadixParser.TAG_CODE_INFORMATION):
			radixCodeInfoDesc=self.convertElementToRadixInfo(elementCodeInfo)
			radixCodeInfoDescList.append(radixCodeInfoDesc)
		return RadixDescription(radixCodeInfoDescList, toOverridePrev)

	def parseFileType(self, rootNode):
		fileType=rootNode.get(Constant.TAG_FILE_TYPE)
		return fileType

	def parseInputMethod(self, rootNode):
		nameInputMethod=rootNode.get(Constant.TAG_INPUT_METHOD)
		return nameInputMethod

