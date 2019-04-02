#!/usr/bin/env python3

from injector import inject
from injector import singleton
from model.element.CodingConfig import CodingConfig
from model.CodeInfoManager import CodeInfoManager
from .element.CharacterDescription import CharacterDescription
from .element.SubstituteRule import SubstituteRule
from parser import QHParser
import Constant

class SubstituteManager:
	@inject
	def __init__(self, qhparser: QHParser.QHParser):
		self.qhparser = qhparser
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
class CharacterDescriptionManager:
	@inject
	def __init__(self, qhparser: QHParser.QHParser,
			substituteManager: SubstituteManager,
			codingConfig: CodingConfig):
		self.qhparser = qhparser
		self.substituteManager = substituteManager

		self.doInitialization()

		self.codingConfig = codingConfig

	def doInitialization(self):
		self.characterDB={}


	def getAllCharacters(self):
		return self.characterDB.keys()

	def queryCharacterDescription(self, characterName):
		return self.characterDB.get(characterName, None)

	def loadData(self):
		componentFiles = self.codingConfig.getCommonComponentFileList() + self.codingConfig.getSpecificComponentFileList()
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

	def queryChildren(self, charDesc):
		return charDesc.getCompList()

	def queryStructureList(self, charDesc):
		return charDesc.getStructureList()

	def loadSubstituteRules(self):
		substituteFiles = self.codingConfig.getCommonTemplateFileList()
		self.substituteManager.loadSubstituteRules(substituteFiles)

	def getSubstituteRuleList(self):
		return self.substituteManager.getSubstituteRuleList()

@singleton
class RadixManager(CharacterDescriptionManager):
	@inject
	def __init__(self, qhparser: QHParser.QHParser,
			substituteManager: SubstituteManager,
			codeInfoManager: CodeInfoManager,
			codingConfig: CodingConfig):
		super().__init__(qhparser=qhparser, codingConfig=codingConfig)
		self.qhparser = qhparser
		self.substituteManager = substituteManager
		self.codeInfoManager = codeInfoManager

		self.doInitialization()

		self.codingConfig = codingConfig

	def loadRadix(self):
		radixFiles = self.codingConfig.getSpecificRadixFileList()
		self.codeInfoManager.loadRadix(radixFiles)

		resetRadixNameList=self.codeInfoManager.getResetRadixList()
		for resetRadixName in resetRadixNameList:
			charDesc=CharacterDescription(resetRadixName)
			self.characterDB[resetRadixName]=charDesc

	def loadSubstituteRules(self):
		substituteFiles = self.codingConfig.getSpecificSubstituteFileList()
		self.substituteManager.loadSubstituteRules(substituteFiles)

if __name__=='__main__':
	pass

