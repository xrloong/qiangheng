#!/usr/bin/env python3

import sys
from .CharacterDescription import CharacterDescription
from im.gear import OperatorManager
from parser import QHParser
from state import StateManager
from xml.etree import ElementTree
import Constant

class CharDescriptionManager:
	def __init__(self, imModule):
		self.templateDB={}
		self.characterDB={}

		def charDescQueryer(charName):
			charDesc=self.characterDB.get(charName, None)
			return charDesc

		self.operationMgr=OperatorManager.OperatorManager(self)

		self.charDescQueryer=charDescQueryer

		self.parser=QHParser.QHParser(self.operationMgr.getOperatorGenerator())

	def getAllCharacters(self):
		return self.characterDB.keys()

	def queryCharacterDescription(self, character):
		return self.charDescQueryer(character)

	def queryCharacterFrequency(self, character):
		charDesc=self.queryCharacterDescription(character)
		freq=charDesc.getFrequency()
		return freq


	def loadData(self, toTemplateList, toComponentList):
		for filename in toTemplateList:
			self.loadTemplateFromXML(filename, fileencoding=Constant.FILE_ENCODING)

		for filename in toComponentList:
			self.loadFromXML(filename, fileencoding=Constant.FILE_ENCODING)
		self.adjustData()

	def loadFromXML(self, filename, fileencoding=Constant.FILE_ENCODING):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		charDescList=self.parser.loadCharDescriptionByParsingXML(rootNode)
		for charDesc in charDescList:
			charName=charDesc.getName()
			if charName in self.characterDB:
				characterProperty=charDesc.getCharacterProperty()
				origCharDesc=self.characterDB.get(charName)
				origCharDesc.setStructureList(charDesc.getStructureList())
				origCharDesc.updateCharacterProperty(charDesc.getCharacterProperty())
			else:
				characterProperty=charDesc.getCharacterProperty()
				self.characterDB[charName]=charDesc


	def loadTemplateFromXML(self, filename, fileencoding=Constant.FILE_ENCODING):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		templateDB=self.parser.loadTemplateByParsingXML(rootNode)
		self.templateDB.update(templateDB)
		self.operationMgr.setTemplateDB(self.templateDB)

	def adjustData(self):
		charDescRearranger=StateManager.characterDescriptionRearrangerGenerator(self.operationMgr)
		for charName in self.characterDB.keys():
#			print("name: %s"%charName, file=sys.stderr);
			charDesc=self.characterDB.get(charName)
			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				charDescRearranger.rearrangeRecursively(structDesc)
#			print("name: %s %s"%(charName, structDesc), file=sys.stderr);

if __name__=='__main__':
	pass

