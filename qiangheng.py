#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xml.etree import ElementTree
from im.IMMgr import IMMgr
from character.CharDescriptionManager import CharDescriptionManager

from optparse import OptionParser
oparser = OptionParser()
oparser.add_option("-i", "--im", dest="imname", help="輸入法名稱", default="倉頡")
oparser.add_option("--dir-charinfo", dest="dir_charinfo", help="結構所在的目錄", default="charinfo")
oparser.add_option("--xml", action="store_true", dest="xml_format")
oparser.add_option("--text", action="store_false", dest="xml_format")
(options, args) = oparser.parse_args()

filenamelist=[
#		'CJK.txt',
		'CJK.xml',
]

def getDescDBFromXML(filenamelist, descMgr):
	for filename in filenamelist:
		descMgr.loadFromXML(filename, fileencoding='utf-8-sig')

def genIMMapping(descMgr, targetCharList):
	table=[]
	for chname in targetCharList:
		expandDesc=descMgr.getExpandDescriptionByNameInNetwork(chname)

		if expandDesc==None:
			continue

		descMgr.setCharTree(expandDesc)

		chinfo=expandDesc.getChInfo()
		code=chinfo.getCode()
		if chinfo.isToShow() and code:
			table.append([code, chname])
		else:
			pass
	return table

def getIMInfo(imName):
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
	
def genFile(options):
	choice=options.imname
	xml_format=options.xml_format

	[imModule, imDirPath]=getIMInfo(choice)

	dirchar=options.dir_charinfo + "/"
	tmpfname=filenamelist[0]
	pathlist=[
			dirchar+'main/'+tmpfname,
			dirchar+imDirPath+tmpfname,
			]

	ciGenerator=imModule.CharInfoGenerator
	descMgr=CharDescriptionManager(ciGenerator)

	getDescDBFromXML(pathlist, descMgr)
	descMgr.ConstructDescriptionNetwork()

	if xml_format:
		toXML(descMgr)
	else:
		toTXT(descMgr)

def toXML(descMgr):
	charGroup=ElementTree.Element("對應集")
	targetCharList=descMgr.keys()
	cm=genIMMapping(descMgr, targetCharList)
	for x in cm:
		ElementTree.SubElement(charGroup, "對應", attrib={"按鍵":x[0], "字符":x[1]})
	xmlNode=ElementTree.ElementTree(charGroup)
	ElementTree.dump(xmlNode)
#	xmlNode.write(sys.stdout)

def toTXT(descMgr):
	targetCharList=descMgr.keys()
	cm=genIMMapping(descMgr, targetCharList)
	table="\n".join(sorted(map(lambda x : '{0}\t{1}'.format(*x), cm)))
	print(table)

genFile(options)

