from injector import inject

from coding.Base import CodingRadixParser
from tree.node import Node
from tree.parser import constant

from .element.enum import FontVariance
from .element.StructureDescription import StructureDescription
from .manager import OperatorManager
from model.element.radix import RadixDescription

class StructureDescriptionGenerator:
	@inject
	def __init__(self, operationManager: OperatorManager):
		self.operationManager = operationManager

	def generateNode(self, prop: dict = {}, children: tuple = ()) -> StructureDescription:
		operatorName = prop.get(constant.TAG_OPERATOR, '龜')
		operator = self.operationManager.generateOperator(operatorName)

		structDesc = StructureDescription(operator, children)

		replacement = prop.get(constant.TAG_REPLACEMENT)
		if replacement:
			structDesc.setReferenceExpression(replacement)

		structDesc.generateName()
		return structDesc

class StructureConverter:
	def __init__(self, nodeGenerator: StructureDescriptionGenerator):
		self.nodeGenerator = nodeGenerator

	def convert(self, node: Node, font: FontVariance) -> StructureDescription:
		structureDescription = self.__convert(node)
		structureDescription.updateFontVariance(font)
		return structureDescription

	def __convert(self, node: Node) -> StructureDescription:
		children = tuple(self.__convert(n) for n in node.children)
		return self.nodeGenerator.generateNode(node.prop, children)

class RadicalCodingConverter:
	@inject
	def __init__(self, codingRadixParser: CodingRadixParser):
		self.codingRadixParser = codingRadixParser

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

