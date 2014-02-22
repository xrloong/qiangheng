from operatorinfo.RearrangeInfo import *
from .CharDesc import CharDesc

def getOperatorByName(name):
	return OperatorManager.getOperatorByName(name)

class OperatorManager:
	def __init__(self, descMgr, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.descMgr=descMgr

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

	@staticmethod
	def getOperatorByName(operatorName):
		return Operator.Operator(operatorName)

#	def isAvailableOperation(self, operator):
#		return Operator.Operator.isAvailableOperation(operator)

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
		operator=charDesc.getOperator()
		operatorName=operator.getName()
		rearrangeInfo=self.rearrangeInfoDict.get(operatorName)

		if rearrangeInfo!=None:
			rearrangeInfo.rearrange(charDesc)

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
#		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical()


