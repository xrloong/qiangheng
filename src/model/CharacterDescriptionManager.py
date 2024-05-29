#!/usr/bin/env python3

import abc
from injector import inject

from parser.QHParser import QHParser

from .element.CharacterDescription import CharacterDescription
from .element.CharacterDescription import RadicalCharacterDescription
from .element.CharacterDescription import CharacterDecompositionSet
from .element.SubstituteRule import SubstituteRuleSet
from .element.radix import RadicalSet
from .element.radix import RadixDescription

from .helper import RadicalCodingConverter
from .helper import StructureParser

class SubstituteManager:
	class RearrangeCallback(object, metaclass=abc.ABCMeta):
		@abc.abstractmethod
		def prepare(self, structure): pass

		@abc.abstractmethod
		def matchAndReplace(self, tre, structure, result): pass

	@inject
	def __init__(self, qhparser: QHParser):
		self.__qhparser = qhparser
		self.__substituteRules = []
		self.__opToRuleDict = {}

	def loadSubstituteRules(self, substituteFiles):
		totalSubstituteRules = []
		for filename in substituteFiles:
			model = self.__qhparser.loadSubstituteRuleSet(filename)
			substituteRuleSet = SubstituteRuleSet(model = model)

			substituteRules = substituteRuleSet.rules
			totalSubstituteRules.extend(substituteRules)
		self.__substituteRules = totalSubstituteRules

		for rule in totalSubstituteRules:
			tre = rule.getTRE()
			opName = tre.prop["運算"]

			rules = self.__opToRuleDict.get(opName, ())
			rules = rules + (rule, )

			self.__opToRuleDict[opName] = rules

	def recursivelyRearrangeStructure(self, structure, rearrangeCallback: RearrangeCallback):
		rearrangeCallback.prepare(structure)

		self.__rearrangeStructure(structure, rearrangeCallback)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructure(childStructure, rearrangeCallback)

	def __rearrangeStructure(self, structure, rearrangeCallback: RearrangeCallback):
		def expandLeaf(structure):
			rearrangeCallback.prepare(structure)

			children = structure.getStructureList()
			for child in children:
				expandLeaf(child)

		def rearrangeStructureOneTurn(structure, filteredSubstituteRules):
			changed = False
			for rule in filteredSubstituteRules:
				tre = rule.getTRE()
				result = rule.getReplacement()

				tmpStructure = rearrangeCallback.matchAndReplace(tre, structure, result)
				if tmpStructure != None:
					structure.changeToStructure(tmpStructure)
					structure = tmpStructure
					changed = True
					break
			return changed

		substituteRules = self.__substituteRules
		changed = True
		while changed:
			opName = structure.getExpandedOperatorName()
			rules = self.__opToRuleDict.get(opName, ())
			changed = rearrangeStructureOneTurn(structure, rules)

class CompositionManager:
	@inject
	def __init__(self, qhparser: QHParser, structureParser: StructureParser):
		self.qhparser = qhparser
		self.structureParser = structureParser

		self.characterDB={}


	def queryCharacter(self, characterName):
		return self.characterDB.get(characterName, None)

	def loadComponents(self, componentFiles):
		for filename in componentFiles:
			charDecompSetModel = self.qhparser.loadCharacterDecompositionSet(filename)
			charDecompositionSet = CharacterDecompositionSet(model = charDecompSetModel)
			charDecompositionSet.prepareStructures(self.structureParser)

			charDescs = charDecompositionSet.charDescs
			for charDesc in charDescs:
				charName = charDesc.name
				self.characterDB[charName] = charDesc

class RadixManager:
	@inject
	def __init__(self, parser: QHParser, radicalCodingConverter: RadicalCodingConverter):
		self.__parser = parser
		self.__radicalCodingConverter = radicalCodingConverter

		self.__radixCodeInfoDB = {}
		self.__radixDB = {}

	def loadMainRadicals(self, radixFiles):
		radixCodeInfoDB = self.__loadRadix(radixFiles)
		self.__radixCodeInfoDB = radixCodeInfoDB

	def loadAdjust(self, adjustFiles):
		radixCodeInfoDB = self.__loadRadix(adjustFiles)

		self.__radixCodeInfoDB.update(radixCodeInfoDB)

		resetRadixNameList = radixCodeInfoDB.keys()
		for radixName in resetRadixNameList:
			self.__radixDB[radixName] = RadicalCharacterDescription(radixName)

	def loadFastCodes(self, fastFile):
		fastCodeCharacterDB = self.__loadRadix([fastFile])
		return fastCodeCharacterDB

	def queryRadix(self, characterName):
		return self.__radixDB.get(characterName, None)

	def hasRadix(self, radixName):
		return (radixName in self.__radixCodeInfoDB)

	def getRadixCodeInfoList(self, radixName):
		return self.__radixCodeInfoDB.get(radixName)

	def __loadRadix(self, radixFiles: list[str]) -> dict[str, RadixDescription]:
		parser = self.__parser
		radixDescriptions = []
		for radicalFile in radixFiles:
			model = parser.loadRadicalSet(radicalFile)
			radicalSet = RadicalSet(model = model)
			radixDescriptions.extend(radicalSet.radicals)

		radicalCodingConverter = self.__radicalCodingConverter
		radixCodeInfoDB = {}
		for radixDescription in radixDescriptions:
			radixName = radixDescription.getRadixName()
			radixCodeInfos = radicalCodingConverter.convertRadixDescToCodeInfoList(radixDescription)

			radixCodeInfoDB[radixName] = radixCodeInfos

		return radixCodeInfoDB

if __name__=='__main__':
	pass

