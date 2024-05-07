#!/usr/bin/env python3

import ruamel.yaml as ryaml
import lxml.etree as ET
import sys

infile = sys.argv[1]
infofile = sys.argv[2]

yaml = ryaml.YAML()
root = yaml.load(open(infile))
info = yaml.load(open(infofile))

codingType = root["編碼類型"]
rootNode=ET.Element("編碼法", attrib={"編碼類型": codingType})
if (codingType == "輸入法"):
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

codingType = root["編碼類型"]
if "編碼集" in root:
	mappings = root["編碼集"]

	if (codingType == "輸入法"):
		charGroup=ET.SubElement(rootNode, "編碼集")
		for mapping in mappings:
			keySequence = mapping['按鍵序列']
			character = mapping['字符']
			variance = mapping['類型']
			attrib={"按鍵序列": keySequence, "字符": character, "類型": variance}
			ET.SubElement(charGroup, "對應", attrib)

	elif (codingType == "描繪法"):
		characterShapesNode=ET.SubElement(rootNode, "編碼集")
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
	else:
		pass

xmlNode=ET.ElementTree(rootNode)
print(ET.tounicode(xmlNode, pretty_print=True))

