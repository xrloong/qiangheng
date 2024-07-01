from typing import Optional
from injector import inject

from model.element.CharacterDescription import CharacterDescription
from model.element.StructureDescription import StructureDescription
from model.element.SubstituteRule import SubstituteRule

from model.helper import StructureConverter
from model.helper import OperatorManager

from model.manager import CompositionManager
from model.manager import RadixManager

from model.datamanager import QHDataManager

from tree.node import Node as TreeExpression
from tree.regexp.item import MatchResult
from tree.regexp import TreeRegExpInterpreter

from .tree import HanZiTreeProxy
from .tree import TreeNodeGenerator


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


class StructureManager:
    @inject
    def __init__(
        self,
        qhDM: QHDataManager,
        structureConverter: StructureConverter,
        operatorManager: OperatorManager,
    ):
        self.__qhDM = qhDM
        self.__structureConverter = structureConverter
        self.__operatorManager = operatorManager

    @property
    def compositionManager(self) -> CompositionManager:
        return self.__qhDM.compositionManager

    @property
    def radixManager(self) -> RadixManager:
        return self.__qhDM.radixManager

    def queryStructures(self, character: str) -> tuple[StructureDescription]:
        charDesc = self.__queryCharacterDescription(character)
        return charDesc.structures

    def __queryCharacterDescription(self, character: str) -> CharacterDescription:
        charDesc = self.radixManager.queryRadix(character)
        if not charDesc:
            charDesc = self.compositionManager.queryCharacter(character)
        charDesc.prepareStructures(self.__structureConverter)
        return charDesc

    def queryChildren(
        self, charDesc: StructureDescription
    ) -> tuple[StructureDescription]:
        return charDesc.compList

    def generateSubstituteHelperForTemplate(
        self,
        treeNodeGenerator: TreeNodeGenerator,
    ) -> SubstituteHelper:
        templateManager = self.__qhDM.templateManager
        rules = templateManager.substituteRules
        return SubstituteHelper(
            rules=rules,
            treeNodeGenerator=treeNodeGenerator,
            operatorManager=self.__operatorManager,
        )

    def generateSubstituteHelperForSubstitute(
        self,
        treeNodeGenerator: TreeNodeGenerator,
    ) -> SubstituteHelper:
        substituteManager = self.__qhDM.substituteManager
        rules = substituteManager.substituteRules
        return SubstituteHelper(
            rules=rules,
            treeNodeGenerator=treeNodeGenerator,
            operatorManager=self.__operatorManager,
        )
