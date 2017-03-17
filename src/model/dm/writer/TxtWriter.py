from .BaseDmWriter import BaseDmWriter
from xie.graphics.canvas import BaseTextCanvasController
from xie.graphics.drawing import DrawingSystem
from xie.graphics.stroke import Character

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

