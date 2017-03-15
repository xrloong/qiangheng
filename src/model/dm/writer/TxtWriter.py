from .BaseDmWriter import BaseDmWriter
from xie.graphics.canvas import BaseTextCanvasController
from xie.graphics.drawing import DrawingSystem

class TextCanvasController(BaseTextCanvasController):
	def __init__(self):
		super().__init__()

class TxtWriter(BaseDmWriter):
	def writeCodeMapping(self, imInfo, codeMappingInfoList):
		table="\n".join(map(lambda x : '{0[0]}\t{0[1]}'.format(x), codeMappingInfoList))
		print(table)

	def genIMMapping(self, characterInfoList):
		controller = TextCanvasController()
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

