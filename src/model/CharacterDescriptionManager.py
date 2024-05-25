#!/usr/bin/env python3

import abc

from injector import inject
from .element.CharacterDescription import CharacterDescription
from .helper import RadixHelper
from parser.QHParser import QHParser
from parser.QHParser import QHSubstituteRuleParser
from parser.QHParser import QHRadixParser

class RearrangeCallback(object, metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def prepare(self, structure):
		pass

	@abc.abstractmethod
	def checkApplied(self, structure):
		pass

	@abc.abstractmethod
	def setApplied(self, structure):
		pass

	@abc.abstractmethod
	def matchAndReplace(self, tre, structure, result):
		pass

class SubstituteManager:
	@inject
	def __init__(self, parser: QHSubstituteRuleParser):
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

	def recursivelyRearrangeStructure(self, structure, rearrangeCallback):
		rearrangeCallback.prepare(structure)

		if rearrangeCallback.checkApplied(structure):
			return

		self.rearrangeStructure(structure, rearrangeCallback)
		for childStructure in structure.getStructureList():
			self.recursivelyRearrangeStructure(childStructure, rearrangeCallback)

		rearrangeCallback.setApplied(structure)

	def rearrangeStructure(self, structure, rearrangeCallback):
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
	def __init__(self, qhparser: QHParser):
		self.qhparser = qhparser

		self.characterDB={}


	def queryCharacter(self, characterName):
		return self.characterDB.get(characterName, None)

	def loadComponents(self, componentFiles):
		for filename in componentFiles:
			charDescList=self.qhparser.loadCharacters(filename)
			for charDesc in charDescList:
				self._saveChar(charDesc)

	def _saveChar(self, charDesc):
		charName=charDesc.getName()

		if charName in self.characterDB:
			origCharDesc=self.characterDB.get(charName)
			origCharDesc.setStructureList(charDesc.getStructureList())
		else:
			self.characterDB[charName]=charDesc

class RadixManager:
	@inject
	def __init__(self, radixParser: QHRadixParser):
		self.radixParser = radixParser

		self.radixCodeInfoDB = {}
		self.radixDB = {}

	def loadMainRadicals(self, radixFiles):
		radixHelper = RadixHelper(self.radixParser)

		radixCodeInfoDB = radixHelper.loadRadix(radixFiles)
		self.radixCodeInfoDB = radixCodeInfoDB

	def loadAdjust(self, adjustFiles):
		radixHelper = RadixHelper(self.radixParser)
		radixCodeInfoDB = radixHelper.loadRadix(adjustFiles)

		self.radixCodeInfoDB.update(radixCodeInfoDB)

		resetRadixNameList = radixCodeInfoDB.keys()
		for radixName in resetRadixNameList:
			self.radixDB[radixName] = CharacterDescription(radixName)

	def loadFastCodes(self, fastFile):
		radixHelper = RadixHelper(self.radixParser)
		fastCodeCharacterDB = radixHelper.loadRadix([fastFile])
		return fastCodeCharacterDB

	def queryRadix(self, characterName):
		return self.radixDB.get(characterName, None)

	def hasRadix(self, radixName):
		return (radixName in self.radixCodeInfoDB)

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)


if __name__=='__main__':
	pass

