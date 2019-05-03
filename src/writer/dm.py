from xie.graphics.drawing import DrawingSystem
from xie.graphics.stroke import Character


# base writer
class BaseDmWriter:
	def write(self, imInfo, characterInfoList):
		codeMappingInfoList=self.genIMMapping(characterInfoList)
		self.writeCodeMapping(imInfo, codeMappingInfoList)

	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		pass

	def genIMMapping(self, characterInfoList):
		table=[]
		for characterInfo in characterInfoList:
			table.extend(characterInfo.getCodeMappingInfoList())
		return table


# Quiet writer
class QuietWriter(BaseDmWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		pass


# text writer
from xie.graphics.canvas import BaseTextCanvasController

class TextCanvasController(BaseTextCanvasController):
	def __init__(self):
		super().__init__()
		self.table=[]

	def getTable(self):
		return self.table

	def onPreDrawCharacter(self, character):
		pass

	def onPostDrawCharacter(self, character):
		charName=character.getName()
		self.table.append((charName, self.getCharacterExpression()))

class TxtWriter(BaseDmWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		table="\n".join(map(lambda x : '{0[0]}\t{0[1]}'.format(x), codeMappingInfoList))
		print(table)

	def genIMMapping(self, characterInfoList):
		controller = TextCanvasController()
		ds = DrawingSystem(controller)
		for characterInfo in characterInfoList:
			codeMappingInfoList=characterInfo.getCodeMappingInfoList()
			for codeMappingInfo in codeMappingInfoList:
				code=codeMappingInfo.getCode()
				charName=codeMappingInfo.getName()

				if len(charName)>1:
					continue

				dcStrokeGroup = code
				strokeGroup = dcStrokeGroup.getStrokeGroup()
				character=Character(charName, strokeGroup)

				ds.draw(character)
		return controller.getTable()


# XML writer
#from xml.etree import ElementTree as ET
#from xml.etree import cElementTree as ET
import lxml.etree as ET
#import lxml.objectify as ET

from xie.graphics.canvas import HexTextCanvasController

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


# YAML writer
import yaml

class CustomDumper(yaml.Dumper):
	#Super neat hack to preserve the mapping key order. See https://stackoverflow.com/a/52621703/1497385
	def represent_dict_preserve_order(self, data):
		return self.represent_dict(data.items())

CustomDumper.add_representer(dict, CustomDumper.represent_dict_preserve_order)

class YamlCanvasController(BaseTextCanvasController):
	def __init__(self):
		super().__init__()
		self.strokes = []

	def getStrokes(self):
		return self.strokes

	def onPreDrawCharacter(self, character):
		self.strokes=[]

	def onPreDrawStroke(self, stroke):
		self.clearStrokeExpression()

	def onPostDrawStroke(self, stroke):
		e=self.getStrokeExpression()
		if e:
			attrib={
				"名稱": stroke.getName(),
				"描繪": e,
				}
			self.strokes.append(attrib)

class YamlWriter(BaseDmWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		rootNode="描繪法"

		controller = YamlCanvasController()
		ds = DrawingSystem(controller)
		l=[]
		for codeMappingInfo in codeMappingInfoList:
			charName = codeMappingInfo.getName()
			dcStrokeGroup = codeMappingInfo.getCode()
			variance = codeMappingInfo.getVariance()

			controller = YamlCanvasController()
			ds = DrawingSystem(controller)

			strokeGroup = dcStrokeGroup.getStrokeGroup()
			character = Character(charName, strokeGroup)

			ds.draw(character)

			code = controller.getStrokes()

			attrib = {"名稱": charName, "類型":variance, "字圖":code}
			l.append(attrib)
		codeMappingSet={"描繪法":l}

		print(yaml.dump(codeMappingSet, allow_unicode=True, Dumper = CustomDumper))

if __name__=='__main__':
	pass

