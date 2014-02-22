from ..base.CodeInfo import CodeInfo
from ..DynamicComposition.DCCodeInfo import DCCodeInfo

class SOCodeInfo(DCCodeInfo):
	INSTALLMENT_SEPERATOR='|'
	STROKE_SEPERATOR=';'
	RADIX_SEPERATOR=','

	def __init__(self, strokeList, region):
		DCCodeInfo.__init__(self, strokeList, region)

	@staticmethod
	def generateDefaultCodeInfo(strokeList, region):
		codeInfo=SOCodeInfo(strokeList, region)
		return codeInfo

	def getCode(self):
		codeList=[stroke.getTypeName() for stroke in self.strokeList]
		return ','.join(codeList)

