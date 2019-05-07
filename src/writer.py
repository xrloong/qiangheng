import ruamel.yaml as yaml

# base writer
class BaseWriter:
	def write(self, characterInfoList):
		codeMappingInfoList=self.genIMMapping(characterInfoList)
		self.writeCodeMapping(codeMappingInfoList)

	def writeCodeMapping(self, codeMappingInfoList):
		pass

	def genIMMapping(self, characterInfoList):
		table=[]
		for characterInfo in characterInfoList:
			table.extend(characterInfo.getCodeMappingInfoList())
		return table


# quiet writer
class QuietWriter(BaseWriter):
	def writeCodeMapping(self, codeMappingInfoList):
		pass


class CustomDumper(yaml.cyaml.CDumper):
	#Super neat hack to preserve the mapping key order. See https://stackoverflow.com/a/52621703/1497385
	def represent_dict_preserve_order(self, data):
		return self.represent_dict(data.items())

CustomDumper.add_representer(dict, CustomDumper.represent_dict_preserve_order)

# YAML writer for input methods
class ImYamlWriter(BaseWriter):
	def write(self, characterInfoList):
		codeMappingInfoList=self.genIMMapping(characterInfoList)
		self.writeCodeMapping(codeMappingInfoList)

	def genIMMapping(self, characterInfoList):
		table=[]
		for characterInfo in characterInfoList:
			table.extend(characterInfo.getCodeMappingInfoList())
		return table

	def writeCodeMapping(self, codeMappingInfoList):
		nodeCodeMaps = []
		for x in codeMappingInfoList:
			attrib = {"字符":x.getName(), "類型":x.getVariance(), "按鍵序列":x.getCode()}
			nodeCodeMaps.append(attrib)

		r = {
			"對應集": nodeCodeMaps
		}
		print(yaml.dump(r, allow_unicode=True, Dumper = CustomDumper))


try:
	import xie

	from xie.graphics.canvas import BaseTextCanvasController

	class AbsTextCanvasController(BaseTextCanvasController):
		pass
except ImportError:
	class AbsTextCanvasController:
		pass

class YamlCanvasController(AbsTextCanvasController):
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



# YAML writer for drawing methods
class DmYamlWriter(BaseWriter):
	def write(self, characterInfoList):
		codeMappingInfoList=self.genIMMapping(characterInfoList)
		self.writeCodeMapping(codeMappingInfoList)

	def genIMMapping(self, characterInfoList):
		table=[]
		for characterInfo in characterInfoList:
			table.extend(characterInfo.getCodeMappingInfoList())
		return table

	def writeCodeMapping(self, codeMappingInfoList):
		from xie.graphics.drawing import DrawingSystem
		from xie.graphics.stroke import Character

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

			attrib = {"字符": charName, "類型":variance, "字圖":code}
			l.append(attrib)
		codeMappingSet={"描繪法":l}

		print(yaml.dump(codeMappingSet, allow_unicode=True, Dumper = CustomDumper))

