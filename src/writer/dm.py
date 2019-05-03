import yaml

from xie.graphics.drawing import DrawingSystem
from xie.graphics.stroke import Character
from xie.graphics.canvas import BaseTextCanvasController


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
	def write(self, imInfo, characterInfoList):
		codeMappingInfoList=self.genIMMapping(characterInfoList)
		self.writeCodeMapping(imInfo, codeMappingInfoList)

	def genIMMapping(self, characterInfoList):
		table=[]
		for characterInfo in characterInfoList:
			table.extend(characterInfo.getCodeMappingInfoList())
		return table

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

