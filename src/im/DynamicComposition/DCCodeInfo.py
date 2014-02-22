from ..base.CodeInfo import CodeInfo
from .Calligraphy import Pane

class DCCodeInfo(CodeInfo):
	INSTALLMENT_SEPERATOR='|'
	STROKE_SEPERATOR=';'
	RADIX_SEPERATOR=','

	def __init__(self, strokeList, pane):
		CodeInfo.__init__(self)

		self.strokeList=strokeList
		self.pane=pane

	@staticmethod
	def generateDefaultCodeInfo(strokeList, pane):
		codeInfo=DCCodeInfo(strokeList, pane)
		return codeInfo

	def toCode(self):
		return self.getCode()

	def getStrokeList(self):
		return self.strokeList

	def getCode(self):
		codeList=[stroke.getCode() for stroke in self.strokeList]
		return ','.join(codeList)

