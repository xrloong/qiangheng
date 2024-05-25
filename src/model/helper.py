from injector import inject

from .element.StructureDescription import StructureDescription
from .manager import OperatorManager

from model.element.radix import RadicalSet

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

class RadixHelper:
	def __init__(self, radixParser):
		self.__radixParser = radixParser

		self.__descriptionDict = {}
		self.__radixCodeInfoDB = {}

	def loadRadix(self, radixFiles):
		radixParser = self.__radixParser

		radixDescriptions = []
		for radicalFile in radixFiles:
			model = radixParser.loadRadicalSet(radicalFile)
			radicalSet = RadicalSet(model = model)
			radixDescriptions.extend(radicalSet.radicals)

		for radixDescription in radixDescriptions:
			radixName = radixDescription.getRadixName()
			radixCodeInfos = radixParser.convertRadixDescToCodeInfoList(radixDescription)

			self.__descriptionDict[radixName] = radixDescription
			self.__radixCodeInfoDB[radixName] = radixCodeInfos

		return self.__radixCodeInfoDB

