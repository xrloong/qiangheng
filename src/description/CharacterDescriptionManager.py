#!/usr/bin/env python3

from .CharacterDescription import CharacterDescription
from .operator import OperatorManager
from parser import QHParser
from xml.etree import ElementTree

class CharDescriptionManager:
	def __init__(self, imModule):
		self.templateDB={}
		self.characterDB={}

		def charDescRearranger(charDesc):
			return self.operationMgr.rearrangeDesc(charDesc)

		def charDescQueryer(charName):
			charDesc=self.characterDB.get(charName, [])
			return charDesc

		imName=imModule.IMInfo.IMName
		self.operationMgr=OperatorManager.OperatorManager(self)

		self.charDescQueryer=charDescQueryer
		self.charDescRearranger=charDescRearranger

		self.operatorGenerator=self.operationMgr.getOperatorGenerator()

		self.parser=QHParser.QHParser(self.operationMgr.getOperatorGenerator())

	def getAllCharacters(self):
		return self.characterDB.keys()

	def queryCharacterDescription(self, character):
		return self.charDescQueryer(character)

	def queryCharacterFrequency(self, character):
		charDesc=self.queryCharacterDescription(character)
		freq=charDesc.getFrequency()
		return freq


	def loadData(self, toTemplateList, toComponentList, toCodeList):
		for filename in toTemplateList:
			self.loadTemplateFromXML(filename, fileencoding='utf-8-sig')

		for filename in toComponentList:
			self.loadFromXML(filename, fileencoding='utf-8-sig')
		self.adjustData()

		for filename in toCodeList:
			self.loadCodeInfoFromXML(filename, fileencoding='utf-8-sig')
		self.setAllExpandName()


	def loadFromXML(self, filename, fileencoding='utf-8-sig'):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		charDescList=self.parser.loadCharDescriptionByParsingXML(rootNode)
		for charDesc in charDescList:
			charName=charDesc.getName()
			if charName in self.characterDB:
				origCharDesc=self.characterDB.get(charName, None)
				origCharDesc.setStructureList(charDesc.getStructureList())
				origCharDesc.updateProperty(charDesc.getProperty())
			else:
				self.characterDB[charName]=charDesc


	def loadTemplateFromXML(self, filename, fileencoding='utf-8-sig'):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		templateDB=self.parser.loadTemplateByParsingXML(rootNode)
		self.templateDB.update(templateDB)
		self.operationMgr.setTemplateDB(self.templateDB)

	def loadCodeInfoFromXML(self, filename, fileencoding='utf-8-sig'):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()

		turtleInfoList=self.parser.loadCodeInfoByParsingXML(rootNode)
		for [charName, compList, propDict] in turtleInfoList:
			charDesc=self.characterDB.get(charName, None)
			if charDesc==None:
				charDesc=CharacterDescription(charName)
				self.characterDB[charName]=charDesc
			charDesc.extendStructureList(compList)

	def adjustData(self):
		self.operationMgr.adjustTemplate()

		for charName in self.characterDB.keys():
			charDesc=self.characterDB.get(charName)
			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				self.operationMgr.rearrangeRecursively(structDesc)

	def setAllExpandName(self):
		for charName in self.characterDB.keys():
			charDesc=self.characterDB.get(charName)
			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				structDesc.setExpandName(charName)

if __name__=='__main__':
	pass
