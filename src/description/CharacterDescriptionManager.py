#!/usr/bin/env python3

import sys
from .CharacterDescription import CharacterDescription
from parser import QHParser
import Constant
from gear import TreeRegExp
import yaml

class CharacterDescriptionManager:
	def __init__(self):
		self.characterDB={}

		def charDescQueryer(charName):
			charDesc=self.characterDB.get(charName, None)
			return charDesc

		self.charDescQueryer=charDescQueryer
		self.substitutePatternList=[]

	def getAllCharacters(self):
		return self.characterDB.keys()

	def queryCharacterDescription(self, character):
		return self.charDescQueryer(character)

	def loadData(self, toComponentList):
		self.loadComponent(toComponentList)

	def loadComponent(self, toComponentList):
		parser=QHParser.QHParser()
		for filename in toComponentList:
			charDescList=parser.loadCharacters(filename)
			for charDesc in charDescList:
				self.saveChar(charDesc)

	def loadSubstituteRules(self, toSubstituteFile):
		self.substitutePatternList=self._loadSubstituteRules(toSubstituteFile)

	def _loadSubstituteRules(self, toSubstituteFile):
		node=yaml.load(open(toSubstituteFile), yaml.CLoader)
		ruleSetNode=node.get(Constant.TAG_RULE_SET)

		if not ruleSetNode:
			return []

		templatePatternList=[]
		for node in ruleSetNode:
			templateName=node.get(Constant.TAG_NAME)
			matchPattern=node.get(Constant.TAG_MATCH)
			replacePattern=node.get(Constant.TAG_SUBSTITUTE)
			tre=TreeRegExp.compile(matchPattern)

			templatePatternList.append([templateName, tre, replacePattern])

		return templatePatternList

	def getSubstitutePatternList(self):
		return self.substitutePatternList

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

	def resetCompoundCharactersToBeRadix(self, resetRadixNameList):
		for resetRadixName in resetRadixNameList:
			charDesc=CharacterDescription(resetRadixName)
			self.characterDB[resetRadixName]=charDesc

if __name__=='__main__':
	pass

