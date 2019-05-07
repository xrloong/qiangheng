#!/usr/bin/env python3

import ruamel.yaml as yaml
import lxml.etree as ET
import sys

infile = sys.argv[1]
infofile = sys.argv[2]

root = yaml.load(open(infile), yaml.cyaml.CSafeLoader)
info = yaml.load(open(infofile), yaml.cyaml.CSafeLoader)

if "對應集" in root:
	rootName = "輸入法"
elif "描繪法" in root:
	rootName = "描繪法"
else:
	rootName = "編碼法"

rootNode=ET.Element(rootName)
if "編碼法資訊" in info and "描繪法資訊" not in info:
	codingInfos = info["編碼法資訊"]
	imNames = codingInfos["顯示名稱"]

	# 名稱
	nameNode=ET.SubElement(rootNode, "輸入法名稱",
		attrib={
			"EN":imNames.get('en'),
			"TW":imNames.get('tw'),
			"CN":imNames.get('cn'),
			"HK":imNames.get('hk'),
			})

	maxKeyLength = codingInfos.get("最大長度")
	# 屬性
	propertyNode=ET.SubElement(rootNode, "屬性",
		attrib={
			"最大按鍵數": "{}".format(maxKeyLength)
			})

	keyMaps = codingInfos["按鍵對應"]

	keyMapsNode=ET.SubElement(rootNode, "按鍵對應集")
	for keyMap in keyMaps:
		key = keyMap[0]
		disp = keyMap[1]

		attrib={"按鍵":key, "顯示":disp}
		ET.SubElement(keyMapsNode, "按鍵對應", attrib)

if "對應集" in root:
	mappings = root["對應集"]

	charGroup=ET.SubElement(rootNode, "對應集")
	for mapping in mappings:
		keySequence = mapping['按鍵序列']
		character = mapping['字符']
		variance = mapping['類型']
		attrib={"按鍵序列": keySequence, "字符": character, "類型": variance}
		ET.SubElement(charGroup, "對應", attrib)

if "描繪法" in root:
	mappings = root["描繪法"]

	characterShapesNode=ET.SubElement(rootNode, "字圖集")
	for mapping in mappings:
		character = mapping['字符']
		variance = mapping['類型']
		attrib={"字符": character, "類型": variance}
		charNode = ET.SubElement(characterShapesNode, "字圖", attrib)

		strokes = mapping['字圖']
		for stroke in strokes:
			strokeName = stroke["名稱"]
			drawExpression = stroke["描繪"]
			attrib={"名稱": strokeName, "描繪": drawExpression}
			strokeNode = ET.SubElement(charNode, "筆劃", attrib)

xmlNode=ET.ElementTree(rootNode)
print(ET.tounicode(xmlNode, pretty_print=True))

