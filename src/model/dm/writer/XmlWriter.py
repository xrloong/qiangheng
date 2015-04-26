#from xml.etree import ElementTree as ET
#from xml.etree import cElementTree as ET
import lxml.etree as ET
#import lxml.objectify as ET

class XmlWriter:
	def write(self, imInfo, codeMappingInfoList):
		keyMaps=imInfo.getKeyMaps()

		rootNode=ET.Element("描繪法")

		# 對照表
		charGroup=ET.SubElement(rootNode, "描繪集")
		for x in codeMappingInfoList:
			attrib={"名稱":x.getName(), "描繪序列":x.getCode(), "類型":x.getVariance()}
			ET.SubElement(charGroup, "描繪", attrib)
		xmlNode=ET.ElementTree(rootNode)
		print(ET.tounicode(xmlNode, pretty_print=True))
#		ET.dump(xmlNode)
#		xmlNode.write(sys.stdout, encoding="unicode")

