#from xml.etree import ElementTree as ET
#from xml.etree import cElementTree as ET
import lxml.etree as ET
#import lxml.objectify as ET

class XmlWriter:
	def write(self, imInfo, codeMappingInfoList):
		keyMaps=imInfo.getKeyMaps()

		rootNode=ET.Element("輸入法")

		# 名稱
		nameNode=ET.SubElement(rootNode, "輸入法名稱",
			attrib={
				"EN":imInfo.getName('en'),
				"TW":imInfo.getName('tw'),
				"CN":imInfo.getName('cn'),
				"HK":imInfo.getName('hk'),
#				"SG":imInfo.getName('sg'),
				})

		# 屬性
		propertyNode=ET.SubElement(rootNode, "屬性",
			attrib={
				"最大按鍵數":"%s"%imInfo.getMaxKeyLength()
				})

		# 按鍵與顯示的對照表
		keyMapsNode=ET.SubElement(rootNode, "按鍵對應集")
		for key, disp in keyMaps:
			attrib={"按鍵":key, "顯示":disp}
			ET.SubElement(keyMapsNode, "按鍵對應", attrib)

		# 對照表
		charGroup=ET.SubElement(rootNode, "對應集")
		for x in codeMappingInfoList:
			attrib={"按鍵序列":x.getCode(), "字符":x.getName(), "類型":x.getVariance()}
			ET.SubElement(charGroup, "對應", attrib)
		xmlNode=ET.ElementTree(rootNode)
		print(ET.tounicode(xmlNode, pretty_print=True))
#		ET.dump(xmlNode)
#		xmlNode.write(sys.stdout, encoding="unicode")

