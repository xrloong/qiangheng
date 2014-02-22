#!/usr/bin/env python3

import sys
from .CharacterDescription import CharacterDescription
from parser import QHParser
from xml.etree import ElementTree
import Constant
from im.base import StructureRearranger

class CharDescriptionManager:
	def __init__(self):
		self.templateDB={}
		self.characterDB={}

		def charDescQueryer(charName):
			charDesc=self.characterDB.get(charName, None)
			return charDesc

		self.charDescQueryer=charDescQueryer

		self.structurRearranger=StructureRearranger()

		self.parser=QHParser.QHParser(self.structurRearranger.getOperatorGenerator())

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

		self.structurRearranger.setTemplateDB(self.templateDB)

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

	def adjustData(self):
		for charName in self.characterDB.keys():
#			print("name: %s"%charName, file=sys.stderr);
			charDesc=self.characterDB.get(charName)
			self.structurRearranger.rearrangeOn(charDesc)
#			print("name: %s %s"%(charName, structDesc), file=sys.stderr);

if __name__=='__main__':
	pass

