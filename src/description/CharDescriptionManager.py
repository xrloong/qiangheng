#!/usr/bin/env python3

from .CharacterDescription import CharacterDescription
#from .StructureDescription import StructureDescription
from .StructureDescription import HangerStructureDescription
from .TemplateDesc import TemplateDesc
from .TemplateDesc import TemplateCondition
from .operator import OperatorManager
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

		imName=imModule.IMInfo.IMName
		self.operationMgr=OperatorManager.OperatorManager(self)

		self.structDescGenerator=structDescGenerator
		self.charDescQueryer=charDescQueryer
		self.charDescRearranger=charDescRearranger
		self.charPropQueryer=charPropQueryer

		self.operatorGenerator=self.operationMgr.getOperatorGenerator()

	def keys(self):
		return self.characterDB.keys()

	def getStructDescGenerator(self):
		return self.structDescGenerator

#	def getStructDescQueryer(self):
#		return self.structDescQueryer

	def getCharDescQueryer(self):
		return self.charDescQueryer

	def getCharPropQueryer(self):
		return self.charPropQueryer

	def loadFromXML(self, filename, fileencoding='utf-8-sig'):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		version=rootNode.get('版本號')
		if version=='0.2':
			self.loadCharDescriptionByParsingXML__0_2(rootNode)

	def loadTemplateFromXML(self, filename, fileencoding='utf-8-sig'):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		version=rootNode.get('版本號')
		if version=='0.2':
			self.loadTemplateByParsingXML__0_2(rootNode)

	def loadCodeInfoFromXML(self, filename, fileencoding='utf-8-sig'):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		version=rootNode.get('版本號')
		if version=='0.2':
			self.loadCodeInfoByParsingXML__0_2(rootNode)


	def loadByParsingXML__0_2(self, rootNode):
		self.loadTemplateByParsingXML__0_2(rootNode)
		self.loadCharDescriptionByParsingXML__0_2(rootNode)
		self.loadCodeInfoByParsingXML__0_2(rootNode)

	def loadCharDescriptionByParsingXML__0_2(self, rootNode):
		# 用於 0.2 版
		structDescGenerator=self.getStructDescGenerator()

		def getDesc_AssembleChar(assembleChar):
			l=[]
			operatorName=assembleChar.get("運算")
			filter_lambda=lambda x: x.tag in ["字根", "組字", "套用範本"]
			targetChildNodes=filter(filter_lambda , list(assembleChar))
			for node in targetChildNodes:
				if node.tag=="字根":
					name=node.get("置換")
					structDesc=structDescGenerator()
					structDesc.setExpandName(name)
					l.append(structDesc)
				elif node.tag=="組字":
					l.append(getDesc_AssembleChar(node))
				else:
					pass

			propDict=assembleChar.attrib
			if operatorName:
				comp=structDescGenerator([operatorName, l])
			else:
				comp=structDescGenerator()

			return comp

		def getDesc_SubCharacter(nodeCharacter):
			assembleCharList=nodeCharacter.findall("組字")
			compList=[]
			for assembleChar in assembleCharList:
				comp=getDesc_AssembleChar(assembleChar)

				comp.setStructureProperties(assembleChar.attrib)

				compList.append(comp)
			return compList

		def getDesc_CompleteCharacterList(nodeCharacter):
			compList=getDesc_SubCharacter(nodeCharacter)
			return compList

		charGroupNode=rootNode.find("字符集")
		targetChildNodes=charGroupNode.findall("字符")
		for node in targetChildNodes:
			compList=getDesc_CompleteCharacterList(node)
			charName=node.get('名稱')
			for comp in compList:
				comp.setExpandName(charName)

			charDesc=self.characterDB.get(charName, None)
			if charDesc==None:
				charDesc=CharacterDescription(charName)
				self.characterDB[charName]=charDesc
			charDesc.setStructureList(compList)
			charDesc.updateProperty(node.attrib)
				
#			self.characterDB[charName]=CharacterDescription(charName, compList)

	def loadTemplateByParsingXML__0_2(self, rootNode):
		# 用於 0.2 版
		structDescGenerator=self.getStructDescGenerator()

		def getDesc_AssembleChar(assembleChar):
			l=[]
			operatorName=assembleChar.get("運算")
			filter_lambda=lambda x: x.tag in ["字根", "組字", "套用範本"]
			targetChildNodes=filter(filter_lambda , list(assembleChar))
			for node in targetChildNodes:
				if node.tag=="字根":
					name=node.get("置換")
					structDesc=structDescGenerator()
					structDesc.setExpandName(name)
					l.append(structDesc)
				elif node.tag=="組字":
					l.append(getDesc_AssembleChar(node))
				else:
					pass

			if operatorName:
				comp=structDescGenerator([operatorName, l])
			else:
				comp=structDescGenerator()

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

		def getDesc_Template_Structure(nodeStructure):
			condition=None

			conditionNode=nodeStructure.find("條件式")
			if conditionNode!=None:
				operator=conditionNode.get('運算')
				operand1=conditionNode.get('運算元一')
				operand2=conditionNode.get('運算元二')
				condition=TemplateCondition([operator, operand1, operand2])
			else:
				condition=TemplateCondition()

			assembleChar=nodeStructure.find("組字")
			comp=getDesc_AssembleChar(assembleChar)
			return [condition, comp]

		def getDesc_Template(nodeTemplate):
			templateName=nodeTemplate.get('名稱')

			parameterNodeList=nodeTemplate.find("參數列")
			parameterNameList=getDesc_ParameterList(parameterNodeList)

			replaceInfoList=[]
			structureNodes=nodeTemplate.findall("組字結構")
			for node in structureNodes:
				replaceInfo=getDesc_Template_Structure(node)
				replaceInfoList.append(replaceInfo)
			[condition, comp]=replaceInfoList[0]

			return TemplateDesc(templateName, replaceInfoList, parameterNameList)

		templateGroupNode=rootNode.find("範本集")
		if None!=templateGroupNode:
			targetChildNodes=templateGroupNode.findall("範本")
			for node in targetChildNodes:
				templateName=node.get('名稱')
				templateDesc=getDesc_Template(node)
				self.templateDB[templateName]=templateDesc
			self.operationMgr.setTemplateDB(self.templateDB)

	def loadCodeInfoByParsingXML__0_2(self, rootNode):
		# 用於 0.2 版
		def getDesc_CodeInfoList(nodeCharacter):
			assembleCharList=nodeCharacter.findall("組字")
			infoDictList=[]
			for assembleChar in assembleCharList:
				infoDict=None
				codeInfo=assembleChar.find("編碼資訊")
				if codeInfo is not None:
					infoDict=codeInfo.attrib

				infoDictList.append(infoDict)
			return infoDictList

		charGroupNode=rootNode.find("字符集")
		targetChildNodes=charGroupNode.findall("字符")
		for node in targetChildNodes:
			charName=node.get('名稱')
			codeInfoDictList=getDesc_CodeInfoList(node)
			self.propertyDB[charName]=codeInfoDictList

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

