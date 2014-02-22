#!/usr/bin/env python3

from .CharDesc import CharDesc
from .CharDesc import TemplateCharDesc
from .TemplateDesc import TemplateDesc
from .CharInfo import CharInfo
from .OperatorManager import OperatorManager
from xml.etree import ElementTree

class CharDescriptionManager:
	NoneInfo=CharInfo('[瑲珩預設]', [])
	NoneDesc=CharDesc("", '龜', [], '*', '(龜)', NoneInfo)

	def __init__(self, imModule, CharInfoGenerator):
		# characterDB 放最原始、沒有擴展過的 CharDesc ，也就是從檔案讀出來的資料。
		# descNetwork 放擴展過的，且各個 CharDesc 可能會彼此參照。
		# 但 descNetwork 跟 characterDB 則是完全獨立。
		# 在使用 descNetwork 前，要先呼叫 ConstructDescriptionNetwork()
		# ConstructDescriptionNetwork() 會從 characterDB 建立 descNetwork
		self.templateDB={}
		self.characterDB={}
		self.descNetwork={}

		def CharDescGenerator(charName, structInfo=['龜', [], '(龜)']):
			operator, CompList, expression=structInfo
#			direction=RearrangementManager.computeDirection(operator)
			direction=self.rearrangeMgr.computeDirection(operator)
			tmpCharInfo=CharInfoGenerator(charName, [])
			charDesc=CharDesc(charName, operator, CompList, direction, expression, tmpCharInfo)
			return charDesc

		def emptyCharInfoGenerator():
			return CharInfoGenerator("[瑲珩預設]", [])

		def emptyCharDescGenerator():
			anonymousName=CharDesc.generateNewAnonymousName()
			return CharDescGenerator(anonymousName)

		imName=imModule.IMInfo.IMName
		self.rearrangeMgr=imModule.OperatorManager(self, emptyCharDescGenerator)

		self.charInfoGenerator=CharInfoGenerator
		self.charDescGenerator=CharDescGenerator
		self.emptyCharInfoGenerator=emptyCharInfoGenerator
		self.emptyCharDescGenerator=emptyCharDescGenerator

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

	@staticmethod
	def getNoneInfo():
		return CharDescriptionManager.NoneInfo

	@staticmethod
	def getNoneDescription():
		return CharDescriptionManager.NoneDesc


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
			operator=assembleChar.get("運算")
			filter_lambda=lambda x: x.tag in ["字根", "組字"]
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
			comp=charDescGenerator(anonymousName, [operator, l, '(龜)'])
			return comp

		def getDesc_CharacterX(charName, nodeCharacter):
#			charName=nodeCharacter.get('名稱')
			assembleChar=nodeCharacter.find("組字")
			if assembleChar==None:
				return None

			infoList=[]
			charInfo=nodeCharacter.find("編碼資訊")
			if charInfo is not None:
				infoExpr=charInfo.get('資訊表示式')
				infoExtra=charInfo.get('補充資訊')
				if infoExpr: infoList.append(infoExpr)
				if infoExtra: infoList.append(infoExtra)
				
			chInfo=charInfoGenerator(charName, infoList)

			comp=getDesc_AssembleChar(assembleChar)
			comp.setName(charName)
			comp.setChInfo(chInfo)

			return comp

		def getDesc_Character(nodeCharacter):
			applyTemplate=nodeCharacter.find("套用範本")
			charName=nodeCharacter.get('名稱')

			templateCharDesc=None
			if applyTemplate!=None:
				argumentNodeList=applyTemplate.find("引數列")
				argumentNameList=getDesc_ArgumentList(argumentNodeList)

				templateName=applyTemplate.get("範本名稱")
				templateCharDesc=TemplateCharDesc(charName, templateName, argumentNameList)

				comp=getDesc_CharacterX(charName, nodeCharacter)
#				comp=getDesc_CharacterX(charName, applyTemplate)
				if comp!=None:
					templateCharDesc.setCharDesc(comp)

				comp=templateCharDesc
			else:
				comp=getDesc_CharacterX(charName, nodeCharacter)

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

			comp=getDesc_AssembleChar(assembleChar)
			comp.setName(templateName)
#			comp.setChInfo(chInfo)
			return TemplateDesc(templateName, comp, parameterNameList)

		templateGroupNode=rootNode.find("範本集")
		if None!=templateGroupNode:
			targetChildNodes=templateGroupNode.findall("範本")
			for node in targetChildNodes:
				templateDesc=getDesc_Template(node)
				self.templateDB[templateDesc.getName()]=templateDesc

		charGroupNode=rootNode.find("字符集")
		targetChildNodes=charGroupNode.findall("字符")
		for node in targetChildNodes:
			comp=getDesc_Character(node)
			self.characterDB[comp.getName()]=comp

	def ConstructDescriptionNetwork(self):
#		# dirty Work
#		# 需要先處理的 List
#		dirtySpecialList=["彳", "亍", "亠", "[衣下]", ]
#		for charName in dirtySpecialList+list(self.characterDB.keys()):

#		for templateName in self.templateDB.keys():
#			self.templateDB.get(templateName)

		charInfoGenerator=self.getCharInfoGenerator()
		for charName in self.characterDB.keys():
			charDesc=self.characterDB.get(charName)
			if charDesc.isTemplate():
				templateDesc=self.templateDB.get(charDesc.getTemplateName())
				charDesc.setTemplateDesc(templateDesc)
				charDesc=charDesc.getCharDesc()
				charDesc.setName(charName)
				chInfo=charInfoGenerator(charName, [])
				charDesc.setChInfo(chInfo)

				self.characterDB[charName]=charDesc

		for charName in self.characterDB.keys():
			if charName not in self.descNetwork:
				charDesc=self.charDescGenerator(charName)
				self.expandCharDescInNetwork(charDesc, self.characterDB.get(charName))
				self.descNetwork[charName]=charDesc

	def expandCharDescInNetwork(self, dstDesc, srcDesc):
		# 擴展 dstDesc
		# dstDesc 會被改變，而非產生新的 CharDesc
		dstDesc.copyInfoWithoutCompListFrom(srcDesc)

		compList=[]
		for childSrcDesc in srcDesc.getCompList():
			if childSrcDesc.isAnonymous():
				# 若是為匿名結構，無法用名字查出結構，直接複製
				anonymousName=CharDesc.generateNewAnonymousName()
				childDstDesc=self.charDescGenerator(anonymousName)
				self.expandCharDescInNetwork(childDstDesc, childSrcDesc)

			else:
				if childSrcDesc.name in self.descNetwork:
					childDstDesc=self.descNetwork.get(childSrcDesc.name)
				else:
					expandChildSrcDesc=self.characterDB.get(childSrcDesc.name)

					childDstDesc=self.charDescGenerator(expandChildSrcDesc.name)

					self.expandCharDescInNetwork(childDstDesc, expandChildSrcDesc)
					self.descNetwork[childDstDesc.name]=childDstDesc

			compList.append(childDstDesc)
		dstDesc.setCompList(compList)

		self.rearrangeMgr.rearrangeDesc(dstDesc)

	def getExpandDescriptionByNameInNetwork(self, charName):
		return self.descNetwork.get(charName, None)

	@staticmethod
	def setCharTree(charDesc):
		"""設定某一個字符所包含的部件的碼"""

		chInfo=charDesc.getChInfo()
		if not chInfo.isToSetTree():
			return

		radixList=charDesc.getCompList()
		for tmpdesc in radixList:
			CharDescriptionManager.setCharTree(tmpdesc)

		infoList=[x.getChInfo() for x in radixList]
		chInfo.setByComps(infoList, charDesc.getDirection())

if __name__=='__main__':
	pass

