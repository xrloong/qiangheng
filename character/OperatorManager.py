from .CharDesc import CharDesc
from character import Operator

class RearrangeInfoSame:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		pass

class RearrangeInfoSurroundingOpenUp:
	def __init__(self, OperatorLoong):
		self.operatorLoong=OperatorLoong

	def rearrange(self, charDesc):
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorLoong
		x=oldCompList[0]
		y=oldCompList[1]
		charDesc.setCompList([y, x])
		charDesc.setOperator(ansOperator)

class RearrangeInfoLShapeSimpleRadical:
	def __init__(self, OperatorLoong):
		self.operatorLoong=OperatorLoong

	def rearrange(self, charDesc):
		oldCompList=charDesc.getCompList()

		ansOperator=self.operatorLoong
		x=oldCompList[0]
		y=oldCompList[1]

		if x.getExpandName() in ['辶', '廴']:
			charDesc.setCompList([y, x])
			charDesc.setOperator(ansOperator)

class RearrangeInfoTemplate:
	def __init__(self, templateDesc):
		self.templateDesc=templateDesc

	def rearrange(self, charDesc):
		self.templateDesc.rearrange(charDesc)


class OperatorManager:
	def __init__(self, descMgr):
		self.descMgr=descMgr
		self.templateDB={}

		self.rearrangeInfoDictForBuiltinOperator={
			'龜':RearrangeInfoSame(),
			'爲':RearrangeInfoSame(),
			'龍':RearrangeInfoSame(),

			'蚕':RearrangeInfoSame(),
			'鴻':RearrangeInfoSame(),
			'回':RearrangeInfoSame(),


			'錯':RearrangeInfoSame(),
			'函':RearrangeInfoSame(),
			'起':RearrangeInfoSame(),
		}

		self.directionInfoList={
			'龜':'*',
			'爲':'*',
			'龍':'*',

			'蚕':'|',
			'鴻':'-',
			'回':'@',

			'錯':'*',
			'起':'*',
			'函':'@',
		}

		self.rearrangeInfoDictForTemplateOperator={}
		def operatorGenerator(operatorName):
			direction=self.directionInfoList.get(operatorName, '*')
			return Operator.Operator(operatorName, direction)

		operatorLoong=operatorGenerator('龍')
		self.operatorGenerator=operatorGenerator

	def setTemplateDB(self, templateDB):
		self.templateDB=templateDB
		for templateName, templateDesc in templateDB.items():
			rearrangeInfoTemplate=RearrangeInfoTemplate(templateDesc)
			self.rearrangeInfoDictForTemplateOperator[templateName]=rearrangeInfoTemplate

	def getOperatorGenerator(self):
		return self.operatorGenerator

	def isTemplateOperator(self, operator):
		return (operator.getName() in self.templateDB.keys())

	def rearrangeRecursively(self, charDesc):
		self.rearrangeDesc(charDesc)
		for childDesc in charDesc.getCompList():
			self.rearrangeRecursively(childDesc)
		return charDesc

	def getOperatorByName(self, operatorName):
		return self.operatorGenerator(operatorName)

	def rearrangeDesc(self, charDesc):
		operator=charDesc.getOperator()
		rearrangeInfo=self.getRearrangeInfoByOperator(operator)

		if rearrangeInfo!=None:
			rearrangeInfo.rearrange(charDesc)
			operator=charDesc.getOperator()
			if self.isTemplateOperator(operator):
				self.rearrangeDesc(charDesc)

	def getRearrangeInfoByOperator(self, operator):
		operatorName=operator.getName()
		if self.isTemplateOperator(operator):
			rearrangeInfo=self.rearrangeInfoDictForTemplateOperator.get(operatorName)
		else:
			rearrangeInfo=self.rearrangeInfoDictForBuiltinOperator.get(operatorName)
		return rearrangeInfo

	def adjustTemplate(self):
		pass

class OperatorManager_AR(OperatorManager):
	def __init__(self, descMgr):
		OperatorManager.__init__(self, descMgr)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDictForBuiltinOperator['起']=RearrangeInfoLShapeSimpleRadical(operatorLoong)
		self.rearrangeInfoDictForBuiltinOperator['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)

class OperatorManager_BS(OperatorManager):
	def __init__(self, descMgr):
		OperatorManager.__init__(self, descMgr)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDictForBuiltinOperator['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)
		self.rearrangeInfoDictForBuiltinOperator['起']=RearrangeInfoLShapeSimpleRadical(operatorLoong)

class OperatorManager_CJ(OperatorManager):
	def __init__(self, descMgr):
		OperatorManager.__init__(self, descMgr)

class OperatorManager_DY(OperatorManager):
	def __init__(self, descMgr):
		OperatorManager.__init__(self, descMgr)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDictForBuiltinOperator['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)
		self.rearrangeInfoDictForBuiltinOperator['起']=RearrangeInfoLShapeSimpleRadical(operatorLoong)

class OperatorManager_ZM(OperatorManager):
	def __init__(self, descMgr):
		OperatorManager.__init__(self, descMgr)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDictForBuiltinOperator['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)
#		self.rearrangeInfoDictForBuiltinOperator['起']=RearrangeInfoLShapeSimpleRadical()


