import yaml
from .BaseDmWriter import BaseDmWriter
from xie.graphics.canvas import BaseTextCanvasController
from xie.graphics.drawing import DrawingSystem
from xie.graphics.stroke import Character

class YamlCanvasController(BaseTextCanvasController):
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

