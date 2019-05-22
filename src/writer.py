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

# quiet writer
class BaseCmYamlWriter(BaseWriter):
	def writeCodeMapping(self, codeMappingInfoList):
		codingTypeName = self.getCodingTypeName()

		nodeCodeMaps = []
		for codeMappingInfo in codeMappingInfoList:
			info = self.interpreteCodeMappingInfo(codeMappingInfo)
			nodeCodeMaps.append(info)

		codeMappingSet = {
			"編碼類型": codingTypeName,
			"編碼集": nodeCodeMaps
		}

		print(yaml.dump(codeMappingSet, allow_unicode=True, Dumper = CustomDumper))


class CustomDumper(yaml.cyaml.CDumper):
	#Super neat hack to preserve the mapping key order. See https://stackoverflow.com/a/52621703/1497385
	def represent_dict_preserve_order(self, data):
		return self.represent_dict(data.items())

CustomDumper.add_representer(dict, CustomDumper.represent_dict_preserve_order)

# YAML writer for input methods
class ImYamlWriter(BaseCmYamlWriter):
	def interpreteCodeMappingInfo(self, codeMappingInfo):
		return {"字符": codeMappingInfo.getName(),
			"類型": codeMappingInfo.getVariance(),
			"按鍵序列": codeMappingInfo.getCode()}

	def getCodingTypeName(self):
		return "輸入法"


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
class DmYamlWriter(BaseCmYamlWriter):
	def interpreteCodeMappingInfo(self, codeMappingInfo):
		from xie.graphics.drawing import DrawingSystem
		from xie.graphics.stroke import Character

		controller = YamlCanvasController()
		ds = DrawingSystem(controller)

		charName = codeMappingInfo.getName()
		dcStrokeGroup = codeMappingInfo.getCode()
		variance = codeMappingInfo.getVariance()

		controller = YamlCanvasController()
		ds = DrawingSystem(controller)

		strokeGroup = dcStrokeGroup.getStrokeGroup()
		character = Character(charName, strokeGroup)

		ds.draw(character)

		code = controller.getStrokes()

		return {"字符": charName, "類型":variance, "字圖":code}

	def getCodingTypeName(self):
		return "描繪法"

