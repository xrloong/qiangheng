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

	def keys(self):
		return self.characterDB.keys()

	def getCharDescQueryer(self):
		return self.charDescQueryer

	def loadFromXML(self, filename, fileencoding='utf-8-sig'):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		nodeInfoList=self.parser.loadCharDescriptionByParsingXML(rootNode)
		for [charName, compList, propDict] in nodeInfoList:
			charDesc=self.characterDB.get(charName, None)
			if charDesc==None:
				charDesc=CharacterDescription(charName)
				self.characterDB[charName]=charDesc
			charDesc.setStructureList(compList)
			charDesc.updateProperty(propDict)


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
#			charDesc.updateProperty(propDict)

	def adjustData(self):
		self.operationMgr.adjustTemplate()

		for charName in self.characterDB.keys():
			charDesc=self.characterDB.get(charName)
			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				backupCodeType=structDesc.getCodeType()
				self.operationMgr.rearrangeRecursively(structDesc)
				structDesc.setCodeType(backupCodeType)

if __name__=='__main__':
	pass

