#!/usr/bin/env python3


from typing import Optional
from injector import inject

from parser.QHParser import QHParser


from element.enum import CodeVariance
from coding.Base import CodeInfo

from .element.CharacterDescription import CharacterDescription
from .element.CharacterDescription import CharacterDecompositionSet
from .element.SubstituteRule import SubstituteRule
from .element.SubstituteRule import SubstituteRuleSet
from .element.radix import RadicalSet

from .helper import RadicalCodingConverter


class SubstituteManager:
    @inject
    def __init__(self, qhparser: QHParser):
        self.__qhparser = qhparser
        self.__substituteRules = ()

    @property
    def substituteRules(self) -> tuple[SubstituteRule]:
        return self.__substituteRules

    def loadSubstituteRules(self, substituteFiles):
        substituteRuleSets = map(
            lambda filename: self.__loadSubstituteRuleSet(filename), substituteFiles
        )
        rulesTuple = map(
            lambda substituteRuleSet: substituteRuleSet.rules, substituteRuleSets
        )
        totalSubstituteRules = sum(rulesTuple, ())
        self.__substituteRules = totalSubstituteRules

    def __loadSubstituteRuleSet(self, filename: str) -> SubstituteRuleSet:
        model = self.__qhparser.loadSubstituteRuleSet(filename)
        return SubstituteRuleSet(model=model)


class CompositionManager:
    @inject
    def __init__(self, qhparser: QHParser):
        self.qhparser = qhparser

        self.characterDB = {}

    def queryCharacter(self, characterName):
        return self.characterDB.get(characterName, None)

    def loadComponents(self, componentFiles):
        for filename in componentFiles:
            charDecompSetModel = self.qhparser.loadCharacterDecompositionSet(filename)
            charDecompositionSet = CharacterDecompositionSet(model=charDecompSetModel)

            charDescs = charDecompositionSet.charDescs
            for charDesc in charDescs:
                charName = charDesc.name
                self.characterDB[charName] = charDesc


class RadixManager:
    @inject
    def __init__(
        self, parser: QHParser, radicalCodingConverter: RadicalCodingConverter
    ):
        self.__parser = parser
        self.__radicalCodingConverter = radicalCodingConverter

        self.__radixCodeInfoDB = {}
        self.__radixDB = {}

        self.__fastCodeDB = {}

    def loadMainRadicals(self, radixFiles):
        radixCodeInfoDB = self.__loadRadix(radixFiles)
        self.__radixCodeInfoDB = radixCodeInfoDB

    def loadAdjust(self, adjustFiles):
        radixCodeInfoDB = self.__loadRadix(adjustFiles)

        self.__radixCodeInfoDB.update(radixCodeInfoDB)

        resetRadixNameList = radixCodeInfoDB.keys()
        for radixName in resetRadixNameList:
            self.__radixDB[radixName] = CharacterDescription(name=radixName)

    def loadFastCodes(self, fastFile):
        fastCodeCharacterDB = self.__loadRadix(
            [fastFile], baseVariance=CodeVariance.SIMPLIFIED
        )
        self.__fastCodeDB.update(fastCodeCharacterDB)

    def queryFastCodeInfo(self, character) -> Optional[CodeInfo]:
        fastCodeInfos = self.__fastCodeDB.get(character, None)
        if fastCodeInfos:
            assert len(fastCodeInfos) == 1
            fastCodeInfo = fastCodeInfos[0]
            return fastCodeInfo
        else:
            return None

    def queryRadix(self, characterName):
        return self.__radixDB.get(characterName, None)

    def hasRadix(self, radixName):
        return radixName in self.__radixCodeInfoDB

    def getRadixCodeInfoList(self, radixName):
        return self.__radixCodeInfoDB.get(radixName)

    def __loadRadix(
        self, radixFiles: list[str], baseVariance: CodeVariance = CodeVariance.STANDARD
    ) -> dict[str, list[CodeInfo]]:
        parser = self.__parser
        radixDescriptions = []
        for radicalFile in radixFiles:
            model = parser.loadRadicalSet(radicalFile)
            radicalSet = RadicalSet(model=model)
            radixDescriptions.extend(radicalSet.radicals)

        radicalCodingConverter = self.__radicalCodingConverter
        radixCodeInfoDB = {}
        for radixDescription in radixDescriptions:
            radixName = radixDescription.getRadixName()
            radixCodeInfos = radicalCodingConverter.convertToCodeInfos(
                radicalDescription=radixDescription, baseVariance=baseVariance
            )

            radixCodeInfoDB[radixName] = radixCodeInfos

        return radixCodeInfoDB


if __name__ == "__main__":
    pass
