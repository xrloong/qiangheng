from ..base.CodeInfo import CodeInfo
from ..DynamicComposition.DCCodeInfo import DCCodeInfo

class SOCodeInfo(DCCodeInfo):
	INSTALLMENT_SEPERATOR='|'
	STROKE_SEPERATOR=';'
	RADIX_SEPERATOR=','

	def __init__(self, strokeGroup):
		super().__init__(strokeGroup)

	@staticmethod
	def generateDefaultCodeInfo(strokeGroup):
		codeInfo=SOCodeInfo(strokeGroup)
		return codeInfo

	def getCode(self):
		strokeList=self.getStrokeList()
		codeList=[stroke.getTypeName() for stroke in strokeList]
		return ','.join(codeList)

