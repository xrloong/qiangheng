import abc
import weakref
from typing import Optional

from .info import UnitStructureInfo, CompoundStructureInfo
from .workspace import HanZiStructure, HanZiNode
from .workspace import HanZiWorkspace

from coding.Base import CodeInfo
from element.operator import Operator

from hanzi.tree import TreeNodeGenerator


class HanZiWorkspaceManager(TreeNodeGenerator):
    class OnCreateNodeListener(object, metaclass=abc.ABCMeta):
        @abc.abstractmethod
        def onCreateNode(self, node: HanZiNode):
            pass

    def __init__(self):
        self.reset()
        self.__onCreateNodeListener = None

    def setOnCreateNodeListener(self, listener: OnCreateNodeListener):
        self.__onCreateNodeListener = weakref.proxy(listener)

    def __notifyOnCreateNode(self, node: HanZiNode):
        listener = self.__onCreateNodeListener
        if listener:
            self.__onCreateNodeListener.onCreateNode(node)

    def reset(self):
        self.__workspace = HanZiWorkspace()
        self.__wrapperExpressionDict = {}

    def touchNode(self, character: str) -> HanZiNode:
        (node, added) = self.__workspace.touchNode(character)
        if added:
            self.__notifyOnCreateNode(node)
        return node

    def appendCharacterCodes(
        self,
        node: HanZiNode,
        characterCodes: (tuple[CodeInfo], Optional[CodeInfo]),
    ):
        nodeStructure = node.nodeStructure

        radicalCodeInfos, fastCodeInfo = characterCodes
        for radixCodeInfo in radicalCodeInfos:
            structure = self.__genUnitStructure(radixCodeInfo)
            nodeStructure.addUnitStructure(structure)
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
        structureInfo = UnitStructureInfo(radixCodeInfo)
        return HanZiStructure(structureInfo)

    def addStructureIntoNode(
        self,
        structure: HanZiStructure,
        node: HanZiNode,
        isMainStructure: bool,
    ):
        if isMainStructure:
            nodeStructure = node.nodeStructure
            nodeStructure.structureInfo.setMainStructure(structure)

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
