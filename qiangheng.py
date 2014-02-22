#!/usr/bin/env python3

import char
import im

from optparse import OptionParser
oparser = OptionParser()
oparser.add_option("-g", "--gen", dest="imname", help="輸入法名稱", default="倉頡")
oparser.add_option("-s", "--style", dest="style", help="表格格式", default="scim")
(options, args) = oparser.parse_args()

filename='U4E00-U9FA6.txt'
fileencoding='utf-8'
f=open(filename, encoding=fileencoding)

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

	table=[]
	if choice in ['倉', '倉頡', '倉頡輸入法', 'cangjie', 'cj',]:
		for chname, ch in chdict.items():
			if ch.cj:
				table.append([ch.cj, chname])
		for x in sorted(table): print(*x, sep='\t')
		im.CangJie()
	elif choice in ['行', '行列', '行列輸入法', 'array', 'ar',]:
		for chname, ch in chdict.items():
			if ch.ar:
				table.append([ch.ar, chname])
		for x in sorted(table): print(*x, sep='\t')
		im.Array()
	elif choice in ['易', '大易', '大易輸入法', 'dayi', 'dy',]:
		for chname, ch in chdict.items():
			if ch.dy:
				table.append([ch.dy, chname])
		for x in sorted(table): print(*x, sep='\t')
		im.DaYi()
	elif choice in ['嘸', '嘸蝦米', '嘸蝦米輸入法', 'boshiamy', 'bs',]:
		for chname, ch in chdict.items():
			if ch.bs:
				table.append([ch.bs, chname])
		for x in sorted(table): print(*x, sep='\t')
		im.Boshiamy()
	elif choice in ['鄭', '鄭碼', '鄭碼輸入法', 'zhengma', 'zm',]:
		for chname, ch in chdict.items():
			if ch.zm:
				table.append([ch.zm, chname])
		for x in sorted(table): print(*x, sep='\t')
		im.ZhengMa()

def genFile(chdict, options):
	style=options.style

	# 產生檔頭
	if style in ['scim']:
		print(
"""SCIM_Generic_Table_Phrase_Library_TEXT
VERSION_1_0

BEGIN_DEFINITION

UUID = {{ uuid }}

SERIAL_NUMBER = {{ datestamp }}

ICON = @SCIM_ICONDIR@/CangJie.png

NAME = {{ SRF.name }}

NAME.zh_CN = {{ SRF.name_cn }}
NAME.zh_TW = {{ SRF.name_tw }}
NAME.zh_HK = {{ SRF.name_hk }}

LANGUAGES = zh_TW,zh_HK,zh_CN,zh_SG

STATUS_PROMPT = 中

KEYBOARD_LAYOUT = US_Default

AUTO_SELECT = FALSE

AUTO_WILDCARD = TRUE

AUTO_COMMIT = FALSE

AUTO_SPLIT = TRUE

DYNAMIC_ADJUST = FALSE

AUTO_FILL = FALSE

ALWAYS_SHOW_LOOKUP = TRUE

DEF_FULL_WIDTH_PUNCT = TRUE

DEF_FULL_WIDTH_LETTER = FALSE

MAX_KEY_LENGTH = 5

VALID_INPUT_CHARS = abcdefghijklmnopqrstuvwxyz

MULTI_WILDCARD_CHAR = *

SPLIT_KEYS = quoteright

COMMIT_KEYS = space

FORWARD_KEYS = Return

SELECT_KEYS = 1,2,3,4,5,6,7,8,9,0

PAGE_UP_KEYS = Page_Up,comma,minus

PAGE_DOWN_KEYS = Page_Down,period,equal

BEGIN_CHAR_PROMPTS_DEFINITION
a 日
b 月
c 金
d 木
e 水
f 火
g 土
h 竹
i 戈
j 十
k 大
l 中
m 一
n 弓
o 人
p 心
q 手
r 口
s 尸
t 廿
u 山
v 女
w 田
x 難
y 卜
z 符
END_CHAR_PROMPTS_DEFINITION
END_DEFINITION""")

	elif style in ['gcin']:
		print(
"""
# 瑲珩
%gen_inp
%ename {{ SRF.name_en }}
%cname {{ SRF.name_tw }}
%selkey 1234567890
%space_style 4
%keyname begin
a 日
b 月
c 金
d 木
e 水
f 火
g 土
h 竹
i 戈
j 十
k 大
l 中
m 一
n 弓
o 人
p 心
q 手
r 口
s 尸
t 廿
u 山
v 女
w 田
x 難
y 卜
z 符
%keyname end
""")
	elif style in ['uime']:
		print(
"""/S A日
/S B月
/S C金
/S D木
/S E水
/S F火
/S G土
/S H竹
/S I戈
/S J十
/S K大
/S L中
/S M一
/S N弓
/S O人
/S P心
/S Q手
/S R口
/S S尸
/S T廿
/S U山
/S V女
/S W田
/S X難
/S Y卜
/S Z符""")

	# 產生表格
	if style in ['scim']:
		print('BEGIN_TABLE')
	elif style in ['gcin']:
		print("""%chardef begin""")
	elif style in ['uime']:
		pass

	genTable(chdict, options)

	if style in ['scim']:
		print('END_TABLE')
	elif style in ['gcin']:
		print("""%chardef end""")
	elif style in ['uime']:
		pass

genFile(chdict, options)
