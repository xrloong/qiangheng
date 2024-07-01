from typing import Optional
from injector import inject

from element.enum import FontVariance

from workspace import HanZiNode, HanZiStructure
from workspace import HanZiWorkspaceManager

from model.element.StructureDescription import StructureDescription
from model.element.CharacterInfo import CharacterInfo
from model.interpreter import CodeInfoInterpreter

from .tree import TreeNodeGenerator
from .manager import StructureManager


class CharacterStructuringWork:
    pass


class CharacterStructuringWork(HanZiWorkspaceManager.OnCreateNodeListener):
    @inject
    def __init__(
        self,
        fontVariance: FontVariance,
        structureManager: StructureManager,
        workspaceManager: HanZiWorkspaceManager,
    ):
        self.fontVariance = fontVariance

        self.structureManager = structureManager

        self.__radicalManager = structureManager.radixManager
        self.__workspaceManager = workspaceManager

        self.__templateHelper = structureManager.generateSubstituteHelperForTemplate(
            treeNodeGenerator=self.treeNodeGenerator,
        )

        self.__substituteHelper = (
            structureManager.generateSubstituteHelperForSubstitute(
                treeNodeGenerator=self.treeNodeGenerator,
            )
        )

    @property
    def treeNodeGenerator(self) -> TreeNodeGenerator:
        return self.__workspaceManager

    def reset(self):
        self.__workspaceManager.reset()

    def setupOnCreateNodeListener(self):
        self.__workspaceManager.setOnCreateNodeListener(self)

    def constructCharacter(self, character: str):
        self.__workspaceManager.touchNode(character)

    def __expand(self, node: HanZiNode):
        nodeStructure = node.nodeStructure

        workspaceManager = self.__workspaceManager

        character = nodeStructure.name
        if workspaceManager.isNodeExpanded(character):
            return

        structures = self.structureManager.queryStructures(character)
        for structDesc in structures:
            if structDesc.isEmpty():
                continue

            isMainStructure = self.fontVariance.contains(structDesc.fontVariance)
            structure = self.__convertToStructure(structDesc)

            workspaceManager.addStructureIntoNode(
                structure, nodeStructure, isMainStructure=isMainStructure
            )

    def __convertToStructure(self, structDesc: StructureDescription) -> HanZiStructure:
        structure = self.recursivelyConvertDescriptionToStructure(structDesc)

        self.__templateHelper.recursivelyRearrangeStructure(structure)
        self.__substituteHelper.recursivelyRearrangeStructure(structure)

        return structure

    def recursivelyConvertDescriptionToStructure(
        self, structDesc: StructureDescription
    ) -> HanZiStructure:
        reference = structDesc.reference
        if bool(reference[0]):
            structure = self.treeNodeGenerator.generateLeafNode(reference=reference)
        else:
            operator = structDesc.operator

            childDescs = self.structureManager.queryChildren(structDesc)
            childStructures = tuple(
                self.recursivelyConvertDescriptionToStructure(childDesc)
                for childDesc in childDescs
            )

            structure = self.treeNodeGenerator.generateNode(
                operator=operator, children=childStructures
            )

        return structure

    def __appendCodes(self, node: HanZiNode):
        character = node.name
        characterCodes = self.__radicalManager.queryCharacterCodes(character)
        self.__workspaceManager.appendCharacterCodes(node, characterCodes)

    def onCreateNode(self, node: HanZiNode):
        self.__expand(node)
        self.__appendCodes(node)


class CharacterCodeComputingWork:
    @inject
    def __init__(
        self,
        workspaceManager: HanZiWorkspaceManager,
        codeInfoInterpreter: CodeInfoInterpreter,
    ):
        self.__workspaceManager = workspaceManager
        self.__codeInfoInterpreter = codeInfoInterpreter

    def computeCharacter(self, character: str) -> Optional[CharacterInfo]:
        node = self.__workspaceManager.touchNode(character)
        nodeStructure = node.nodeStructure

        self.__recursivelyComputeCodeInfosOfStructureTree(nodeStructure)

        return self.__getNodeCharacterInfo(node) if node else None

    def __recursivelyComputeCodeInfosOfStructureTree(self, structure: HanZiStructure):
        if not structure:
            return

        if structure.isCodeInfoGenerated():
            return

        for cihldStructure in structure.getChildStructures():
            self.__recursivelyComputeCodeInfosOfStructureTree(cihldStructure)
        self.__generateCodeInfosOfStructure(structure)

    def __generateCodeInfosOfStructure(self, structure: HanZiStructure):
        structureInfo = structure.structureInfo
        operator = structureInfo.getOperator()
        codeInfosCollection = structureInfo.codeInfos

        allCodeInfos = self.__codeInfoInterpreter.computeAllCodeInfos(
            operator, codeInfosCollection
        )
        structureInfo.setComputedCodeInfos(allCodeInfos)

    def __getNodeCharacterInfo(self, hanziNode: HanZiNode) -> CharacterInfo:
        nodeStructure = hanziNode.nodeStructure
        nodeStructureInfo = nodeStructure.structureInfo

        structureList = nodeStructureInfo.childStructures
        codeInfoList = sum(map(lambda s: s.getComputedCodeInfos(), structureList), ())

        fastCodeInfo = nodeStructure.fastCodeInfo
        if fastCodeInfo:
            codeInfoList = codeInfoList + (fastCodeInfo,)

        codeList = self.__codeInfoInterpreter.interpretCodeInfoList(codeInfoList)

        characterInfo = hanziNode.tag
        characterInfo.setCodeProps(codeList)

        return characterInfo
