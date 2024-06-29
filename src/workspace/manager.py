import abc
import weakref
from typing import Optional

from .workspace import HanZiStructure, HanZiNode
from .workspace import HanZiWorkspace
from .workspace import UnitStructureInfo, CompoundStructureInfo

from coding.Base import CodeInfo
from element.operator import Operator

from hanzi.tree import TreeNodeGenerator


class HanZiWorkspaceManager(TreeNodeGenerator):
    class OnCreateNodeListener(object, metaclass=abc.ABCMeta):
        @abc.abstractmethod
        def onCreateNode(self, character: str, node: HanZiNode):
            pass

    def __init__(self):
        self.reset()
        self.__onCreateNodeListener = None

    def setOnCreateNodeListener(self, listener: OnCreateNodeListener):
        self.__onCreateNodeListener = weakref.proxy(listener)

    def __notifyOnCreateNode(self, character: str, node: HanZiNode):
        listener = self.__onCreateNodeListener
        if listener:
            self.__onCreateNodeListener.onCreateNode(character, node)

    def isNodeExpanded(self, name: str) -> bool:
        return self.__workspace.isNodeExpanded(name)

    def reset(self):
        self.__workspace = HanZiWorkspace()
        self.__wrapperExpressionDict = {}

    def touchNode(self, character: str) -> HanZiNode:
        (node, added) = self.__workspace.touchNode(character)
        if added:
            self.__notifyOnCreateNode(character, node)
        return node

    def appendCharacterCodes(
        self,
        character: str,
        characterCodes: (tuple[CodeInfo], Optional[CodeInfo]),
    ):
        node = self.touchNode(character)
        nodeStructure = node.nodeStructure

        radicalCodeInfos, fastCodeInfo = characterCodes
        for radixCodeInfo in radicalCodeInfos:
            structure = self.__genUnitStructure(radixCodeInfo)
            self.addStructureIntoNode(structure, nodeStructure)
        if fastCodeInfo:
            nodeStructure.fastCodeInfo = fastCodeInfo

    def getCompoundStructure(
        self, operator: Operator, structures: tuple[HanZiStructure]
    ) -> HanZiStructure:
        structureInfo = CompoundStructureInfo(operator, structures)
        return HanZiStructure(structureInfo)

    def getWrapperStructure(self, reference: (str, int)) -> HanZiStructure:
        (name, subIndex) = reference
        referenceNode = self.touchNode(name)
        return referenceNode.getSubStructure(subIndex)

    def __genUnitStructure(self, radixCodeInfo: CodeInfo) -> HanZiStructure:
        structureInfo = self.__generateUnitStructureInfo(radixCodeInfo)
        return HanZiStructure(structureInfo)

    def __generateUnitStructureInfo(self, radixCodeInfo: CodeInfo) -> UnitStructureInfo:
        return UnitStructureInfo(radixCodeInfo)

    def addStructureIntoNode(
        self,
        structure: HanZiStructure,
        nodeStructure: HanZiStructure,
        isMainStructure: bool = False,
    ):
        assert nodeStructure.isNode()

        nodeStructure.structureInfo.addStructure(
            structure, isMainStructure=isMainStructure
        )

    def generateLeafNode(self, reference: (str, int)) -> HanZiStructure:
        return self.getWrapperStructure(reference=reference)

    def generateLeafNodeByReference(
        self, structure: HanZiStructure, index: int
    ) -> HanZiStructure:
        reference = (structure.referencedNodeName, index)
        return self.getWrapperStructure(reference=reference)

    def generateNode(
        self, operator: Operator, children: tuple[HanZiStructure]
    ) -> HanZiStructure:
        return self.getCompoundStructure(operator, children)
