from model.base.IMInfo import IMInfo
from model.base.CodeInfo import CodeInfo
from ..DynamicComposition.DCCodeInfo import DCCodeInfo
from ..DynamicComposition.DCCodeInfoEncoder import DCCodeInfoEncoder
from ..DynamicComposition.DCRadixManager import DCRadixParser

class StrokeOrderInfo(IMInfo):
	"筆順"

	IMName="筆順"
	def __init__(self):
		self.keyMaps=[
			['0', '0',],
			['1', '1',],
			['2', '2',],
			['3', '3',],
			['4', '4',],
			['5', '5',],
			['6', '6',],
			['7', '7',],
			['8', '8',],
			['9', '9',],
			]
		self.nameDict={
				'cn':'笔順',
				'tw':'筆順',
				'hk':'筆順',
				'en':'StrokeOrder',
				}
		self.iconfile="qhdc.svg"
		self.maxkeylength=4

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

class SOCodeInfoEncoder(DCCodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, strokeGroup):
		return SOCodeInfo.generateDefaultCodeInfo(strokeGroup)

class SORadixParser(DCRadixParser):
	def __init__(self):
		super().__init__()

IMInfo = StrokeOrderInfo
CodeInfoEncoder = SOCodeInfoEncoder
RadixParser = SORadixParser

