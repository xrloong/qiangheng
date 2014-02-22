#!/usr/bin/env python3
import lxml.etree as ET
import sys

filename=sys.argv[1]
infile = open(filename)

rootNode=ET.Element("瑲珩",
	attrib={
		"版本號":"0.3",
		"文件類型":"組字"
	})
characterSetNode=ET.SubElement(rootNode, "字符集")
for line in infile:
	line=line.strip()
	l=line.split()

	codePoint=int(l[0], 16)
	if codePoint%256==0:
		comment=ET.Comment("%X"%codePoint)
		characterSetNode.append(comment)

	character=ET.SubElement(characterSetNode, "字符",
		attrib={
			"名稱" : chr(codePoint),
			"註記" : "U+%X"%codePoint,
		})

	operator=l[1]
	if operator=="XXXX":
		ET.SubElement(character, "組字")
	elif operator=="龜":
		ET.SubElement(character, "組字")
	else:
		assemble=ET.SubElement(character, "組字",
			attrib={
				"運算" : operator,
			})
		for operand in l[2:]:
			operandNode=ET.SubElement(assemble, "字根",
				attrib={
					"置換" : operand,
				})
xmlNode=ET.ElementTree(rootNode)
print(ET.tounicode(xmlNode, pretty_print=True))

