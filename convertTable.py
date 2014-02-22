#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from im.IMMgr import IMMgr
import platform

from optparse import OptionParser
oparser = OptionParser()
oparser.add_option("-t", "--pure-table-file", dest="ptfile", help="表格名稱")
oparser.add_option("-i", "--im", dest="imname", help="輸入法名稱", default="倉頡")
oparser.add_option("-p", "--platform", dest="platform", help="目標平台", default="puretable")
oparser.add_option("--dir-charinfo", dest="dir_charinfo", help="結構所在的目錄", default="charinfo")
(options, args) = oparser.parse_args()

fileencoding='utf-8-sig'
def getTableFromFile(filename):
	t=[]
	if filename:
		f=open(filename, encoding=fileencoding)
		for line in f.readlines():
			t.append(line.split())
	return t

def convertTable(options):
	pf=options.platform
	choice=options.imname

	if choice in ['倉', '倉頡', '倉頡輸入法', 'cangjie', 'cj',]:
		imName='倉頡'
	elif choice in ['行', '行列', '行列輸入法', 'array', 'ar',]:
		imName='行列'
	elif choice in ['易', '大易', '大易輸入法', 'dayi', 'dy',]:
		imName='大易'
	elif choice in ['嘸', '嘸蝦米', '嘸蝦米輸入法', 'boshiamy', 'bs',]:
		imName='嘸蝦米'
	elif choice in ['鄭', '鄭碼', '鄭碼輸入法', 'zhengma', 'zm',]:
		imName='鄭碼'
	elif choice in ['表', '表格', '表格輸入法', 'table', 'tb',]:
		imName='表格'
	else:
		imName='空'

	imClass=IMMgr.getIM(imName)
	inputMethod=imClass()
	cmtable=getTableFromFile(options.ptfile)

	if pf in ['scim']:
		p=platform.ScimPlatform(inputMethod)
	elif pf in ['ibus']:
		p=platform.IBusPlatform(inputMethod)
	elif pf in ['gcin']:
		p=platform.GcinPlatform(inputMethod)
	elif pf in ['ovim']:
		p=platform.OVimPlatform(inputMethod)
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

	table=p.genCodeMappingsTable(cmtable)
	if table: print(table)
#	for x in sorted(table): print(*x, sep='\t')

	if p.strEndTable: print(p.strEndTable)


convertTable(options)

