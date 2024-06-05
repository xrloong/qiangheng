from injector import inject

from coding.Base import CodingRadixParser
from tree.node import Node
from tree.parser import constant
from element import operator as Operator
from element.enum import FontVariance

from .element.StructureDescription import StructureDescription
from .element.radix import RadixDescription

class OperatorManager:
	# 使用享元模式

	@inject
	def __init__(self):
		self.builtinOperatorDict={
			'龜':Operator.OperatorTurtle,
			'龍':Operator.OperatorLoong,
			'雀':Operator.OperatorSparrow,
			'爲':Operator.OperatorEqual,

			'蚕':Operator.OperatorSilkworm,
			'鴻':Operator.OperatorGoose,
			'回':Operator.OperatorLoop,

			'起':Operator.OperatorQi,
			'這':Operator.OperatorZhe,
			'廖':Operator.OperatorLiao,
			'載':Operator.OperatorZai,
			'斗':Operator.OperatorDou,

			'同':Operator.OperatorTong,
			'區':Operator.OperatorQu,
			'函':Operator.OperatorHan,
			'左':Operator.OperatorLeft,

			'畞':Operator.OperatorMu,
			'㘴':Operator.OperatorZuo,
			'幽':Operator.OperatorYou,
			'㒳':Operator.OperatorLiang,
			'夾':Operator.OperatorJia,

			'䜌':Operator.OperatorLuan,
			'辦':Operator.OperatorBan,
			'粦':Operator.OperatorLin,
			'瓥':Operator.OperatorLi,
			'燚':Operator.OperatorYi,
		}
		self.templateOperatorDict={
		}

	def generateOperator(self, operatorName):
		if operatorName in self.builtinOperatorDict:
			operator=self.builtinOperatorDict.get(operatorName)
		else:
			if operatorName not in self.templateOperatorDict:
				operator=Operator.Operator(operatorName)
				self.templateOperatorDict[operatorName]=operator
			operator=self.templateOperatorDict.get(operatorName)
		return operator

class StructureConverter:
	@inject
	def __init__(self, operationManager: OperatorManager):
		self.operationManager = operationManager

	def __generateNode(self, prop: dict = {}, children: tuple = ()) -> StructureDescription:
		operatorName = prop.get(constant.TAG_OPERATOR, '龜')
		operator = self.operationManager.generateOperator(operatorName)

		structDesc = StructureDescription(operator, children)

		replacement = prop.get(constant.TAG_REPLACEMENT)
		if replacement:
			structDesc.setReferenceExpression(replacement)

		structDesc.generateName()
		return structDesc

	def convert(self, node: Node, font: FontVariance) -> StructureDescription:
		structureDescription = self.__convert(node)
		structureDescription.updateFontVariance(font)
		return structureDescription

	def __convert(self, node: Node) -> StructureDescription:
		children = tuple(self.__convert(n) for n in node.children)
		return self.__generateNode(node.prop, children)

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

