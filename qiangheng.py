#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from im.IMMgr import IMMgr
from xml.dom import minidom

import platform
from character.CharDescriptionManager import CharDescriptionManager
import qhparser

from optparse import OptionParser
oparser = OptionParser()
oparser.add_option("-i", "--im", dest="imname", help="輸入法名稱", default="倉頡")
oparser.add_option("--dir-charinfo", dest="dir_charinfo", help="結構所在的目錄", default="charinfo")
(options, args) = oparser.parse_args()

filenamelist=[
#		'CJK.txt',
		'CJK.xml',
]
fileencoding='utf-8-sig'

def parsestructure(g):
	stacklist=[]
	operandlist=[]
	operator=None
	if g[0]=='(' and g[-1]==')':
		operator=g[1]
		for i in g[2:]:
			if i=='(':
				pass
			elif i==')':
				pass
			elif i=='[':
				pass
			elif i==']':
				pass
			elif i==' ':
				continue
			else:
				operandlist.append(i)
		return [operator, operandlist]
	else:
		return None

def parsestructure(g):
	stacklist=[]
	operandlist=[]
	operator=None
	if g[0]=='(' and g[-1]==')':
		operator=g[1]
		i=3
		while i<len(g):
			if g[i]=='(':
				i+=1
			elif g[i]==')':
				i+=1
			elif g[i]=='[':
				j=i+1
				flag=True
				while j<len(g) and g[j]!=']':
					j+=1
				if j<len(g) and g[j]==']':
					operandlist.append(g[i:j+1])
					i=j+1
				else:
					return None
			elif g[i]==']':
				i+=1
			elif g[i]==' ':
				i+=1
			else:
				operandlist.append(g[i])
				i+=1
		return [operator, operandlist]
	else:
		return None

def getDescDBFromFile(filenamelist, descMgr):
	charInfoGenerator=descMgr.getCharInfoGenerator()
	emptyCharInfoGenerator=descMgr.getEmptyCharInfoGenerator()
	charDescGenerator=descMgr.getCharDescGenerator()
	emptyCharDescGenerator=descMgr.getEmptyCharDescGenerator()

	for filename in filenamelist:
		f=open(filename, encoding=fileencoding)
		for line in f.readlines():
			l=line.strip()
			if not l: continue
			elif l[0]=='#': continue
			ll=l.split('\t')
			if len(ll)>=3:
				parseans=parsestructure(ll[2])
				if not parseans:
					print("錯誤的表達式 %s=%s"%(ll[1], ll[2]))
				else:
					operator, operandlist=parseans
					chInfo=charInfoGenerator(ll[1], ll[3:])
					comp=qhparser.Parser.parse(ll[2], ll[1], charDescGenerator)
					comp.setChInfo(chInfo)
					descMgr[ll[1]]=comp

def getDescDBFromXML(filenamelist, descMgr):
	charInfoGenerator=descMgr.getCharInfoGenerator()
	emptyCharInfoGenerator=descMgr.getEmptyCharInfoGenerator()
	charDescGenerator=descMgr.getCharDescGenerator()
	emptyCharDescGenerator=descMgr.getEmptyCharDescGenerator()

	for filename in filenamelist:
		f=open(filename, encoding=fileencoding)
		xmlNode=minidom.parse(f)
		rootNode=xmlNode.documentElement
		charGroupNode=rootNode.getElementsByTagName("字符集")[0]
		charNodeList=charGroupNode.getElementsByTagName("字符")

		for node in charNodeList:
			charName=node.getAttribute('名稱')
			charExpr=node.getAttribute('表示式')

			parseans=parsestructure(charExpr)
			if not parseans:
				print("錯誤的表達式 %s=%s"%(ll[1], ll[2]))
			else:
				operator, operandlist=parseans
				infoList=[]
				charInfoList=node.getElementsByTagName("字符資訊")
				if charInfoList:
					charInfo=charInfoList[0]
					infoExpr=charInfo.getAttribute('資訊表示式')
					infoExtra=charInfo.getAttribute('補充資訊')
					if infoExpr: infoList.append(infoExpr)
					if infoExtra: infoList.append(infoExtra)
					
				chInfo=charInfoGenerator(charName, infoList)
				comp=qhparser.Parser.parse(charExpr, charName, charDescGenerator)
				comp.setChInfo(chInfo)
				descMgr[charName]=comp

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

	[imModule, imDirPath]=getIMInfo(choice)

	dirchar=options.dir_charinfo + "/"
	tmpfname=filenamelist[0]
	pathlist=[
			dirchar+'main/'+tmpfname,
			dirchar+imDirPath+tmpfname,
			]

	ciGenerator=imModule.CharInfoGenerator
	descMgr=CharDescriptionManager(ciGenerator)

#	getDescDBFromFile(pathlist, descMgr)
	getDescDBFromXML(pathlist, descMgr)
	descMgr.ConstructDescriptionNetwork()

	targetCharList=descMgr.keys()
	cm=genIMMapping(descMgr, targetCharList)
	table="\n".join(sorted(map(lambda x : '{0}\t{1}'.format(*x), cm)))
	print(table)

genFile(options)

