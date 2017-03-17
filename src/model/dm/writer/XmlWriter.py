#from xml.etree import ElementTree as ET
#from xml.etree import cElementTree as ET
import lxml.etree as ET
#import lxml.objectify as ET
from .BaseDmWriter import BaseDmWriter
from xie.graphics.canvas import HexTextCanvasController
from xie.graphics.drawing import DrawingSystem
from xie.graphics.stroke import Character

class XmlCanvasController(HexTextCanvasController):
	def __init__(self, charGroupNode):
		super().__init__()
		self.charGroupNode = charGroupNode
		self.drawingNode = None

	def onPreDrawCharacter(self, character):
		charName=character.getName()
		variance=character.getTag()
		attrib={"名稱":charName, "類型":variance}
		self.drawingNode=ET.SubElement(self.charGroupNode, "字圖", attrib)

	def onPostDrawCharacter(self, character):
		pass

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
		controller = XmlCanvasController(charGroup)
		ds = DrawingSystem(controller)
		for codeMappingInfo in codeMappingInfoList:
			code=codeMappingInfo.getCode()
			charName=codeMappingInfo.getName()
			variance=codeMappingInfo.getVariance()

			dcStrokeGroup = code
			strokeGroup = dcStrokeGroup.getStrokeGroup()
			character=Character(charName, strokeGroup, tag=variance)

			ds.draw(character)

		xmlNode=ET.ElementTree(rootNode)
		print(ET.tounicode(xmlNode, pretty_print=True))
#		ET.dump(xmlNode)
#		xmlNode.write(sys.stdout, encoding="unicode")

