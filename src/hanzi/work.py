from typing import Optional
from injector import inject

from tree.node import Node as TreeExpression
from tree.regexp.item import MatchResult
from tree.regexp import TreeRegExpInterpreter


from element.enum import FontVariance

from workspace import HanZiNode, HanZiStructure
from workspace import HanZiWorkspaceManager

from model.element.StructureDescription import StructureDescription
from model.element.CharacterInfo import CharacterInfo
from model.element.SubstituteRule import SubstituteRule
from model.interpreter import CodeInfoInterpreter
from model.helper import OperatorManager

from .tree import HanZiTreeProxy
from .tree import TreeNodeGenerator
from .manager import StructureManager


class SubstituteHelper:
    def __init__(
        self,
        rules: tuple[SubstituteRule],
        treeNodeGenerator: TreeNodeGenerator,
        operatorManager: OperatorManager,
    ):
        self.treInterpreter = TreeRegExpInterpreter(HanZiTreeProxy())
        self.treeNodeGenerator = treeNodeGenerator
        self.__operatorManager = operatorManager

        opToRuleDict = {}
        for rule in rules:
            tre = rule.tre
            opName = tre.prop["運算"]

            opRules = opToRuleDict.get(opName, ())
            opRules = opRules + (rule,)

            opToRuleDict[opName] = opRules

        self.__opToRuleDict = opToRuleDict

    def recursivelyRearrangeStructure(self, structure):
        self.__rearrangeStructure(structure)
        for childStructure in structure.getStructureList():
            self.recursivelyRearrangeStructure(childStructure)

    def __findMatchedRule(self, structure) -> Optional[SubstituteRule]:
        treInterpreter = self.treInterpreter

        def match(rule, structure):
            matchResult: MatchResult = treInterpreter.match(rule.tre, structure)
            return matchResult.isMatched()

        opName = structure.getExpandedOperatorName()
        rules = self.__opToRuleDict.get(opName, ())
        rule = next((rule for rule in rules if match(rule, structure)), None)
        return rule

    def __rearrangeStructure(self, structure):
        while True:
            rule = self.__findMatchedRule(structure)
            if rule:
                tmpStructure = self.replace(rule=rule)
                structure.changeToStructure(tmpStructure)
            else:
                break

    def replace(self, rule: SubstituteRule):
        treeNodeGenerator = self.treeNodeGenerator

        def convertNodeToStructure(node: TreeExpression, allComps):
            operatorName = node.prop["運算"]
            compList = []
            for childNode in node.children:
                if "置換" in childNode.prop:
                    name = childNode.prop["置換"]
                    reference = (name, 0)
                    compList.append(treeNodeGenerator.generateLeafNode(reference))
                elif childNode.isBackRef:
                    # \1 or \1.1
                    refExp = childNode.backRefExp

                    refExp = refExp[1:]
                    refExpList = refExp.split(".")
                    if len(refExpList) < 2:
                        # \1
                        index = int(refExpList[0])
                        compList.extend(allComps[index].getMatched())
                    else:
                        # \1.1
                        index = int(refExpList[0])
                        subIndex = int(refExpList[1])
                        referenceNode = allComps[index].getMatched()[0]
                        comp = treeNodeGenerator.generateLeafNodeByReference(
                            referenceNode, subIndex
                        )
                        compList.append(comp)
                else:
                    comp = convertNodeToStructure(childNode, allComps)
                    compList.append(comp)
            operator = self.__operatorManager.generateOperator(operatorName)
            structDesc = treeNodeGenerator.generateNode(operator, compList)
            return structDesc

        tre = rule.tre
        goalNode = rule.goal
        return convertNodeToStructure(goalNode, tre.getAll())


class CharacterStructuringWork:
    pass


class CharacterStructuringWork(HanZiWorkspaceManager.OnCreateNodeListener):
    @inject
    def __init__(
        self,
        fontVariance: FontVariance,
        operatorManager: OperatorManager,
        structureManager: StructureManager,
        workspaceManager: HanZiWorkspaceManager,
    ):
        self.fontVariance = fontVariance

        self.structureManager = structureManager

        self.__workspaceManager = workspaceManager

        rules = structureManager.templateManager.substituteRules
        self.__templateHelper = SubstituteHelper(
            rules=rules,
            treeNodeGenerator=self.treeNodeGenerator,
            operatorManager=operatorManager,
        )

        rules = structureManager.substituteManager.substituteRules
        self.__substituteHelper = SubstituteHelper(
            rules,
            treeNodeGenerator=self.treeNodeGenerator,
            operatorManager=operatorManager,
        )

    @property
    def treeNodeGenerator(self) -> TreeNodeGenerator:
        return self.__workspaceManager

    def reset(self):
        self.__workspaceManager.reset()

    def setupOnCreateNodeListener(self):
        self.__workspaceManager.setOnCreateNodeListener(self)

    def constructCharacter(self, character: str):
        node = self.__workspaceManager.touchNode(character)
        nodeStructure = node.nodeStructure
        assert nodeStructure.isNode()

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

    def onCreateNode(self, character: str):
        self.constructCharacter(character)


class CharacterCodeAppendingWork:
    @inject
    def __init__(
        self,
        workspaceManager: HanZiWorkspaceManager,
        structureManager: StructureManager,
    ):
        self.__workspaceManager = workspaceManager
        self.__radicalManager = structureManager.radixManager

    def appendCodesForAddedCharacters(self):
        workspaceManager = self.__workspaceManager
        radicalManager = self.__radicalManager

        for character in self.__workspaceManager.addedCharacters:
            characterCodes = radicalManager.queryCharacterCodes(character)
            workspaceManager.appendCharacterCodes(character, characterCodes)

        self.__workspaceManager.resetAddedCharacters()


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
