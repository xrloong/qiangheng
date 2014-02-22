#!/usr/bin/env python3

from .CharDesc import CharDesc
from .CharDesc import TemplateCharDesc
from .TemplateDesc import TemplateDesc
from .CharInfo import CharInfo
from .OperatorManager import OperatorManager
from xml.etree import ElementTree
from character import Operator

class CharDescriptionManager:
	def __init__(self, imModule, CharInfoGenerator):
		self.templateDB={}
		self.characterDB={}

		def CharDescGenerator(charName, structInfo=['龜', []]):
			operatorName, CompList=structInfo
			operator=self.operatorGenerator(operatorName)

			if len(operatorName)>1:
				# 暫時以運算名稱的字數來區分是否為範本
				charDesc=TemplateCharDesc(charName, operator, CompList)
				return charDesc
			else:
				if operator.isAvailableOperation():
					charDesc=CharDesc(charName, operator, CompList)
				else:
					charDesc=None
			return charDesc

		def emptyCharInfoGenerator():
			return CharInfoGenerator({})

		def emptyCharDescGenerator():
			anonymousName=CharDesc.generateNewAnonymousName()
			return CharDescGenerator(anonymousName)


		def charDescRearranger(charDesc):
			return self.operationMgr.rearrangeDesc(charDesc)

		def charDescQueryer(charName):
			charDesc=self.characterDB.get(charName)
			return charDesc

		imName=imModule.IMInfo.IMName
		self.operationMgr=imModule.OperatorManager(self, emptyCharDescGenerator)

		self.charInfoGenerator=CharInfoGenerator
		self.charDescGenerator=CharDescGenerator
		self.emptyCharInfoGenerator=emptyCharInfoGenerator
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.charDescQueryer=charDescQueryer
		self.charDescRearranger=charDescRearranger

		self.operatorGenerator=self.operationMgr.getOperatorGenerator()

	def keys(self):
		return self.characterDB.keys()

	def getCharInfoGenerator(self):
		return self.charInfoGenerator

	def getCharDescGenerator(self):
		return self.charDescGenerator

	def getEmptyCharInfoGenerator(self):
		return self.emptyCharInfoGenerator

	def getEmptyCharDescGenerator(self):
		return self.emptyCharDescGenerator

	def getCharDescQueryer(self):
		return self.charDescQueryer

	def loadFromXML(self, filename, fileencoding='utf-8-sig'):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		version=rootNode.get('版本號')
		if version=='0.1':
			self.loadByParsingXML__0_1(rootNode)


	def loadByParsingXML__0_1(self, rootNode):
		# 用於 0.1 版
		charInfoGenerator=self.getCharInfoGenerator()
		emptyCharInfoGenerator=self.getEmptyCharInfoGenerator()
		charDescGenerator=self.getCharDescGenerator()
		emptyCharDescGenerator=self.getEmptyCharDescGenerator()

		def getDesc_AssembleChar(assembleChar):
			l=[]
			operatorName=assembleChar.get("運算")
			filter_lambda=lambda x: x.tag in ["字根", "組字", "套用範本"]
			targetChildNodes=filter(filter_lambda , list(assembleChar))
			for node in targetChildNodes:
				if node.tag=="字根":
					name=node.get("名稱")
					l.append(charDescGenerator(name))
				elif node.tag=="組字":
					l.append(getDesc_AssembleChar(node))
				else:
					pass

			anonymousName=CharDesc.generateNewAnonymousName()
			comp=charDescGenerator(anonymousName, [operatorName, l])

			return comp

		def getDesc_SubCharacter(nodeCharacter):
			assembleChar=nodeCharacter.find("組字")
			if assembleChar==None:
				return None

			infoList=[]
			infoDict={}
			charInfo=nodeCharacter.find("編碼資訊")
			if charInfo is not None:
				infoDict=charInfo.attrib
				
			chInfo=charInfoGenerator(infoDict)

			comp=getDesc_AssembleChar(assembleChar)
			comp.setChInfo(chInfo)

			return comp

		def getDesc_CompleteCharacter(nodeCharacter):
			comp=getDesc_SubCharacter(nodeCharacter)
			return comp

		def getDesc_ArgumentList(nodeArgument):
			argumentList=[]
			targetArgumentNodes=nodeArgument.findall("引數")
			for node in targetArgumentNodes:
				charName=node.get('名稱')
				argumentList.append(charName)
			return argumentList

		def getDesc_ParameterList(nodeParameter):
			parameterList=[]
			targetParameterNodes=nodeParameter.findall("參數")
			for node in targetParameterNodes:
				charName=node.get('名稱')
				parameterList.append(charName)
			return parameterList

		def getDesc_Template(nodeTemplate):
			templateName=nodeTemplate.get('名稱')
			parameterNodeList=nodeTemplate.find("參數列")
			assembleChar=nodeTemplate.find("組字")

			parameterNameList=getDesc_ParameterList(parameterNodeList)

			chInfo=emptyCharInfoGenerator()
			comp=getDesc_AssembleChar(assembleChar)
			comp.setName(templateName)
			return TemplateDesc(templateName, comp, parameterNameList)

		templateGroupNode=rootNode.find("範本集")
		if None!=templateGroupNode:
			targetChildNodes=templateGroupNode.findall("範本")
			for node in targetChildNodes:
				templateName=node.get('名稱')
				templateDesc=getDesc_Template(node)
				self.templateDB[templateName]=templateDesc
			self.operationMgr.setTemplateDB(self.templateDB)

		charGroupNode=rootNode.find("字符集")
		targetChildNodes=charGroupNode.findall("字符")
		for node in targetChildNodes:
			comp=getDesc_CompleteCharacter(node)
			charName=node.get('名稱')
			comp.setName(charName)
			comp.setAnonymous(charName.count("瑲珩匿名")>0)
			self.characterDB[charName]=comp

	def adjustData(self):
		for charName in self.characterDB.keys():
			srcDesc=self.characterDB.get(charName)
			charDesc=self.operationMgr.rearrangeRecursively(srcDesc)
			self.characterDB[charName]=charDesc

if __name__=='__main__':
	pass

