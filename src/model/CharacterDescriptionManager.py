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
	def __init__(self, codeInfoManager: CodeInfoManager):
		self.codeInfoManager = codeInfoManager

		self.radixDB={}

	def loadRadix(self, radixFiles):
		self.codeInfoManager.loadRadix(radixFiles)

		resetRadixNameList=self.codeInfoManager.getResetRadixList()
		for resetRadixName in resetRadixNameList:
			radixDesc=CharacterDescription(resetRadixName)
			self.radixDB[resetRadixName]=radixDesc

	def getAllRadixes(self):
		return self.radixDB.keys()

	def queryRadix(self, characterName):
		return self.radixDB.get(characterName, None)

if __name__=='__main__':
	pass

