#!/usr/bin/env python3

from im.IMMgr import IMMgr

import platform
from character.CharDescriptionManager import CharDescriptionManager
import qhparser

from optparse import OptionParser
oparser = OptionParser()
oparser.add_option("-t", "--pure-table-file", dest="ptfile", help="表格名稱")
oparser.add_option("-i", "--im", dest="imname", help="輸入法名稱", default="倉頡")
oparser.add_option("-m", "--method", dest="method", help="産生的方式", default="動態")
oparser.add_option("-p", "--platform", dest="platform", help="目標平台", default="puretable")
oparser.add_option("--dir-charinfo", dest="dir_charinfo", help="結構所在的目錄", default="charinfo")
(options, args) = oparser.parse_args()

filenamelist=[
		'CJK.txt',
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
	anonyCharInfoGenerator=descMgr.getAnonymousCharInfoGenerator()

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
					comp=qhparser.Parser.parse(ll[2], ll[1], anonyCharInfoGenerator)
					comp.setChInfo(chInfo)
					descMgr[ll[1]]=comp

def getTableFromFile(filename):
	t=[]
	if filename:
		f=open(filename, encoding=fileencoding)
		for line in f.readlines():
			t.append(line.split())
	return t

def genFile(options):
	pf=options.platform
	choice=options.imname
	method=options.method

	if choice in ['倉', '倉頡', '倉頡輸入法', 'cangjie', 'cj',]:
		imDirPath='cj/'
		imName='倉頡'
	elif choice in ['行', '行列', '行列輸入法', 'array', 'ar',]:
		imDirPath='ar/'
		imName='行列'
	elif choice in ['易', '大易', '大易輸入法', 'dayi', 'dy',]:
		imDirPath='dy/'
		imName='大易'
	elif choice in ['嘸', '嘸蝦米', '嘸蝦米輸入法', 'boshiamy', 'bs',]:
		imDirPath='bs/'
		imName='嘸蝦米'
	elif choice in ['鄭', '鄭碼', '鄭碼輸入法', 'zhengma', 'zm',]:
		imDirPath='zm/'
		imName='鄭碼'
	else:
		imName='空'

	dirchar=options.dir_charinfo + "/"
	tmpfname=filenamelist[0]
	if imName=='空':
		pathlist=[]
	else:
		pathlist=[
				dirchar+'main/'+tmpfname,
				dirchar+imDirPath+tmpfname,
				]

	inputMethod=IMMgr.getIM(imName)
	constructor=IMMgr.getCharInfoGenerator(imName)

	if method in ['動', '動態', '動態組碼', 'dynamic',]:
		def AnonymouseCharInfoGenerator():
			return constructor("XXXX", [])

		descMgr=CharDescriptionManager(constructor)
		getDescDBFromFile(pathlist, descMgr)
		descMgr.ConstructDescriptionNetwork()

		inputMethod.setStruct(descMgr)
	elif method in ['表', '表格', 'puretable', 'pt']:
		cmtable=getTableFromFile(options.ptfile)
		inputMethod.setTable(cmtable)
	else:
		inputMethod.setTable([])

	if pf in ['scim']:
		p=platform.ScimPlatform(inputMethod)
	elif pf in ['gcin']:
		p=platform.GcinPlatform(inputMethod)
	elif pf in ['msim']:
		p=platform.MSimPlatform(inputMethod)
	elif pf in ['table']:
		p=platform.NonePlatform(inputMethod)
	else:
		p=platform.NonePlatform(inputMethod)

	# 產生檔頭
	header=p.genHeader()

	if header: print(header)
	if p.strBeginTable: print(p.strBeginTable)

	table=p.genCodeMappingsTable(inputMethod.genIMMapping())
	if table: print(table)
#	for x in sorted(table): print(*x, sep='\t')

	if p.strEndTable: print(p.strEndTable)


genFile(options)
