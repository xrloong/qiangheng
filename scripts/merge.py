import lxml.etree as ET

fileCJK = 'CJK.xml'
fileCJK_A = 'CJK-A.xml'

inFolder = "qhdata/"
mergedFileName = fileCJK

arFileName = inFolder + 'ar/radix/' + fileCJK
bsFileName = inFolder + 'bs/radix/' + fileCJK
cjFileName = inFolder + 'cj/radix/' + fileCJK
dyFileName = inFolder + 'dy/radix/' + fileCJK
zmFileName = inFolder + 'zm/radix/' + fileCJK
fcFileName = inFolder + 'fc/radix/' + fileCJK
dcFileName = inFolder + 'dc/radix/' + fileCJK

arDoc=ET.parse(arFileName)
bsDoc=ET.parse(bsFileName)
cjDoc=ET.parse(cjFileName)
dyDoc=ET.parse(dyFileName)
zmDoc=ET.parse(zmFileName)
fcDoc=ET.parse(fcFileName)
dcDoc=ET.parse(dcFileName)

arRoot = arDoc.getroot()
bsRoot = bsDoc.getroot()
cjRoot = cjDoc.getroot()
dyRoot = dyDoc.getroot()
zmRoot = zmDoc.getroot()
fcRoot = fcDoc.getroot()
dcRoot = dcDoc.getroot()
attrib = {
	"版本號": "0.3",
	"文件類型": "字根",
	"輸入法": "行列",
}
mergedRoot = ET.Element("瑲珩", attrib)
mergedCharSet=ET.SubElement(mergedRoot, "字符集")

arChars = arRoot.findall('字符集/字符')
bsChars = bsRoot.findall('字符集/字符')
cjChars = cjRoot.findall('字符集/字符')
dyChars = dyRoot.findall('字符集/字符')
zmChars = zmRoot.findall('字符集/字符')
fcChars = fcRoot.findall('字符集/字符')
dcChars = dcRoot.findall('字符集/字符')
for x in zip(arChars, bsChars, cjChars, dyChars, zmChars, fcChars, dcChars):
	arNode, bsNode, cjNode, dyNode, zmNode,fcNode, dcNode = x
	assert arNode.attrib == bsNode.attrib == cjNode.attrib == dyNode.attrib ==zmNode.attrib == fcNode.attrib == dcNode.attrib

	mergedChar = ET.SubElement(mergedCharSet, "字符", arNode.attrib)

	dcPartNode = ET.SubElement(mergedChar, "字形")
	dcPartNode.extend(dcNode)
	arPartNode = ET.SubElement(mergedChar, "行列")
	arPartNode.extend(arNode)
	bsPartNode = ET.SubElement(mergedChar, "嘸蝦米")
	bsPartNode.extend(bsNode)
	cjPartNode = ET.SubElement(mergedChar, "倉頡")
	cjPartNode.extend(cjNode)
	dyPartNode = ET.SubElement(mergedChar, "大易")
	dyPartNode.extend(dyNode)
	zmPartNode = ET.SubElement(mergedChar, "鄭碼")
	zmPartNode.extend(zmNode)
	fcPartNode = ET.SubElement(mergedChar, "四角")
	fcPartNode.extend(fcNode)

xmlNode=ET.ElementTree(mergedRoot)
f=open(mergedFileName, "w")
print(ET.tounicode(xmlNode, pretty_print=True, with_tail=False), file=f)

