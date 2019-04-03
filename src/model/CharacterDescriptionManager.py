#!/usr/bin/env python3

from injector import inject
from injector import singleton
from .element.CharacterDescription import CharacterDescription
from .manager import RadixDescriptionManager
from parser.QHParser import QHParser
from parser.QHParser import QHSubstituteRuleParser
from parser.QHParser import QHRadixParser

class SubstituteManager:
	@inject
	def __init__(self, parser: QHSubstituteRuleParser):
		self.parser = parser
		self.substituteRules = []

	def loadSubstituteRules(self, substituteFiles):
		totalSubstituteRules=[]
		for filename in substituteFiles:
			substituteRules=self.parser.loadSubstituteRules(filename)
			totalSubstituteRules.extend(substituteRules)
		self.substituteRules=totalSubstituteRules

	def getSubstituteRules(self):
		return self.substituteRules

@singleton
class CompositionManager:
	@inject
	def __init__(self, qhparser: QHParser):
		self.qhparser = qhparser

		self.characterDB={}


	def getAllCharacters(self):
		return self.characterDB.keys()

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

@singleton
class RadixManager:
	@inject
	def __init__(self, radixParser: QHRadixParser, radixDescriptionManager: RadixDescriptionManager):
		self.radixParser = radixParser
		self.radixDescriptionManager = radixDescriptionManager
		self.radixCodeInfoDB = {}
		self.radixDB = {}

	def loadRadix(self, radixFiles):
		radixDescriptionList = self.radixParser.loadRadix(radixFiles)
		for radixDescription in radixDescriptionList:
			radixName = radixDescription.getRadixName()
			self.radixDescriptionManager.addDescription(radixName, radixDescription)

		self.convert()

		resetRadixNameList = self.radixDescriptionManager.getResetRadixList()
		self.radixCodeInfoDB = self.radixDescriptionManager.getCodeInfoDB()
		for radixName in resetRadixNameList:
			self.radixDB[radixName]=CharacterDescription(radixName)

	def convert(self):
		radixDescList=self.radixDescriptionManager.getDescriptionList()

		for [charName, radixDesc] in radixDescList:
			radixCodeInfoList=self.radixParser.convertRadixDescToCodeInfoList(radixDesc)
			self.radixDescriptionManager.addCodeInfoList(charName, radixCodeInfoList)


	def getAllRadixes(self):
		return self.radixDB.keys()

	def queryRadix(self, characterName):
		return self.radixDB.get(characterName, None)

	def hasRadix(self, radixName):
		return (radixName in self.radixCodeInfoDB)

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)


if __name__=='__main__':
	pass

