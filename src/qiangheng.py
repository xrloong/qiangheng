#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xml.etree import ElementTree
from im import IMMgr
from description import CharDescriptionManager
from hanzi import HanZiNetwork

from state import StateManager

from optparse import OptionParser

class QiangHeng:
	def __init__(self, options):
		configFile=options.config_file
		xml_format=options.xml_format

		configList=self.readConfig(configFile)
		[imProp, toTemplateList, toComponentList, toCodeList]=configList
		imModule=IMMgr.IMMgr.getIMModule(imProp)

		self.initManager(imModule)

		self.descMgr.loadData(toTemplateList, toComponentList, toCodeList)

		self.constructDescriptionNetwork()

		if xml_format:
			imInfo=imModule.IMInfo()
			self.toXML(imInfo)
		else:
			self.toTXT()

	def initManager(self, imModule):
		self.descMgr=CharDescriptionManager.CharDescriptionManager(imModule)

		self.hanziNetwork=HanZiNetwork.HanZiNetwork()

		StateManager.setIMModule(imModule)

	def readConfig(self, configFile):
		f=open(configFile, encoding='utf-8-sig')
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()

		configNode=rootNode.find('設定')
		imNode=configNode.find('輸入法')
		imProp=imNode.attrib

		configFileNode=rootNode.find('設定檔')
		templateNodeList=configFileNode.findall('範本')
		componentNodeList=configFileNode.findall('部件')
		radixNodeList=configFileNode.findall('字根')

		rootDirPrefix=configFileNode.get('資料目錄')

		toComponentList=[rootDirPrefix+node.get('檔案') for node in componentNodeList]
		toTemplateList=[rootDirPrefix+node.get('檔案') for node in templateNodeList]
		toCodeList=[rootDirPrefix+node.get('檔案') for node in radixNodeList]


		return [imProp, toTemplateList, toComponentList, toCodeList]


	def constructDescriptionNetwork(self):
		charNameList=self.getAllCharacters()
		hanziNetwork=self.hanziNetwork
		sortedNameList=sorted(charNameList)

		for charName in sortedNameList:
			hanziNetwork.addNode(charName)

		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)
			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				self.recursivelyAddNode(structDesc)

		for charName in sortedNameList:
			charDesc=self.queryDescription(charName)
			structDescList=charDesc.getStructureList()
			for structDesc in structDescList:
				if structDesc.isTurtle():
					hanziNetwork.appendTurtleStruct(structDesc)
				else:
					self.recursivelyAddLink(structDesc)


	def recursivelyAddNode(self, srcDesc):
		self.hanziNetwork.addOrFindNodeByCharDesc(srcDesc)

		for childSrcDesc in srcDesc.getCompList():
			self.recursivelyAddNode(childSrcDesc)

	def recursivelyAddLink(self, structDesc):
		operator=structDesc.getOperator()
		childDescList=structDesc.getCompList()

		self.hanziNetwork.addLink(structDesc, operator, childDescList)

		for childSrcDesc in structDesc.getCompList():
			self.recursivelyAddLink(childSrcDesc)

	def toXML(self, imInfo):
		keyMaps=imInfo.getKeyMaps()

		rootNode=ElementTree.Element("輸入法")

		# 名稱
		nameNode=ElementTree.SubElement(rootNode, "輸入法名稱",
			attrib={
				"EN":imInfo.getName('en'),
				"TW":imInfo.getName('tw'),
				"CN":imInfo.getName('cn'),
				"HK":imInfo.getName('hk'),
#				"SG":imInfo.getName('sg'),
				})

		# 屬性
		propertyNode=ElementTree.SubElement(rootNode, "屬性",
			attrib={
				"最大按鍵數":"%s"%imInfo.getMaxKeyLength()
				})

		# 按鍵與顯示的對照表
		keyMapsNode=ElementTree.SubElement(rootNode, "按鍵對應集")
		for key, disp in keyMaps:
			ElementTree.SubElement(keyMapsNode, "按鍵對應", attrib={"按鍵":key, "顯示":disp})

		# 對照表
		charGroup=ElementTree.SubElement(rootNode, "對應集")
		targetCharList=self.getAllCharacters()
		cm=self.genIMMapping(targetCharList)
		for x in sorted(cm):
			attrib={"按鍵序列":x[0], "字符":x[1], "頻率":x[2], "類型":x[3]}
			ElementTree.SubElement(charGroup, "對應", attrib)
		xmlNode=ElementTree.ElementTree(rootNode)
		ElementTree.dump(xmlNode)
#		xmlNode.write(sys.stdout)

	def toTXT(self):
		targetCharList=self.getAllCharacters()
		cm=self.genIMMapping(targetCharList)
		table="\n".join(sorted(map(lambda x : '{0}\t{1}'.format(*x), cm)))
		print(table)

	def genIMMapping(self, targetCharList):

		table=[]
		for charName in sorted(targetCharList):
#			print("<-- %s -->"%charName)
			codePropList=self.hanziNetwork.getCodePropertiesList(charName)
			charDesc=self.queryDescription(charName)
			freq=charDesc.getFrequency()
			for code, type in codePropList:
				table.append([code, charName, freq, type])
		return table

	def getAllCharacters(self):
		return self.descMgr.getAllCharacters()

	def queryDescription(self, characterName):
		return self.descMgr.queryCharacterDescription(characterName)

oparser = OptionParser()
oparser.add_option("-c", "--config", dest="config_file", help="輸入法設定檔", default="qhdata/config/default.xml")
oparser.add_option("--xml", action="store_true", dest="xml_format")
oparser.add_option("--text", action="store_false", dest="xml_format")
(options, args) = oparser.parse_args()

qiangheng=QiangHeng(options)

