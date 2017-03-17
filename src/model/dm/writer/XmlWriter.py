#from xml.etree import ElementTree as ET
#from xml.etree import cElementTree as ET
import lxml.etree as ET
#import lxml.objectify as ET
from .BaseDmWriter import BaseDmWriter
from xie.graphics.canvas import HexTextCanvasController
from xie.graphics.drawing import DrawingSystem

class XmlCanvasController(HexTextCanvasController):
	def __init__(self, drawingNode):
		super().__init__()
		self.drawingNode = drawingNode

	def onPreDrawStroke(self, stroke):
		self.clearStrokeExpression()

	def onPostDrawStroke(self, stroke):
		e=self.getStrokeExpression()
		if e:
			self.clearStrokeExpression()
			attrib={
				"名稱": stroke.getName(),
				"描繪": e,
				"字面框": str(stroke.getInfoPane()),
				}
			ET.SubElement(self.drawingNode, "筆劃", attrib)

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

			controller = XmlCanvasController(drawingNode)
			ds = DrawingSystem(controller)
			ds.clear()

			code=x.getCode()

			strokeGroup = code
			strokeList = strokeGroup.getStrokeList();

			for stroke in strokeList:
				ds.draw(stroke)

		xmlNode=ET.ElementTree(rootNode)
		print(ET.tounicode(xmlNode, pretty_print=True))
#		ET.dump(xmlNode)
#		xmlNode.write(sys.stdout, encoding="unicode")

