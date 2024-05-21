from injector import inject

from coding.Base import CodeInfo

from .element.StructureDescription import StructureDescription
from .element.CodeVarianceType import CodeVarianceTypeFactory
from .manager import OperatorManager


import Constant

class StructureDescriptionGenerator:
	@inject
	def __init__(self, operationManager: OperatorManager):
		self.operationManager = operationManager

	def generateLeafNode(self, nodeExpression):
		structDesc = self.generateNode()
		structDesc.setReferenceExpression(nodeExpression)
		structDesc.generateName()
		return structDesc

	def generateNode(self, structInfo = ['龜', []]):
		operatorName, compList = structInfo
		operator = self.operationManager.generateOperator(operatorName)
		structDesc = StructureDescription(operator, compList)
		structDesc.generateName()
		return structDesc

class RadixCodeInfoDescription:
	def __init__(self, infoDict, codeElementCodeInfo):
		self.codeVariance = CodeVarianceTypeFactory.generate()
		self.codeElementCodeInfo = codeElementCodeInfo

		self.setupCodeAttribute(infoDict)

	def setupCodeAttribute(self, infoDict):
		codeVarianceString = infoDict.get(Constant.TAG_CODE_VARIANCE_TYPE, Constant.VALUE_CODE_VARIANCE_TYPE_STANDARD)
		self.setCodeVarianceType(codeVarianceString)

		[isSupportCharacterCode, isSupportRadixCode] = CodeInfo.computeSupportingFromProperty(infoDict)
		self.setSupportCode(isSupportCharacterCode, isSupportRadixCode)

	def setSupportCode(self, isSupportCharacterCode, isSupportRadixCode):
		self._isSupportCharacterCode = isSupportCharacterCode
		self._isSupportRadixCode = isSupportRadixCode

	def setCodeVarianceType(self, codeVarianceString):
		self.codeVariance = CodeVarianceTypeFactory.generateByString(codeVarianceString)

	def getCodeVarianceType(self):
		return self.codeVariance

	def isSupportCharacterCode(self):
		return self._isSupportCharacterCode

	def isSupportRadixCode(self):
		return self._isSupportRadixCode

	def getCodeElement(self):
		return self.codeElementCodeInfo

class RadixDescription:
	def __init__(self, radixName, radixCodeInfoList):
		self.radixName = radixName
		self.radixCodeInfoList = radixCodeInfoList

	def getRadixName(self):
		return self.radixName

	def getRadixCodeInfoDescriptionList(self):
		return self.radixCodeInfoList

	def getRadixCodeInfoDescription(self, index):
		if index in range(leng(self.radixCodeInfoList)):
			return self.radixCodeInfoList[index]

class RadixHelper:
	def __init__(self, radixParser):
		self.radixParser = radixParser

		self.descriptionDict = {}
		self.radixCodeInfoDB = {}

	def loadRadix(self, radixFiles):
		radixDescriptionList = self.radixParser.loadRadix(radixFiles)
		for radixDescription in radixDescriptionList:
			radixName = radixDescription.getRadixName()
			self.addDescription(radixName, radixDescription)

		descriptions = tuple(self.descriptionDict.items())
		for [charName, radixDesc] in descriptions:
			radixCodeInfoList = self.radixParser.convertRadixDescToCodeInfoList(radixDesc)
			self.addCodeInfoList(charName, radixCodeInfoList)

		return self.getCodeInfoDB()

	def addCodeInfoList(self, charName, radixCodeInfoList):
		self.radixCodeInfoDB[charName] = radixCodeInfoList

	def getCodeInfoDB(self):
		return self.radixCodeInfoDB

	def addDescription(self, charName, description):
		self.descriptionDict[charName] = description

