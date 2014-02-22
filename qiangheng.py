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

		self.getDescDBFromXML(toTemplateList, toComponentList, toCodeList)

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

		codingMethod=configNode.find('拆碼方式')
		quantityStr=codingMethod.get('數量')
		if quantityStr=='無':
			quantity=StateManager.STATE_QUANTITY_NONE
		elif quantityStr=='一':
			quantity=StateManager.STATE_QUANTITY_FIRST
		elif quantityStr=='全':
			quantity=StateManager.STATE_QUANTITY_ALL
		else:
			quantity=StateManager.STATE_QUANTITY_NONE
		StateManager.setQuantity(quantity)

		configFileNode=rootNode.find('設定檔')
		templateNodeList=configFileNode.findall('範本')
		componentNodeList=configFileNode.findall('部件')
		radixNodeList=configFileNode.findall('字根')

		rootDirPrefix=configFileNode.get('資料目錄')

		toComponentList=[rootDirPrefix+node.get('檔案') for node in componentNodeList]
		toTemplateList=[rootDirPrefix+node.get('檔案') for node in templateNodeList]
		toCodeList=[rootDirPrefix+node.get('檔案') for node in radixNodeList]


		return [imProp, toTemplateList, toComponentList, toCodeList]


	def readDesc(self, dirQHDataRoot, configFile):
		rootDirPrefix=dirQHDataRoot+"/"
		configFile=rootDirPrefix+configFile

		f=open(configFile, encoding='utf-8-sig')
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()

		configNode=rootNode.find('設定檔')
		templateNodeList=configNode.findall('範本')
		componentNodeList=configNode.findall('部件')
		radixNodeList=configNode.findall('字根')

		toComponentList=[rootDirPrefix+node.get('檔案') for node in componentNodeList]

		toTemplateList=[rootDirPrefix+node.get('檔案') for node in templateNodeList]

		toCodeList=[rootDirPrefix+node.get('檔案') for node in radixNodeList]

		self.getDescDBFromXML(toTemplateList, toComponentList, toCodeList)

	def constructDescriptionNetwork(self):
		charNameList=self.descMgr.keys()
		hanziNetwork=self.hanziNetwork
		structDescQueryer=self.descMgr.getStructDescQueryer()
		sortedNameList=sorted(charNameList)

		for charName in sortedNameList:
			hanziNetwork.addNode(charName)

		for charName in sortedNameList:
			structDescList=structDescQueryer(charName)
			for structDesc in structDescList:
				self.recursivelyAddNode(structDesc)

		for charName in sortedNameList:
			structDescList=structDescQueryer(charName)
			for structDesc in structDescList:
				self.recursivelyAddLink(structDesc)

		charPropQueryer=self.descMgr.getCharPropQueryer()
		for charName in sortedNameList:
			structDescList=structDescQueryer(charName)
			srcPropList=charPropQueryer(charName)
			for structDesc in structDescList:
				for srcProp in srcPropList:
					hanziNetwork.appendNodeInfo(structDesc, srcProp)

	def recursivelyAddNode(self, srcDesc):
		self.hanziNetwork.addOrFindNodeByCharDesc(srcDesc)

		for childSrcDesc in srcDesc.getCompList():
			self.recursivelyAddNode(childSrcDesc)

	def recursivelyAddLink(self, srcDesc):
		operator=srcDesc.getOperator()
		childDescList=srcDesc.getCompList()

		self.hanziNetwork.addLink(srcDesc, operator, childDescList)

		for childSrcDesc in srcDesc.getCompList():
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
		targetCharList=self.descMgr.keys()
		cm=self.genIMMapping(targetCharList)
		for x in sorted(cm):
			ElementTree.SubElement(charGroup, "對應", attrib={"按鍵序列":x[0], "字符":x[1]})
		xmlNode=ElementTree.ElementTree(rootNode)
		ElementTree.dump(xmlNode)
#		xmlNode.write(sys.stdout)

	def toTXT(self):
		targetCharList=self.descMgr.keys()
		cm=self.genIMMapping(targetCharList)
		table="\n".join(sorted(map(lambda x : '{0}\t{1}'.format(*x), cm)))
		print(table)

	def getDescDBFromXML(self, toTemplateList, toComponentList, toCodeList):
		for filename in toTemplateList:
			self.descMgr.loadTemplateFromXML(filename, fileencoding='utf-8-sig')

		for filename in toComponentList:
			self.descMgr.loadFromXML(filename, fileencoding='utf-8-sig')
		self.descMgr.adjustData()

		for filename in toCodeList:
			self.descMgr.loadCodeInfoFromXML(filename, fileencoding='utf-8-sig')

	def genIMMapping(self, targetCharList):
		table=[]
		for charName in sorted(targetCharList):
#			print("<-- %s -->"%charName)
			codeList=self.hanziNetwork.getCodeList(charName)
			for code in codeList:
				table.append([code, charName])
		return table

oparser = OptionParser()
oparser.add_option("-c", "--config", dest="config_file", help="輸入法設定檔", default="qhdata/config/default.xml")
oparser.add_option("--xml", action="store_true", dest="xml_format")
oparser.add_option("--text", action="store_false", dest="xml_format")
(options, args) = oparser.parse_args()

qiangheng=QiangHeng(options)

