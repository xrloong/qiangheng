#!/usr/bin/env python3

import abc

from injector import inject
from .element.CharacterDescription import CharacterDescription
from .element.CharacterDescription import RadicalCharacterDescription
from parser.QHParser import QHParser

from model.element.radix import RadicalSet
from model.element.radix import RadixDescription
from model.helper import RadicalCodingConverter
from model.helper import StructureParser

class SubstituteManager:
	class RearrangeCallback(object, metaclass=abc.ABCMeta):
		@abc.abstractmethod
		def prepare(self, structure): pass

		@abc.abstractmethod
		def matchAndReplace(self, tre, structure, result): pass

	@inject
	def __init__(self, parser: QHParser):
		self.parser = parser
		self.substituteRules = []
		self.opToRuleDict = {}

	def loadSubstituteRules(self, substituteFiles):
		from parser.model import SubstituteRuleSetModel
		from model.element.SubstituteRule import SubstituteRuleSet

		totalSubstituteRules = []
		for filename in substituteFiles:
			model = self.parser.loadSubstituteRuleSet(filename)
			substituteRuleSet = SubstituteRuleSet(model = model)

			substituteRules = substituteRuleSet.rules
			totalSubstituteRules.extend(substituteRules)
		self.substituteRules = totalSubstituteRules

		for rule in totalSubstituteRules:
			tre = rule.getTRE()
			opName = tre.prop["運算"]

			rules = self.opToRuleDict.get(opName, ())
			rules = rules + (rule, )

			self.opToRuleDict[opName] = rules

	def getSubstituteRules(self):
		return self.substituteRules

	def recursivelyRearrangeStructure(self, structure, rearrangeCallback: RearrangeCallback):
		rearrangeCallback.prepare(structure)

		self.rearrangeStructure(structure, rearrangeCallback)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructure(childStructure, rearrangeCallback)

	def rearrangeStructure(self, structure, rearrangeCallback: RearrangeCallback):
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

		substituteRules = self.substituteRules
		changed = True
		while changed:
			opName = structure.getExpandedOperatorName()
			rules = self.opToRuleDict.get(opName, ())
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
			charDescs = tuple(CharacterDescription(decompositionModel, self.structureParser) for decompositionModel in charDecompSetModel.decompositionSet)
			for charDesc in charDescs:
				self._saveChar(charDesc)

	def _saveChar(self, charDesc):
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

