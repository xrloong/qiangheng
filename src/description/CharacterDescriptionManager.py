#!/usr/bin/env python3

import sys
from .CharacterDescription import CharacterDescription
from state import StateManager
from parser import QHParser
import Constant

class CharacterDescriptionManager:
	def __init__(self):
		self.characterDB={}

		def charDescQueryer(charName):
			charDesc=self.characterDB.get(charName, None)
			return charDesc

		self.charDescQueryer=charDescQueryer

	def getAllCharacters(self):
		return self.characterDB.keys()

	def queryCharacterDescription(self, character):
		return self.charDescQueryer(character)

	def loadData(self, toComponentList):
		self.loadComponent(toComponentList)
		self.adjustResetRadix()

	def loadComponent(self, toComponentList):
		parser=QHParser.QHParser()
		for filename in toComponentList:
			charDescList=parser.loadCharacters(filename)
			for charDesc in charDescList:
				self.saveChar(charDesc)

	def saveChar(self, charDesc):
		charName=charDesc.getName()

		if charName in self.characterDB:
			origCharDesc=self.characterDB.get(charName)
			origCharDesc.setStructureList(charDesc.getStructureList())
		else:
			self.characterDB[charName]=charDesc

	def queryChildren(self, charDesc):
		return charDesc.getCompList()

	def queryStructureList(self, charDesc):
		return charDesc.getStructureList()

	def adjustResetRadix(self):
		codeInfoManager=StateManager.getCodeInfoManager()
		for resetRadixName in codeInfoManager.getResetRadixList():
			charDesc=CharacterDescription(resetRadixName)
			self.characterDB[resetRadixName]=charDesc

if __name__=='__main__':
	pass

