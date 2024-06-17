from typing import Optional
from injector import inject

from tree.regexp.item import TreeRegExp
from tree.regexp.item import MatchResult

from tree.node import Node as TreeExpression
from tree.parser import TreeParser

from element.enum import FontVariance

from workspace import HanZiNode, HanZiStructure
from workspace import HanZiWorkspaceManager

from model.element.StructureDescription import StructureDescription
from model.element.CharacterInfo import CharacterInfo
from model.interpreter import CodeInfoInterpreter
from model.manager import SubstituteManager

from .tree import HanZiTreeRegExpInterpreter
from .manager import StructureManager


class HanZiCodeInfosComputer:
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
        assert nodeStructure.isNode()

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
        assert nodeStructure.isNode()
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


class CharacterComputingHelper:
    class RearrangeCallback(SubstituteManager.RearrangeCallback):
        def __init__(self, computeCharacterInfo, treInterpreter):
            self.computeCharacterInfo = computeCharacterInfo
            self.treInterpreter = treInterpreter

        def prepare(self, structure):
            if structure.isWrapper():
                character = structure.referencedNodeName
                self.computeCharacterInfo.constructCharacter(character)

        def matchAndReplace(self, tre: TreeRegExp, node, goalNode: TreeExpression):
            matchResult: MatchResult = self.treInterpreter.match(tre, node)
            if matchResult.isMatched():
                return self.treInterpreter.replace(tre=tre, goalNode=goalNode)
            else:
                return None

    @inject
    def __init__(
        self,
        fontVariance: FontVariance,
        structureManager: StructureManager,
        treInterpreter: HanZiTreeRegExpInterpreter,
        workspaceManager: HanZiWorkspaceManager,
    ):
        self.fontVariance = fontVariance

        self.structureManager = structureManager

        self.__workspaceManager = workspaceManager

        self.rearrangeCallback = CharacterComputingHelper.RearrangeCallback(
            self, treInterpreter
        )

    def constructCharacter(self, character: str):
        node = self.__workspaceManager.touchNode(character)
        nodeStructure = node.nodeStructure
        assert nodeStructure.isNode()

        self.__appendRadicalCodes(nodeStructure)
        self.__appendFastCode(nodeStructure)

        self.expandNodeStructure(nodeStructure)

    def expandNodeStructure(self, nodeStructure: HanZiStructure):
        assert nodeStructure.isNode()

        workspaceManager = self.__workspaceManager

        character = nodeStructure.name
        if workspaceManager.isNodeExpanded(character):
            return

        structures = self.structureManager.queryStructures(character)
        for structDesc in structures:
            if structDesc.isEmpty():
                continue

            structure = self.__convertToStructure(structDesc)

            workspaceManager.addStructureIntoNode(structure, nodeStructure)

            isMainStructure = self.fontVariance.contains(structDesc.fontVariance)
            if isMainStructure:
                workspaceManager.setMainStructureOfNode(structure, nodeStructure)

    def __convertToStructure(self, structDesc: StructureDescription) -> HanZiStructure:
        structure = self.recursivelyConvertDescriptionToStructure(structDesc)

        structureManager = self.structureManager
        templateManager = structureManager.templateManager
        substituteManager = structureManager.substituteManager

        templateManager.recursivelyRearrangeStructure(structure, self.rearrangeCallback)
        substituteManager.recursivelyRearrangeStructure(
            structure, self.rearrangeCallback
        )

        return structure

    def recursivelyConvertDescriptionToStructure(
        self, structDesc: StructureDescription
    ) -> HanZiStructure:
        if structDesc.isLeaf():
            structure = self.generateReferenceLink(structDesc)
        else:
            structure = self.generateLink(structDesc)

        return structure

    def generateReferenceLink(self, structDesc: StructureDescription) -> HanZiStructure:
        name = structDesc.referenceName
        nodeExpression = structDesc.referenceExpression

        self.constructCharacter(name)

        l = nodeExpression.split(".")
        if len(l) > 1:
            subIndex = int(l[1])
        else:
            subIndex = 0

        return self.__workspaceManager.getWrapperStructure(name, subIndex)

    def generateLink(self, structDesc: StructureDescription) -> HanZiStructure:
        childStructureList = []
        childDescList = self.structureManager.queryChildren(structDesc)
        for childSrcDesc in childDescList:
            childStructure = self.recursivelyConvertDescriptionToStructure(childSrcDesc)
            childStructureList.append(childStructure)

        operator = structDesc.operator

        return self.__workspaceManager.generateCompoundStructure(
            operator, childStructureList
        )

    def __appendRadicalCodes(self, nodeStructure: HanZiStructure):
        assert nodeStructure.isNode()

        if not nodeStructure.hasUnitStructures():
            workspaceManager = self.__workspaceManager
            radixManager = self.structureManager.radixManager

            character = nodeStructure.name
            if radixManager.hasRadix(character):
                radixInfoList = radixManager.getRadixCodeInfoList(character)
                for radixCodeInfo in radixInfoList:
                    structure = workspaceManager.getUnitStructure(radixCodeInfo)
                    workspaceManager.addStructureIntoNode(structure, nodeStructure)

    def __appendFastCode(self, nodeStructure: HanZiStructure):
        assert nodeStructure.isNode()

        if not nodeStructure.fastCodeInfo:
            character = nodeStructure.name
            fastCodeInfo = self.structureManager.queryFastCodeInfo(character)
            if fastCodeInfo:
                nodeStructure.fastCodeInfo = fastCodeInfo

    def reset(self):
        self.__workspaceManager.reset()
