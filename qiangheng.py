#!/usr/bin/env python3

import char
import im
import platform

from optparse import OptionParser
oparser = OptionParser()
oparser.add_option("-g", "--gen", dest="imname", help="輸入法名稱", default="倉頡")
oparser.add_option("-s", "--style", dest="style", help="表格格式", default="scim")
(options, args) = oparser.parse_args()

filenamelist=[
#		'charinfo/Bopomofo.txt',
#		'charinfo/BopomofoExt.txt',
#		'charinfo/CJKpunct.txt',
#		'charinfo/FullASCIIpunct.txt',
		'charinfo/U4E00-U9FA6.txt',
#		'charinfo/U3400-U4DB5.txt',
#		'charinfo/U20000-U2A6DF.txt.txt',
#		'charinfo/Hiragana.txt',
#		'charinfo/Katakana.txt',
#		'charinfo/Verticalpunct.txt',
]
fileencoding='utf-8'

def checkgrammar(g):
	if g[0]=='(' and g[-1]==')':
		if len(g)==3 and g[1]=='龜':
			return True
		elif len(g)==5 and g[1] in ['林', '爻', '卅', '鑫', '燚']:
#			['水', '林', '爻', '卅', '丰', '鑫', '卌', '圭', '燚',]
			return True
		elif len(g)==6 and g[1] in ['好', '志', '回', '同', '函', '區', '載', '廖', '起', '句', '夾',]:
#			['好', '志',
#			'回', '同', '函', '區', '左',
#			'起', '廖', '載', '聖', '句',
#			'夾', '衍', '衷',]
			return True
		elif len(g)==7 and g[1] in ['算', '湘', '霜', '想', '怡', '穎',]:
			return True
		elif len(g)==8 and g[1] in ['纂',]:
#			['纂', '膷',]
			return True
		else:
			return False
	else:
		return False
	return True

chlist=[]
chdict={}

for filename in filenamelist:
	f=open(filename, encoding=fileencoding)
	for line in f.readlines():
		l=line.strip()
		if not l: continue
		elif l[0]=='#': continue
		ll=l.split('\t')
		if len(ll)>=3:
			if not checkgrammar(ll[2]):
				print("錯誤的表達式 %s=%s"%(ll[1], ll[2]))
			else:
				chlist.append(ll[1])
				chdict[ll[1]]=char.Char(ll[1], ll[2:])

def genTable(chdict, options):
	choice=options.imname

	if choice in ['倉', '倉頡', '倉頡輸入法', 'cangjie', 'cj',]:
		z=im.CangJie()
	elif choice in ['行', '行列', '行列輸入法', 'array', 'ar',]:
		z=im.Array()
	elif choice in ['易', '大易', '大易輸入法', 'dayi', 'dy',]:
		z=im.DaYi()
	elif choice in ['嘸', '嘸蝦米', '嘸蝦米輸入法', 'boshiamy', 'bs',]:
		z=im.Boshiamy()
	elif choice in ['鄭', '鄭碼', '鄭碼輸入法', 'zhengma', 'zm',]:
		z=im.ZhengMa()
	else:
		z=im.NoneIM()
	table=z.genTable(chdict)
	for x in sorted(table): print(*x, sep='\t')

def genFile(chdict, options):
	style=options.style

	# 產生檔頭
	if style in ['scim']:
		p=platform.ScimPlatform()
	elif style in ['gcin']:
		p=platform.GcinPlatform()
	elif style in ['msim']:
		p=platform.MSimPlatform()
	else:
		p=platform.NonePlatform()

	print(p.genHeader())
	print(p.strBeginTable)
	genTable(chdict, options)
	print(p.strEndTable)


genFile(chdict, options)
