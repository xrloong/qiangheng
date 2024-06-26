from model.element import CharacterInfo

from .info import (
    StructureInfo,
    WrapperStructureInfo,
    NodeStructureInfo,
)


class HanZiStructure:
    pass


class HanZiStructure:
    def __init__(self, structureInfo: StructureInfo):
        self.__structureInfo = structureInfo
        self.__fastCodeInfo = None

    @property
    def structureInfo(self) -> StructureInfo:
        return self.__structureInfo

    @property
    def name(self) -> str:
        return self.structureInfo.getName()

    @property
    def referencedNodeName(self) -> str:
        nodeStructureInfo = self.structureInfo.referencedNodeStructureInfo
        return nodeStructureInfo.getName()

    @property
    def fastCodeInfo(self):
        return self.__fastCodeInfo

    @fastCodeInfo.setter
    def fastCodeInfo(self, fastCodeInfo):
        self.__fastCodeInfo = fastCodeInfo

    def getComputedCodeInfos(self):
        return self.structureInfo.getComputedCodeInfos()

    def isCodeInfoGenerated(self):
        return self.structureInfo.isCodeInfoGenerated()

    def isMatchStructure(self, operatorName=None, referenceExpression=None):
        isMatch = True
        if referenceExpression:
            isMatch &= referenceExpression == self.structureInfo.referenceExpression

        if operatorName:
            isMatch &= operatorName == self.structureInfo.getExpandedOperatorName()

        return isMatch

    def addUnitStructure(self, structure: HanZiStructure):
        self.structureInfo.addUnitStructure(structure)

    def getStructureList(self) -> tuple[StructureInfo]:
        return self.structureInfo.getStructureList()

    def getExpandedOperatorName(self) -> str:
        return self.structureInfo.getExpandedOperatorName()

    def getExpandedStructureList(self) -> tuple[HanZiStructure]:
        return self.structureInfo.getExpandedStructureList()

    def getChildStructures(self) -> tuple[HanZiStructure]:
        return self.structureInfo.childStructures

    def changeToStructure(self, newTargetStructure: HanZiStructure):
        self.__structureInfo = newTargetStructure.structureInfo


class HanZiNode:
    def __init__(self, name: str):
        self.__name = name
        self.__tag = CharacterInfo.CharacterInfo(name)

        nodeStructureInfo = NodeStructureInfo(name)
        self.__nodeStructure = HanZiStructure(nodeStructureInfo)
        self.__subStructureDict = {}

        self.__expanded = False

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        return self.__name

    @property
    def nodeStructure(self) -> HanZiStructure:
        return self.__nodeStructure

    @property
    def tag(self) -> CharacterInfo.CharacterInfo:
        return self.__tag

    @property
    def expanded(self) -> bool:
        return self.__expanded

    def setExpanded(self):
        self.__expanded = True

    def getSubStructure(self, index: int = 0) -> HanZiStructure:
        if index in self.__subStructureDict:
            return self.__subStructureDict[index]

        structureInfo = WrapperStructureInfo(self.nodeStructure, index)
        structure = HanZiStructure(structureInfo)
        self.__subStructureDict[index] = structure
        return structure


class HanZiWorkspace:
    def __init__(self):
        self.__nodeDict = {}

    def reset(self):
        self.__nodeDict = {}

    def __addNode(self, node):
        name = node.name
        self.__nodeDict[name] = node

    def __isWithNode(self, name):
        return name in self.__nodeDict

    def __findNode(self, name):
        return self.__nodeDict.get(name)

    def touchNode(self, character: str) -> (HanZiNode, bool):
        if not self.__isWithNode(character):
            node = HanZiNode(character)
            self.__addNode(node)
            added = True
        else:
            node = self.__findNode(character)
            added = False
        return (node, added)
