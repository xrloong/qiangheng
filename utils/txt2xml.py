#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform
from xml.dom import minidom
from character.CJCharInfo import CJCharInfo
import sys
import qhparser
from character.CharDescriptionManager import CharDescriptionManager

if len(sys.argv)>1:
	filename=sys.argv[1]
else:
	print('[Usage] txt2xml.py file')
	sys.exit()
f=open(filename, encoding="utf-8-sig")


descMgr=CharDescriptionManager(CJCharInfo)
charInfoGenerator=descMgr.getCharInfoGenerator()
emptyCharInfoGenerator=descMgr.getEmptyCharInfoGenerator()
charDescGenerator=descMgr.getCharDescGenerator()
emptyCharDescGenerator=descMgr.getEmptyCharDescGenerator()


domImpl=minidom.getDOMImplementation()
xmlNode=domImpl.createDocument("http://qiangheng.openfoundry.org/", "瑲珩", None)

charGroup=xmlNode.createElement("字符集")
rootNode=xmlNode.documentElement
rootNode.setAttribute("版本號", "0.1")
rootNode.appendChild(charGroup)

for line in f:
	l=line.strip()
	if not l:
		continue
	if l[0]=='#':
		if len(l.split())>1:
			comment=xmlNode.createComment(l.split()[1])
			charGroup.appendChild(comment)
		continue
	ll=l.split('\t')
	char=xmlNode.createElement("字符")
	char.setAttribute("註記", ll[0])
	char.setAttribute("名稱", ll[1])

	combInfo=xmlNode.createElement("組字資訊")
	combInfo.setAttribute("表示式", ll[2])
#	qhparser.Parser.parse(ll[2], ll[0], charDescGenerator)
	x=qhparser.ParserXML.parse(ll[2], ll[0], charDescGenerator, xmlNode)
	char.appendChild(combInfo)
	char.appendChild(x)

	if len(ll)>3:
		charInfo=xmlNode.createElement("編碼資訊")
		charInfo.setAttribute('資訊表示式',ll[3])
		if len(ll)>4:
			charInfo.setAttribute('補充資訊',ll[4])
		char.appendChild(charInfo)
	charGroup.appendChild(char)
	#print(ll)

print(xmlNode.toprettyxml())

if __name__=='__main__':
	pass
