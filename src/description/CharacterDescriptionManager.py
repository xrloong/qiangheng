#!/usr/bin/env python3

import sys
from .CharacterDescription import CharacterDescription
from parser import QHParser
import Constant

class CharacterDescriptionManager:
	def __init__(self, operationManager):
		self.characterDB={}

		def charDescQueryer(charName):
			charDesc=self.characterDB.get(charName, None)
			return charDesc

		self.charDescQueryer=charDescQueryer

		self.operationManager=operationManager

		self.parser=QHParser.QHParser(operationManager.getOperatorGenerator())

	def getAllCharacters(self):
		return self.characterDB.keys()

	def queryCharacterDescription(self, character):
		return self.charDescQueryer(character)

	def queryCharacterFrequency(self, character):
		charDesc=self.queryCharacterDescription(character)
		freq=charDesc.getFrequency()
		return freq


	def loadData(self, toTemplateList, toComponentList):
		templateDB={}
		for filename in toTemplateList:
			tmpTemplateDB=self.parser.loadTemplates(filename)
			templateDB.update(tmpTemplateDB)

		self.operationManager.setTemplateDB(templateDB)

		for filename in toComponentList:
			charDescList=self.parser.loadCharacters(filename)
			for charDesc in charDescList:
				self.saveChar(charDesc)

		structureRearranger=self.operationManager.getStructureRearranger()
		self.adjustData(structureRearranger)

	def saveChar(self, charDesc):
		charName=charDesc.getName()
		if charName in self.characterDB:
			characterProperty=charDesc.getCharacterProperty()
			origCharDesc=self.characterDB.get(charName)
			origCharDesc.setStructureList(charDesc.getStructureList())
			origCharDesc.updateCharacterProperty(charDesc.getCharacterProperty())
		else:
			characterProperty=charDesc.getCharacterProperty()
			self.characterDB[charName]=charDesc

	def queryChildren(self, charDesc):
		return charDesc.getCompList()

	def adjustData(self, structureRearranger):
		for charName in self.characterDB.keys():
#			print("name: %s"%charName, file=sys.stderr);
			charDesc=self.characterDB.get(charName)
			structureRearranger.rearrangeOn(charDesc)
#			print("name: %s %s"%(charName, structDesc), file=sys.stderr);

if __name__=='__main__':
	pass

