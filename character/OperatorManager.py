from operatorinfo.RearrangeInfo import *
from .CharDesc import CharDesc
from character import Operator

class OperatorManager:
	def __init__(self, descMgr, emptyCharDescGenerator):
		self.emptyCharDescGenerator=emptyCharDescGenerator
		self.descMgr=descMgr
		self.templateDB={}

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
		}
		def operatorGenerator(operatorName):
			return Operator.Operator(operatorName)

		self.operatorGenerator=operatorGenerator

	def isTemplateName(self, operatorName):
		return (operatorName in self.templateDB.keys())

	def setTemplateDB(self, templateDB):
		self.templateDB=templateDB

	def getCharDescFromTemplate(self, charDesc):
		templateName=charDesc.getTemplateName()
		templateDesc=self.templateDB.get(templateName)
		charDesc.setTemplateDesc(templateDesc)

		resultDesc=charDesc.getCharDesc()

		resultDesc=self.copyCharDesc(resultDesc)
		resultDesc.setName(charDesc.getName())
		return resultDesc

	def copyCharDesc(self, charDesc):
		if charDesc.getOperator().getName()=='龜':
			ansDesc=charDesc.copyDescription()
			ansDesc.setOperator(charDesc.getOperator())
			return ansDesc
		ansDesc=self.emptyCharDescGenerator()
		ansChildList=[]
		for childDesc in charDesc.getCompList():
			ansChilDesc=self.copyCharDesc(childDesc)
			ansChildList.append(ansChilDesc)
		ansDesc.setCompList(ansChildList)
		ansDesc.setOperator(charDesc.getOperator())
		return ansDesc

	def getOperatorGenerator(self):
		return self.operatorGenerator

	def rearrangeRecursively(self, charDesc):
		if charDesc.isTemplate():
			charDesc=self.getCharDescFromTemplate(charDesc)
		l=[]
		for childDesc in charDesc.getCompList():
			newChildDesc=self.rearrangeRecursively(childDesc)
			l.append(newChildDesc)
		charDesc.setCompList(l)
		self.rearrangeDesc(charDesc)
		return charDesc

	def getOperatorByName(self, operatorName):
		return Operator.Operator(operatorName)

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


