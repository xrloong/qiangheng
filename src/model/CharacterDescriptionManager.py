#!/usr/bin/env python3

from injector import inject
from injector import singleton
from model.base.CodingConfig import CodingConfig
from model.CodeInfoManager import CodeInfoManager
from .element.CharacterDescription import CharacterDescription
from .element.SubstituteRule import SubstituteRule
from parser import QHParser
import Constant

@singleton
class CharacterDescriptionManager:
	@inject
	def __init__(self, qhparser: QHParser.QHParser,
			codingConfig: CodingConfig,
                        ):
		self.doInitialization(qhparser)
		self.setupCodingConfig(codingConfig)

	def setupCodingConfig(self, codingConfig):
		self.componentFiles = codingConfig.getCommonComponentFileList()
		self.substituteFile = codingConfig.getCommonTemplateFile()

	def doInitialization(self, qhparser):
		self.qhparser = qhparser
		self.characterDB={}

		self.substituteRuleList=[]


	def getAllCharacters(self):
		return self.characterDB.keys()

	def queryCharacterDescription(self, characterName):
		return self.characterDB.get(characterName, None)

	def loadData(self):
		self._loadComponent(self.componentFiles)

	def loadSubstituteRules(self):
		self.substituteRuleList=self._loadSubstituteRules(self.substituteFile)

	def _loadComponent(self, toComponentList):
		for filename in toComponentList:
			charDescList=self.qhparser.loadCharacters(filename)
			for charDesc in charDescList:
				self.saveChar(charDesc)

	def _loadSubstituteRules(self, toSubstituteFile):
		import yaml
		node=yaml.load(open(toSubstituteFile), yaml.SafeLoader)
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

@singleton
class ImCharacterDescriptionManager(CharacterDescriptionManager):
	@inject
	def __init__(self, qhparser: QHParser.QHParser,
			codeInfoManager: CodeInfoManager,
			codingConfig: CodingConfig,
                        ):
		super().__init__(qhparser=qhparser, codingConfig=codingConfig)
		self.doInitialization(qhparser)
		self.codeInfoManager = codeInfoManager
		self.setupCodingConfig(codingConfig)

	def setupCodingConfig(self, codingConfig):
		self.componentFiles = codingConfig.getSpecificComponentFileList()
		self.substituteFile = codingConfig.getSpecificSubstituteFile()
		self.radixFiles = codingConfig.getSpecificRadixFileList()

	def loadRadix(self):
		self.codeInfoManager.loadRadix(self.radixFiles)

		resetRadixNameList=self.codeInfoManager.getResetRadixList()
		self.resetCompoundCharactersToBeRadix(resetRadixNameList)

	def resetCompoundCharactersToBeRadix(self, resetRadixNameList):
		for resetRadixName in resetRadixNameList:
			charDesc=CharacterDescription(resetRadixName)
			self.characterDB[resetRadixName]=charDesc

if __name__=='__main__':
	pass

