import lxml.etree as ET
import os
import sys

fileCJK = "CJK.xml"
fileCJK_A = "CJK-A.xml"

mergedFileName = sys.argv[1]
outFolder = sys.argv[2]
outFileName = sys.argv[3]

os.makedirs(outFolder + "ar/radix/", exist_ok=True)
os.makedirs(outFolder + "bs/radix/", exist_ok=True)
os.makedirs(outFolder + "cj/radix/", exist_ok=True)
os.makedirs(outFolder + "dy/radix/", exist_ok=True)
os.makedirs(outFolder + "zm/radix/", exist_ok=True)
os.makedirs(outFolder + "fc/radix/", exist_ok=True)
os.makedirs(outFolder + "dc/radix/", exist_ok=True)

arFileName = outFolder + "ar/radix/" + outFileName
bsFileName = outFolder + "bs/radix/" + outFileName
cjFileName = outFolder + "cj/radix/" + outFileName
dyFileName = outFolder + "dy/radix/" + outFileName
zmFileName = outFolder + "zm/radix/" + outFileName
fcFileName = outFolder + "fc/radix/" + outFileName
dcFileName = outFolder + "dc/radix/" + outFileName

# arDoc=ET.parse(arFileName)
# bsDoc=ET.parse(bsFileName)
# cjDoc=ET.parse(cjFileName)
# dyDoc=ET.parse(dyFileName)
# zmDoc=ET.parse(zmFileName)
# fcDoc=ET.parse(fcFileName)
# dcDoc=ET.parse(dcFileName)

attrib = {
    "版本號": "0.3",
    "文件類型": "字根",
}

attrib["輸入法"] = "行列"
arRoot = ET.Element("瑲珩", attrib)
attrib["輸入法"] = "嘸蝦米"
bsRoot = ET.Element("瑲珩", attrib)
attrib["輸入法"] = "倉頡"
cjRoot = ET.Element("瑲珩", attrib)
attrib["輸入法"] = "大易"
dyRoot = ET.Element("瑲珩", attrib)
attrib["輸入法"] = "鄭碼"
zmRoot = ET.Element("瑲珩", attrib)
attrib["輸入法"] = "四角"
fcRoot = ET.Element("瑲珩", attrib)
attrib["輸入法"] = "動態組字"
dcRoot = ET.Element("瑲珩", attrib)

arCharSet = ET.SubElement(arRoot, "字符集")
bsCharSet = ET.SubElement(bsRoot, "字符集")
cjCharSet = ET.SubElement(cjRoot, "字符集")
dyCharSet = ET.SubElement(dyRoot, "字符集")
zmCharSet = ET.SubElement(zmRoot, "字符集")
fcCharSet = ET.SubElement(fcRoot, "字符集")
dcCharSet = ET.SubElement(dcRoot, "字符集")


def writeRootToFile(root, filename):
    xmlNode = ET.ElementTree(root)
    f = open(filename, "w")
    print(ET.tounicode(xmlNode, pretty_print=True, with_tail=False), file=f)


mergedDoc = ET.parse(mergedFileName)
mergedRoot = mergedDoc.getroot()


mergedChars = mergedRoot.findall("字符集/字符")
for charNode in mergedChars:
    attrib = charNode.attrib
    arChar = ET.SubElement(arCharSet, "字符", attrib)
    bsChar = ET.SubElement(bsCharSet, "字符", attrib)
    cjChar = ET.SubElement(cjCharSet, "字符", attrib)
    dyChar = ET.SubElement(dyCharSet, "字符", attrib)
    zmChar = ET.SubElement(zmCharSet, "字符", attrib)
    fcChar = ET.SubElement(fcCharSet, "字符", attrib)
    dcChar = ET.SubElement(dcCharSet, "字符", attrib)

    arNode = charNode.find("行列")
    bsNode = charNode.find("嘸蝦米")
    cjNode = charNode.find("倉頡")
    dyNode = charNode.find("大易")
    zmNode = charNode.find("鄭碼")
    fcNode = charNode.find("四角")
    dcNode = charNode.find("字形")

    arChar.extend(arNode)
    bsChar.extend(bsNode)
    cjChar.extend(cjNode)
    dyChar.extend(dyNode)
    zmChar.extend(zmNode)
    fcChar.extend(fcNode)
    dcChar.extend(dcNode)

# arNode, bsNode, cjNode, dyNode, zmNode,fcNode, dcNode = x
# assert arNode.attrib == bsNode.attrib == cjNode.attrib == dyNode.attrib ==zmNode.attrib == fcNode.attrib == dcNode.attrib

# mergedChar = ET.SubElement(mergedCharSet, "字符", arNode.attrib)
#
# dcPartNode = ET.SubElement(mergedChar, "字形")
# dcPartNode.extend(dcNode)
# arPartNode = ET.SubElement(mergedChar, "行列")
# arPartNode.extend(arNode)
# bsPartNode = ET.SubElement(mergedChar, "嘸蝦米")
# bsPartNode.extend(bsNode)
# cjPartNode = ET.SubElement(mergedChar, "倉頡")
# cjPartNode.extend(cjNode)
# dyPartNode = ET.SubElement(mergedChar, "大易")
# dyPartNode.extend(dyNode)
# zmPartNode = ET.SubElement(mergedChar, "鄭碼")
# zmPartNode.extend(zmNode)
# fcPartNode = ET.SubElement(mergedChar, "四角")
# fcPartNode.extend(fcNode)

writeRootToFile(arRoot, arFileName)
writeRootToFile(bsRoot, bsFileName)
writeRootToFile(cjRoot, cjFileName)
writeRootToFile(dyRoot, dyFileName)
writeRootToFile(zmRoot, zmFileName)
writeRootToFile(fcRoot, fcFileName)
writeRootToFile(dcRoot, dcFileName)
