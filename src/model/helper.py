from injector import inject

from .element.StructureDescription import StructureDescription
from .manager import OperatorManager

from model.element.radix import RadicalSet
from model.element.radix import RadixDescription

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


	def loadRadix(self, radixFiles) -> dict[str, RadixDescription]:
		radixParser = self.__radixParser

		radixDescriptions = []
		for radicalFile in radixFiles:
			model = radixParser.loadRadicalSet(radicalFile)
			radicalSet = RadicalSet(model = model)
			radixDescriptions.extend(radicalSet.radicals)

		radixCodeInfoDB = {}
		for radixDescription in radixDescriptions:
			radixName = radixDescription.getRadixName()
			radixCodeInfos = radixParser.convertRadixDescToCodeInfoList(radixDescription)

			radixCodeInfoDB[radixName] = radixCodeInfos

		return radixCodeInfoDB

