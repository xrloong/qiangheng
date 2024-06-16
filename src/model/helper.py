from injector import inject

from coding.Base import CodeInfo
from coding.Base import CodingRadixParser
from tree.node import Node
from tree.parser import constant
from element.operator import Operator
from element.enum import CodeVariance
from element.enum import FontVariance

from .element.StructureDescription import StructureDescription
from .element.radix import RadixDescription
from .element.radix import RadixCodeInfoDescription


class OperatorManager:
    # 使用享元模式

    @inject
    def __init__(self):
        self.builtinOperatorDict = {
            "龜": Operator.Turtle,
            "龍": Operator.Loong,
            "雀": Operator.Sparrow,
            "爲": Operator.Equal,
            "蚕": Operator.Silkworm,
            "鴻": Operator.Goose,
            "回": Operator.Loop,
            "起": Operator.Qi,
            "這": Operator.Zhe,
            "廖": Operator.Liao,
            "載": Operator.Zai,
            "斗": Operator.Dou,
            "同": Operator.Tong,
            "區": Operator.Qu,
            "函": Operator.Han,
            "左": Operator.Left,
            "畞": Operator.Mu,
            "㘴": Operator.Zuo,
            "幽": Operator.You,
            "㒳": Operator.Liang,
            "夾": Operator.Jia,
            "䜌": Operator.Luan,
            "辦": Operator.Ban,
            "粦": Operator.Lin,
            "瓥": Operator.Li,
            "燚": Operator.Yi,
        }
        self.templateOperatorDict = {}

    def generateOperator(self, operatorName):
        if operatorName in self.builtinOperatorDict:
            operator = self.builtinOperatorDict.get(operatorName)
        else:
            if operatorName not in self.templateOperatorDict:
                operator = Operator(operatorName)
                self.templateOperatorDict[operatorName] = operator
            operator = self.templateOperatorDict.get(operatorName)
        return operator


class StructureConverter:
    @inject
    def __init__(self, operationManager: OperatorManager):
        self.operationManager = operationManager

    def __generateNode(
        self, prop: dict = {}, children: tuple = ()
    ) -> StructureDescription:
        operatorName = prop.get(constant.TAG_OPERATOR, "龜")
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

    def convertToCodeInfos(
        self, radicalDescription: RadixDescription, baseVariance: CodeVariance
    ) -> tuple[CodeInfo]:
        radicalCodeInfoList: list[CodeInfo] = []
        radicalCodeInfoDescripptions = (
            radicalDescription.getRadixCodeInfoDescriptionList()
        )
        for radicalCodeInfoDesc in radicalCodeInfoDescripptions:
            codeInfo = self.__convertToCodeInfo(
                radicalCodeInfoDesc, baseVariance=baseVariance
            )
            if codeInfo:
                radicalCodeInfoList.append(codeInfo)
        return tuple(radicalCodeInfoList)

    def __convertToCodeInfo(
        self, radixDesc: RadixCodeInfoDescription, baseVariance: CodeVariance
    ) -> CodeInfo:
        codeInfo = self.codingRadixParser.convertRadixDescToCodeInfo(radixDesc)

        codeVariance = baseVariance * radixDesc.codeVariance
        isSupportRadixCode = radixDesc.isSupportRadixCode
        codeInfo.setCodeInfoAttribute(codeVariance, isSupportRadixCode)

        return codeInfo
