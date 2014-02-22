from ..base.CodeInfo import CodeInfo
from ..DynamicComposition.DCCodeInfo import DCCodeInfo

class SOCodeInfo(DCCodeInfo):
	INSTALLMENT_SEPERATOR='|'
	STROKE_SEPERATOR=';'
	RADIX_SEPERATOR=','

	def __init__(self, strokeList):
		DCCodeInfo.__init__(self, strokeList)

	@staticmethod
	def generateDefaultCodeInfo(strokeList):
		codeInfo=SOCodeInfo(strokeList)
		return codeInfo

	def getCode(self):
		codeList=[stroke.getName() for stroke in self.strokeList]
		return ','.join(codeList)

