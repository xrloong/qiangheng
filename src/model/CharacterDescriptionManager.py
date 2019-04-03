#!/usr/bin/env python3

from injector import inject
from injector import singleton
from model.CodeInfoManager import CodeInfoManager
from .element.CharacterDescription import CharacterDescription
from .element.SubstituteRule import SubstituteRule
from parser import QHParser
import Constant

class SubstituteManager:
	@inject
	def __init__(self):
		self.substituteRuleList=[]

	def loadSubstituteRules(self, substituteFiles):
		totalSubstituteRuleList=[]
		for filename in substituteFiles:
			substituteRuleList=self._loadSubstituteRules(filename)
			totalSubstituteRuleList.extend(substituteRuleList)
		self.substituteRuleList=totalSubstituteRuleList

	def _loadSubstituteRules(self, substituteFile):
		import yaml
		node=yaml.load(open(substituteFile), yaml.SafeLoader)
		ruleSetNode=node.get(Constant.TAG_RULE_SET)

		if not ruleSetNode:
			return []

		substitueRuleList=[]
		for node in ruleSetNode:
			matchPattern=node.get(Constant.TAG_MATCH)
			replacePattern=node.get(Constant.TAG_SUBSTITUTE)

			substitueRule=SubstituteRule(matchPattern, replacePattern)
			substitueRuleList.append(substitueRule)

		return substitueRuleList

	def getSubstituteRuleList(self):
		return self.substituteRuleList

@singleton
class CompositionManager:
	@inject
	def __init__(self, qhparser: QHParser.QHParser):
		self.qhparser = qhparser

		self.characterDB={}


	def getAllCharacters(self):
		return self.characterDB.keys()

	def queryCharacterDescription(self, characterName):
		return self.characterDB.get(characterName, None)

	def loadComponents(self, componentFiles):
		self._loadComponent(componentFiles)

	def _loadComponent(self, toComponentList):
		for filename in toComponentList:
			charDescList=self.qhparser.loadCharacters(filename)
			for charDesc in charDescList:
				self.saveChar(charDesc)

	def saveChar(self, charDesc):
		charName=charDesc.getName()

		if charName in self.characterDB:
			origCharDesc=self.characterDB.get(charName)
			origCharDesc.setStructureList(charDesc.getStructureList())
		else:
			self.characterDB[charName]=charDesc

@singleton
class RadixManager:
	@inject
	def __init__(self, codeInfoManager: CodeInfoManager):
		self.codeInfoManager = codeInfoManager

		self.characterDB={}

	def loadRadix(self, radixFiles):
		self.codeInfoManager.loadRadix(radixFiles)

		resetRadixNameList=self.codeInfoManager.getResetRadixList()
		for resetRadixName in resetRadixNameList:
			charDesc=CharacterDescription(resetRadixName)
			self.characterDB[resetRadixName]=charDesc

	def getAllCharacters(self):
		return self.characterDB.keys()

	def queryCharacterDescription(self, characterName):
		return self.characterDB.get(characterName, None)

if __name__=='__main__':
	pass

