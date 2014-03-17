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

		operationManager=StateManager.getOperationManager()

		self.operationManager=operationManager

		self.parser=QHParser.QHParser(operationManager.getOperatorGenerator())

	def getAllCharacters(self):
		return self.characterDB.keys()

	def queryCharacterDescription(self, character):
		return self.charDescQueryer(character)

	def loadData(self, toTemplateList, toComponentList):
		self.loadTemplate(toTemplateList)
		self.loadComponent(toComponentList)
		self.adjustData()

	def loadComponent(self, toComponentList):
		for filename in toComponentList:
			charDescList=self.parser.loadCharacters(filename)
			for charDesc in charDescList:
				self.saveChar(charDesc)

	def loadTemplate(self, toTemplateList):
		templateDB={}
		for filename in toTemplateList:
			tmpTemplateDB=self.parser.loadTemplates(filename)
			templateDB.update(tmpTemplateDB)

		self.operationManager.setTemplateDB(templateDB)

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

	def adjustData(self):
		operationManager=self.operationManager
		for charName in self.characterDB.keys():
#			print("name: %s"%charName, file=sys.stderr);
			charDesc=self.characterDB.get(charName)

			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				operationManager.rearrangeStructure(structDesc)
#				print("name: %s %s"%(charName, structDesc), file=sys.stderr);

if __name__=='__main__':
	pass

