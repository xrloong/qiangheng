from injector import inject

from .element.StructureDescription import StructureDescription
from .manager import OperatorManager

from .element.CodeVarianceType import CodeVarianceType

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
	def __init__(self, codeElementCodeInfo, variance: CodeVarianceType):
		self.__codeVariance = variance
		self.__codeElementCodeInfo = codeElementCodeInfo

	def setSupportCode(self, isSupportCharacterCode, isSupportRadixCode):
		self.__isSupportCharacterCode = isSupportCharacterCode
		self.__isSupportRadixCode = isSupportRadixCode

	@property
	def codeVariance(self):
		return self.__codeVariance

	@property
	def isSupportCharacterCode(self):
		return self.__isSupportCharacterCode

	@property
	def isSupportRadixCode(self):
		return self.__isSupportRadixCode

	@property
	def codeElement(self):
		return self.__codeElementCodeInfo

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
		self.__radixParser = radixParser

		self.__descriptionDict = {}
		self.__radixCodeInfoDB = {}

	def loadRadix(self, radixFiles):
		radixParser = self.__radixParser

		radixDescriptions = radixParser.loadRadix(radixFiles)
		for radixDescription in radixDescriptions:
			radixName = radixDescription.getRadixName()
			radixCodeInfos = radixParser.convertRadixDescToCodeInfoList(radixDescription)

			self.__descriptionDict[radixName] = radixDescription
			self.__radixCodeInfoDB[radixName] = radixCodeInfos

		return self.__radixCodeInfoDB

