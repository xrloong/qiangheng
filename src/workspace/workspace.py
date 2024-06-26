from model.element import CharacterInfo

from .info import (
    StructureInfo,
    UnitStructureInfo,
    WrapperStructureInfo,
    CompoundStructureInfo,
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

    def isUnit(self) -> bool:
        return isinstance(self.structureInfo, UnitStructureInfo)

    def isWrapper(self) -> bool:
        return isinstance(self.structureInfo, WrapperStructureInfo)

    def isCompound(self) -> bool:
        return isinstance(self.structureInfo, CompoundStructureInfo)

    def isNode(self) -> bool:
        return isinstance(self.structureInfo, NodeStructureInfo)

    def hasMainStructure(self) -> bool:
        return self.structureInfo.hasMainStructure()

    def isCodeInfoGenerated(self):
        return self.structureInfo.isCodeInfoGenerated()

    def isMatchStructure(self, operatorName=None, referenceExpression=None):
        isMatch = True
        if referenceExpression:
            isMatch &= referenceExpression == self.structureInfo.referenceExpression

        if operatorName:
            isMatch &= operatorName == self.structureInfo.getExpandedOperatorName()

        return isMatch

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

    def isNodeExpanded(self, name):
        node = self.__findNode(name)
        nodeStructure = node.nodeStructure
        return nodeStructure.hasMainStructure()
