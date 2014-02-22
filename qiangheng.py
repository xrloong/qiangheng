#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xml.etree import ElementTree
from im.IMMgr import IMMgr
from character.CharDescriptionManager import CharDescriptionManager
from character.HanZiNetwork import HanZiNetwork
#from character.OperatorManager import OperatorManager

from optparse import OptionParser

class QiangHeng:
	def __init__(self, options):
		choice=options.imname
		xml_format=options.xml_format

		[imModule, dirIM]=self.getIMInfo(choice)

		self.initManager(imModule)

		dirCharInfoRoot=options.dir_charinfo
		self.readDesc(dirCharInfoRoot, dirIM)

		self.constructDescriptionNetwork()

		if xml_format:
			imInfo=imModule.IMInfo()
			self.toXML(imInfo)
		else:
			self.toTXT()

	def initManager(self, imModule):
		ciGenerator=imModule.CharInfoGenerator
		self.descMgr=CharDescriptionManager(imModule, ciGenerator)

		emptyCharInfoGenerator=self.descMgr.getEmptyCharInfoGenerator()
		charDescQueryer=self.descMgr.getCharDescQueryer()
		self.hanziNetwork=HanZiNetwork(emptyCharInfoGenerator, charDescQueryer)

#		self.operationMgr=imModule.OperatorManager(self, emptyCharDescGenerator)

	def readDesc(self, dirCharInfoRoot, dirIM):
		filenamelist=[
#				'CJK.txt',
				'CJK.xml',
		]

		dirCharInfo=dirCharInfoRoot + "/"
		tmpfname=filenamelist[0]
		pathlist=[
				dirCharInfo+'main/'+tmpfname,
				dirCharInfo+dirIM+tmpfname,
				]

		self.getDescDBFromXML(pathlist)

	def constructDescriptionNetwork(self):
		self.hanziNetwork.constructHanZiNetwork(self.descMgr.keys())

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

	def getDescDBFromXML(self, filenamelist):
		for filename in filenamelist:
			self.descMgr.loadFromXML(filename, fileencoding='utf-8-sig')

	def genIMMapping(self, targetCharList):
		table=[]
		for charName in targetCharList:
			code=self.hanziNetwork.getCode(charName)
			if code:
				table.append([code, charName])
			else:
				pass
		return table

	def getIMInfo(self, imName):
		if imName in ['倉', '倉頡', '倉頡輸入法', 'cangjie', 'cj',]:
			imDirPath='cj/'
			imName='倉頡'
		elif imName in ['行', '行列', '行列輸入法', 'array', 'ar',]:
			imDirPath='ar/'
			imName='行列'
		elif imName in ['易', '大易', '大易輸入法', 'dayi', 'dy',]:
			imDirPath='dy/'
			imName='大易'
		elif imName in ['嘸', '嘸蝦米', '嘸蝦米輸入法', 'boshiamy', 'bs',]:
			imDirPath='bs/'
			imName='嘸蝦米'
		elif imName in ['鄭', '鄭碼', '鄭碼輸入法', 'zhengma', 'zm',]:
			imDirPath='zm/'
			imName='鄭碼'
		else:
			imDirPath=''
			imName='空'

		imModule=IMMgr.getIMModule(imName)
		return [imModule, imDirPath]

oparser = OptionParser()
oparser.add_option("-i", "--im", dest="imname", help="輸入法名稱", default="倉頡")
oparser.add_option("--dir-charinfo", dest="dir_charinfo", help="結構所在的目錄", default="charinfo")
oparser.add_option("--xml", action="store_true", dest="xml_format")
oparser.add_option("--text", action="store_false", dest="xml_format")
(options, args) = oparser.parse_args()

qiangheng=QiangHeng(options)

