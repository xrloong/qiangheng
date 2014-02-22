#!/usr/bin/env python3

from .CharDesc import CharDesc
from .TemplateDesc import TemplateDesc
from .OperatorManager import OperatorManager
from xml.etree import ElementTree
from character import Operator

class CharDescriptionManager:
	def __init__(self, imModule):
		self.templateDB={}
		self.characterDB={}

		def CharDescGenerator(structInfo=['龜', []]):
			operatorName, CompList=structInfo
			operator=self.operatorGenerator(operatorName)

			if len(operatorName)>1:
				# 暫時以運算名稱的字數來區分是否為範本
				charDesc=CharDesc(operator, CompList)
				return charDesc
			else:
				if operator.isAvailableOperation():
					charDesc=CharDesc(operator, CompList)
				else:
					charDesc=None
			return charDesc

		def charDescRearranger(charDesc):
			return self.operationMgr.rearrangeDesc(charDesc)

		def charDescQueryer(charName):
			charDescList=self.characterDB.get(charName)
			charDesc=charDescList[0]
			return charDesc

		imName=imModule.IMInfo.IMName
		self.operationMgr=imModule.OperatorManager(self)

		self.charDescGenerator=CharDescGenerator
		self.charDescQueryer=charDescQueryer
		self.charDescRearranger=charDescRearranger

		self.operatorGenerator=self.operationMgr.getOperatorGenerator()

	def keys(self):
		return self.characterDB.keys()

	def getCharDescGenerator(self):
		return self.charDescGenerator

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
		charDescGenerator=self.getCharDescGenerator()

		def getDesc_AssembleChar(assembleChar):
			l=[]
			operatorName=assembleChar.get("運算")
			filter_lambda=lambda x: x.tag in ["字根", "組字", "套用範本"]
			targetChildNodes=filter(filter_lambda , list(assembleChar))
			for node in targetChildNodes:
				if node.tag=="字根":
					name=node.get("置換")
					charDesc=charDescGenerator()
					charDesc.setExpandName(name)
					l.append(charDesc)
				elif node.tag=="組字":
					l.append(getDesc_AssembleChar(node))
				else:
					pass

			if operatorName:
				comp=charDescGenerator([operatorName, l])
			else:
				comp=charDescGenerator()

			codeInfo=assembleChar.find("編碼資訊")
			if codeInfo is not None:
				infoDict=codeInfo.attrib
				comp.setPropDict(infoDict)

			return comp

		def getDesc_SubCharacter(nodeCharacter):
			assembleCharList=nodeCharacter.findall("組字")
			compList=[]
			for assembleChar in assembleCharList:
				comp=getDesc_AssembleChar(assembleChar)
				compList.append(comp)
			return compList

		def getDesc_CompleteCharacterList(nodeCharacter):
			compList=getDesc_SubCharacter(nodeCharacter)
			return compList

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
			compList=getDesc_CompleteCharacterList(node)
			comp=compList[0]
			charName=node.get('名稱')
			comp.setExpandName(charName)
			self.characterDB[charName]=compList

	def adjustData(self):
		for charName in self.characterDB.keys():
			srcDescList=self.characterDB.get(charName)
			l=[]
#			srcDesc=self.charDescQueryer(charName)
			for srcDesc in srcDescList:
				charDesc=self.operationMgr.rearrangeRecursively(srcDesc)
				l.append(charDesc)
			self.characterDB[charName]=l

if __name__=='__main__':
	pass

