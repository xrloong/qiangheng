from injector import inject

from .OperatorManager import OperatorManager
from .manager import RadixDescriptionManager
from model.element.StructureDescription import StructureDescription
from model.element.CodeVarianceType import CodeVarianceTypeFactory
from model.manager import RadixDescriptionManager
from model.BaseCoding import CodeInfo
from model.BaseCoding import CodingRadixParser


import Constant
import yaml

class StructureDescriptionGenerator:
	@inject
	def __init__(self, operationManager: OperatorManager):
		self.operationManager = operationManager

	def generateLeafNode(self, nodeExpression):
		structDesc=self.generateNode()
		structDesc.setReferenceExpression(nodeExpression)
		structDesc.generateName()
		return structDesc

	def generateNode(self, structInfo=['龜', []]):
		operatorName, compList=structInfo
		operator=self.operationManager.generateOperator(operatorName)
		structDesc=StructureDescription(operator, compList)
		structDesc.generateName()
		return structDesc

class RadixParser:
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
		for elementCodeInfo in nodeCharacter.get(RadixParser.TAG_CODE_INFORMATION):
			radixCodeInfoDesc=self.convertElementToRadixInfo(elementCodeInfo)
			radixCodeInfoDescList.append(radixCodeInfoDesc)
		return RadixDescription(radixCodeInfoDescList, toOverridePrev)

	def parseFileType(self, rootNode):
		fileType=rootNode.get(Constant.TAG_FILE_TYPE)
		return fileType

	def parseInputMethod(self, rootNode):
		nameInputMethod=rootNode.get(Constant.TAG_INPUT_METHOD)
		return nameInputMethod

class RadixCodeInfoDescription:
	def __init__(self, infoDict, codeElementCodeInfo):
		self.codeVariance=CodeVarianceTypeFactory.generate()
		self.codeElementCodeInfo=codeElementCodeInfo

		self.setupCodeAttribute(infoDict)

	def setupCodeAttribute(self, infoDict):
		codeVarianceString=infoDict.get(Constant.TAG_CODE_VARIANCE_TYPE, Constant.VALUE_CODE_VARIANCE_TYPE_STANDARD)
		self.setCodeVarianceType(codeVarianceString)

		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupportingFromProperty(infoDict)
		self.setSupportCode(isSupportCharacterCode, isSupportRadixCode)

	def setSupportCode(self, isSupportCharacterCode, isSupportRadixCode):
		self._isSupportCharacterCode=isSupportCharacterCode
		self._isSupportRadixCode=isSupportRadixCode

	def setCodeVarianceType(self, codeVarianceString):
		self.codeVariance=CodeVarianceTypeFactory.generateByString(codeVarianceString)

	def getCodeVarianceType(self):
		return self.codeVariance

	def isSupportCharacterCode(self):
		return self._isSupportCharacterCode

	def isSupportRadixCode(self):
		return self._isSupportRadixCode

	def getCodeElement(self):
		return self.codeElementCodeInfo

class RadixDescription:
	def __init__(self, radixCodeInfoList, toOverride=True):
		self.radixCodeInfoList=radixCodeInfoList
		self.toOverridePrev=toOverride

	def isToOverridePrev(self):
		return self.toOverridePrev

	def getRadixCodeInfoDescriptionList(self):
		return self.radixCodeInfoList

	def getRadixCodeInfoDescription(self, index):
		if index in range(leng(self.radixCodeInfoList)):
			return self.radixCodeInfoList[index]

	def mergeRadixDescription(self, radixDesc):
		radixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		self.radixCodeInfoList.extend(radixCodeInfoList)

