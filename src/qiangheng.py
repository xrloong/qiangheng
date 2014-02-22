#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from xml.etree import ElementTree
from im import IMMgr
from description import CharacterDescriptionManager
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

		StateManager.setIMModule(imModule)

		self.descMgr=CharacterDescriptionManager.CharDescriptionManager(imModule)
		self.descMgr.loadData(toTemplateList, toComponentList, toCodeList)

		StateManager.setRadixManager(self.descMgr.radixManager)

		self.hanziNetwork=HanZiNetwork.HanZiNetwork.construct(self.descMgr)

		codeMappingInfoList=self.genIMMapping()
		if xml_format:
			imInfo=imModule.IMInfo()
			self.toXML(imInfo, codeMappingInfoList)
		else:
			self.toTXT(codeMappingInfoList)

	def readConfig(self, configFileName):
		f=open(configFileName, encoding='utf-8-sig')
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()

		configNode=rootNode.find('設定')
		imNode=configNode.find('輸入法')
		imProp=imNode.attrib

#		configFileNode=rootNode.find('設定檔')
		[toTemplateList, toComponentList, toCodeList]=self.getConfigFiles(configFileName)

		return [imProp, toTemplateList, toComponentList, toCodeList]

	def getConfigFiles(self, configFileName):
		f=open(configFileName, encoding='utf-8-sig')
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()
		configFileNode=rootNode.find('設定檔')

		importNodeList=configFileNode.findall('匯入')

		templateNodeList=configFileNode.findall('範本')
		componentNodeList=configFileNode.findall('部件')
		radixNodeList=configFileNode.findall('字根')

		rootDirPrefix=configFileNode.get('資料目錄')

		toComponentList=[]
		toTemplateList=[]
		toCodeList=[]

		for node in importNodeList:
			fileName=rootDirPrefix+node.get('檔案')
			[tmpToTemplateList, tmpToComponentList, tmpToCodeList]= \
				self.getConfigFiles(fileName)
			toComponentList.extend(tmpToComponentList)
			toTemplateList.extend(tmpToTemplateList)
			toCodeList.extend(tmpToCodeList)

		tmpToComponentList=[rootDirPrefix+node.get('檔案') for node in componentNodeList]
		tmpToTemplateList=[rootDirPrefix+node.get('檔案') for node in templateNodeList]
		tmpToCodeList=[rootDirPrefix+node.get('檔案') for node in radixNodeList]

		toComponentList.extend(tmpToComponentList)
		toTemplateList.extend(tmpToTemplateList)
		toCodeList.extend(tmpToCodeList)

		return [toTemplateList, toComponentList, toCodeList]


	def toXML(self, imInfo, codeMappingInfoList):
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
		for x in sorted(codeMappingInfoList, key=lambda y: y.getKey()):
			attrib={"按鍵序列":x.getCode(), "字符":x.getName(), "頻率":x.getFrequency(), "類型":x.getVariance()}
			ElementTree.SubElement(charGroup, "對應", attrib)
		xmlNode=ElementTree.ElementTree(rootNode)
		ElementTree.dump(xmlNode)
#		xmlNode.write(sys.stdout)

	def toTXT(self, codeMappingInfoList):
		table="\n".join(sorted(map(lambda x : '{0}\t{1}'.format(*x.getKey()), codeMappingInfoList)))
		print(table)

	def genIMMapping(self):
		characterFilter=lambda charName: (len(charName)==1)
		targetCharacterList=filter(characterFilter, self.descMgr.getAllCharacters())
		table=[]
		for charName in sorted(targetCharacterList):
#			print("<-- %s -->"%charName, sys.stderr)
			characterInfo=self.hanziNetwork.getCharacterInfo(charName)
			table.extend(characterInfo.getCodeMappingInfoList())
		return table

oparser = OptionParser()
oparser.add_option("-c", "--config", dest="config_file", help="輸入法設定檔", default="qhdata/config/default.xml")
oparser.add_option("--xml", action="store_true", dest="xml_format")
oparser.add_option("--text", action="store_false", dest="xml_format")
(options, args) = oparser.parse_args()

qiangheng=QiangHeng(options)

