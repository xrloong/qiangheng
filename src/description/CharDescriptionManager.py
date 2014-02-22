#!/usr/bin/env python3

from .CharacterDescription import CharacterDescription
#from .StructureDescription import StructureDescription
from .StructureDescription import HangerStructureDescription
#from .TemplateDesc import TemplateDesc
#from .TemplateDesc import TemplateCondition
from .operator import OperatorManager
from parser import QHParser
from xml.etree import ElementTree

class CharDescriptionManager:
	def __init__(self, imModule):
		self.templateDB={}
		self.characterDB={}
		self.propertyDB={}

		def structDescGenerator(structInfo=['龜', []]):
			operatorName, CompList=structInfo
			operator=self.operatorGenerator(operatorName)

			structDesc=HangerStructureDescription(operator, CompList)
			return structDesc

		def charDescRearranger(charDesc):
			return self.operationMgr.rearrangeDesc(charDesc)

		def charDescQueryer(charName):
			charDesc=self.characterDB.get(charName, [])
			return charDesc

		def charPropQueryer(charName):
			codeInfoDictList=self.propertyDB.get(charName, [])
			return codeInfoDictList

		self.parser=QHParser.QHParser(structDescGenerator)

		imName=imModule.IMInfo.IMName
		self.operationMgr=OperatorManager.OperatorManager(self)

		self.structDescGenerator=structDescGenerator
		self.charDescQueryer=charDescQueryer
		self.charDescRearranger=charDescRearranger
		self.charPropQueryer=charPropQueryer

		self.operatorGenerator=self.operationMgr.getOperatorGenerator()

	def keys(self):
		return self.characterDB.keys()

	def getCharDescQueryer(self):
		return self.charDescQueryer

	def getCharPropQueryer(self):
		return self.charPropQueryer

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
		self.operationMgr.setTemplateDB(templateDB)

	def loadCodeInfoFromXML(self, filename, fileencoding='utf-8-sig'):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		propertyDB=self.parser.loadCodeInfoByParsingXML(rootNode)
		self.propertyDB.update(propertyDB)


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

