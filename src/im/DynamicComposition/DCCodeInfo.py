from ..base.CodeInfo import CodeInfo
from .Calligraphy import Pane
from .Calligraphy import StrokeGroup

class DCCodeInfo(CodeInfo):
	def __init__(self, strokeGroup):
		CodeInfo.__init__(self)

		self.strokeGroup=strokeGroup

	@staticmethod
	def generateDefaultCodeInfo(strokeGroup):
		codeInfo=DCCodeInfo(strokeGroup)
		return codeInfo

	def toCode(self):
		return self.getCode()

	def getStrokeList(self):
		return self.strokeGroup.getStrokeList()

	def getCode(self):
		strokeList=self.getStrokeList()
		codeList=[stroke.getCode() for stroke in strokeList]
		return ','.join(codeList)

