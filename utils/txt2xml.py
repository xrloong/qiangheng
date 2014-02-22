#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from xml.dom import minidom
import sys

if len(sys.argv)>1:
	filename=sys.argv[1]
else:
	print('[Usage] txt2xml.py file')
	sys.exit()
f=open(filename, encoding="utf-8-sig")


domImpl=minidom.getDOMImplementation()
xmlNode=domImpl.createDocument("http://qiangheng.openfoundry.org/", "瑲珩", None)

charGroup=xmlNode.createElement("字符集")
rootNode=xmlNode.documentElement
rootNode.appendChild(charGroup)

for line in f:
	l=line.strip()
	if not l:
		continue
	if l[0]=='#':
		continue
	ll=l.split('\t')
	char=xmlNode.createElement("字符")
	char.setAttribute("註記", ll[0])
	char.setAttribute("名稱", ll[1])
	char.setAttribute("表示式", ll[2])
	if len(ll)>3:
		charInfo=xmlNode.createElement("字符資訊")
		charInfo.setAttribute('資訊表示式',ll[3])
		if len(ll)>4:
			charInfo.setAttribute('補充資訊',ll[4])
		char.appendChild(charInfo)
	charGroup.appendChild(char)
	#print(ll)

print(xmlNode.toprettyxml())

