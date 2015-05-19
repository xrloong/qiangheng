#from xml.etree import ElementTree as ET
#from xml.etree import cElementTree as ET
import lxml.etree as ET
#import lxml.objectify as ET
from .BaseDmWriter import BaseDmWriter

class XmlWriter(BaseDmWriter):
	def write(self, imInfo, characterInfoList):
		codeMappingInfoList=self.genIMMapping(characterInfoList)
		self.writeCodeMapping(imInfo, codeMappingInfoList)

	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		keyMaps=imInfo.getKeyMaps()

		rootNode=ET.Element("描繪法")

		# 對照表
		charGroup=ET.SubElement(rootNode, "字圖集")
		for x in codeMappingInfoList:
			attrib={"名稱":x.getName(), "類型":x.getVariance()}
			drawingNode=ET.SubElement(charGroup, "字圖", attrib)

			code=x.getCode()
			for stroke in code:
				strokeName=stroke.getName()
				strokeExpression=stroke.getExpression()
				attrib={
					"名稱": stroke.getName(),
					"描繪": stroke.getExpression(),
					"字面框": str(stroke.getInfoPane()),
					}
				ET.SubElement(drawingNode, "筆劃", attrib)

		xmlNode=ET.ElementTree(rootNode)
		print(ET.tounicode(xmlNode, pretty_print=True))
#		ET.dump(xmlNode)
#		xmlNode.write(sys.stdout, encoding="unicode")

