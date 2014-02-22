from operatorinfo.RearrangeInfo import *
from .CharDesc import CharDesc
from character import Operator

class OperatorManager:
	def __init__(self, descMgr, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.descMgr=descMgr

		operatorLoong=self.getOperatorByName('龍')
		operatorH2=self.getOperatorByName('好')
		operatorH3=self.getOperatorByName('湘')
		operatorH4=self.getOperatorByName('膷')
		operatorV2=self.getOperatorByName('志')
		operatorV3=self.getOperatorByName('算')
		operatorV4=self.getOperatorByName('纂')
		self.rearrangeInfoDict={
			'龜':RearrangeInfoSame(),
			'水':RearrangeInfoSame(),
			'錯':RearrangeInfoSame(),
			'起':RearrangeInfoSame(),
			'廖':RearrangeInfoSame(),
			'載':RearrangeInfoSame(),
			'聖':RearrangeInfoSame(),
			'霜':RearrangeInfoFrost(self.emptyCharDescGenerator, operatorH2, operatorV2),
			'想':RearrangeInfoThink(self.emptyCharDescGenerator, operatorH2, operatorV2),
			'怡':RearrangeInfoHappy(self.emptyCharDescGenerator, operatorH2, operatorV2),
			'穎':RearrangeInfoSmart(self.emptyCharDescGenerator, operatorH2, operatorV2),
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
			'林':RearrangeInfoH2(operatorH2),
			'爻':RearrangeInfoV2(operatorV2),
			'卅':RearrangeInfoH3(operatorH3),
			'丰':RearrangeInfoV3(operatorV3),
			'鑫':RearrangeInfoTriangle(self.emptyCharDescGenerator, operatorH2, operatorV2),
			'卌':RearrangeInfoH4(operatorH4),
			'圭':RearrangeInfoV4(operatorV4),
			'燚':RearrangeInfoSquare(self.emptyCharDescGenerator, operatorH2, operatorV2),
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
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical(operatorLoong)
		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)

class OperatorManager_BS(OperatorManager):
	def __init__(self, descMgr, emptyCharDescGenerator):
		OperatorManager.__init__(self, descMgr, emptyCharDescGenerator)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)
		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical(operatorLoong)

class OperatorManager_CJ(OperatorManager):
	def __init__(self, descMgr, emptyCharDescGenerator):
		OperatorManager.__init__(self, descMgr, emptyCharDescGenerator)

class OperatorManager_DY(OperatorManager):
	def __init__(self, descMgr, emptyCharDescGenerator):
		OperatorManager.__init__(self, descMgr, emptyCharDescGenerator)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)
		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical(operatorLoong)

class OperatorManager_ZM(OperatorManager):
	def __init__(self, descMgr, emptyCharDescGenerator):
		OperatorManager.__init__(self, descMgr, emptyCharDescGenerator)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)
#		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical()


