from operatorinfo import OperatorInfo
from operatorinfo.RearrangeInfo import *
from .CharDesc import CharDesc
class OperatorManager:
	def __init__(self, descMgr, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.descMgr=descMgr

		self.directionInfoList={
			'龜':OperatorInfo.Arbitrary,
			'龍':OperatorInfo.Arbitrary,
			'纂':OperatorInfo.Vertical,
			'算':OperatorInfo.Vertical,
			'志':OperatorInfo.Vertical,
			'霜':OperatorInfo.Vertical,
			'想':OperatorInfo.Vertical,
			'爻':OperatorInfo.Vertical,
			'卅':OperatorInfo.Vertical,
			'蚕':OperatorInfo.Vertical,
			'湘':OperatorInfo.Horizontal,
			'好':OperatorInfo.Horizontal,
			'怡':OperatorInfo.Horizontal,
			'穎':OperatorInfo.Horizontal,
			'林':OperatorInfo.Horizontal,
			'鑫':OperatorInfo.Horizontal,
			'鴻':OperatorInfo.Horizontal,
			'載':OperatorInfo.Arbitrary,
			'廖':OperatorInfo.Arbitrary,
			'起':OperatorInfo.Arbitrary,
			'夾':OperatorInfo.Arbitrary,
			'燚':OperatorInfo.Arbitrary,
			'回':OperatorInfo.Surrounding,
			'同':OperatorInfo.Surrounding,
			'函':OperatorInfo.Surrounding,
			'區':OperatorInfo.Surrounding,
			'左':OperatorInfo.Surrounding,
#			'水':OperatorInfo.Arbitrary,
		}

		self.rearrangeInfoDict={
			'龜':RearrangeInfoSame(),
			'水':RearrangeInfoSame(),
			'錯':RearrangeInfoSame(),
			'起':RearrangeInfoSame(),
			'廖':RearrangeInfoSame(),
			'載':RearrangeInfoSame(),
			'聖':RearrangeInfoSame(),
			'霜':RearrangeInfoFrost(self.emptyCharDescGenerator),
			'想':RearrangeInfoThink(self.emptyCharDescGenerator),
			'怡':RearrangeInfoHappy(self.emptyCharDescGenerator),
			'穎':RearrangeInfoSmart(self.emptyCharDescGenerator),
			'回':RearrangeInfoSame(),
			'同':RearrangeInfoSame(),
			'函':RearrangeInfoSame(),
			'區':RearrangeInfoSame(),
			'左':RearrangeInfoSame(),
			'好':RearrangeInfoSame(),
			'志':RearrangeInfoSame(),
			'算':RearrangeInfoSame(),
			'湘':RearrangeInfoSame(),
			'纂':RearrangeInfoSame(),
			'膷':RearrangeInfoSame(),
			'林':RearrangeInfoH2(),
			'爻':RearrangeInfoV2(),
			'卅':RearrangeInfoH3(),
			'丰':RearrangeInfoV3(),
			'鑫':RearrangeInfoTriangle(self.emptyCharDescGenerator),
			'卌':RearrangeInfoH4(),
			'圭':RearrangeInfoV4(),
			'燚':RearrangeInfoSquare(self.emptyCharDescGenerator),
		}
	# 分成以下層級
	# SpecialCase:	錯、龜、水
	# 橫、縱：鴻：不定個數橫向組同，蚕：不定個數縱向組合，龍：不定個數的組同。
	# Base:		好、志、湘、算、纂、膷
	# Surrounding:	回、同、區、函、左
	# LShape:	廖、載、聖、起
	# Insertion:	夾、衍、衷
	# TowLayer:	霜、想、怡、穎
	# Repeate:	林、爻、卅、丰、卌、圭、燚
	def rearrangeDesc(self, charDesc):
		rearrangeInfo=self.rearrangeInfoDict.get(charDesc.getOperator())

		if rearrangeInfo!=None:
			rearrangeInfo.rearrange(charDesc)

	def computeDirection(self, oldOperator):
		"""計算部件的結合方向"""

		directionInfo=self.directionInfoList.get(oldOperator, OperatorInfo.Arbitrary)
		return directionInfo.getDirection()

class OperatorManager_AR(OperatorManager):
	def __init__(self, descMgr, emptyCharDescGenerator):
		OperatorManager.__init__(self, descMgr, emptyCharDescGenerator)
		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical()
		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp()

class OperatorManager_BS(OperatorManager):
	def __init__(self, descMgr, emptyCharDescGenerator):
		OperatorManager.__init__(self, descMgr, emptyCharDescGenerator)
		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp()
		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical()

class OperatorManager_CJ(OperatorManager):
	def __init__(self, descMgr, emptyCharDescGenerator):
		OperatorManager.__init__(self, descMgr, emptyCharDescGenerator)

class OperatorManager_DY(OperatorManager):
	def __init__(self, descMgr, emptyCharDescGenerator):
		OperatorManager.__init__(self, descMgr, emptyCharDescGenerator)
		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp()
		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical()

class OperatorManager_ZM(OperatorManager):
	def __init__(self, descMgr, emptyCharDescGenerator):
		OperatorManager.__init__(self, descMgr, emptyCharDescGenerator)
		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp()

