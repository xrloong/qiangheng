import yaml
from .BaseDmWriter import BaseDmWriter
from xie.graphics.canvas import BaseTextCanvasController
from xie.graphics.drawing import DrawingSystem

class YamlCanvasController(BaseTextCanvasController):
	def __init__(self):
		super().__init__()

class YamlWriter(BaseDmWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		rootNode="描繪法"

		l=[]
		for x in codeMappingInfoList:
			attrib={"名稱":x[0], "描繪序列":x[1]}
			l.append(attrib)
		codeMappingSet={"描繪集":l}

		l=[codeMappingSet]
		print(yaml.dump(l, allow_unicode=True))

	def genIMMapping(self, characterInfoList):
		controller = YamlCanvasController()
		ds = DrawingSystem(controller)

		table=[]
		for characterInfo in characterInfoList:
			codeMappingInfoList=characterInfo.getCodeMappingInfoList()
			for codeMappingInfo in codeMappingInfoList:
				code=codeMappingInfo.getCode()
				charName=codeMappingInfo.getName()

				if len(charName)>1:
					continue

				ds.clear()
				for stroke in code:
					ds.draw(stroke)
				table.append((charName, controller.getCharacterExpression()))
		return table

