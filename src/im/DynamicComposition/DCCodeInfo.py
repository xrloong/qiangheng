from ..base.CodeInfo import CodeInfo
from .Calligraphy import Pane
from .Calligraphy import StrokeGroup

class DCCodeInfo(CodeInfo):
	def __init__(self, strokeGroup):
		CodeInfo.__init__(self)

		self.strokeGroup=strokeGroup
		self.extraPane=None

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

	def setExtraPane(self, extranPane):
		self.extraPane=extranPane

	def getExtraPane(self):
		return self.extraPane

	def getStrokeGroup(self):
		return self.strokeGroup

	def transform(self, pane):
		self.strokeGroup.transform(pane)

