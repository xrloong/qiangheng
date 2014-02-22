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
	def __init__(self, operatorManager):
		self.operatorManager=operatorManager
		self.templateDB=operatorManager.templateDB

	def rearrange(self, charDesc):
		self.operatorManager.getCharDescFromTemplate(charDesc)
		self.operatorManager.rearrangeRecursively(charDesc)

class OperatorManager:
	def __init__(self, descMgr):
		self.descMgr=descMgr
		self.templateDB={}

		operatorLoong=self.getOperatorByName('龍')
		self.rearrangeInfoDict={
			'龜':RearrangeInfoSame(),
			'爲':RearrangeInfoSame(),
			'錯':RearrangeInfoSame(),

			'蚕':RearrangeInfoSame(),
			'鴻':RearrangeInfoSame(),

			'起':RearrangeInfoSame(),
			'廖':RearrangeInfoSame(),
			'載':RearrangeInfoSame(),
			'聖':RearrangeInfoSame(),

			'回':RearrangeInfoSame(),
			'同':RearrangeInfoSame(),
			'函':RearrangeInfoSame(),
			'區':RearrangeInfoSame(),
			'左':RearrangeInfoSame(),
		}
		def operatorGenerator(operatorName):
			return Operator.Operator(operatorName)

		self.operatorGenerator=operatorGenerator

	def setTemplateDB(self, templateDB):
		self.templateDB=templateDB
		self.templateRearrangeInfo=RearrangeInfoTemplate(self)

	def getCharDescFromTemplate(self, charDesc):
		operator=charDesc.getOperator()
		compList=charDesc.getCompList()

		templateName=operator.getName()
		templateDesc=self.templateDB.get(templateName)

		resultDesc=templateDesc.getReplacedCharDesc(compList)
		resultDesc.setExpandName(charDesc.getExpandName())

		charDesc.setHanger(resultDesc.getHanger())

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
		return Operator.Operator(operatorName)

	def rearrangeDesc(self, charDesc):
		operator=charDesc.getOperator()
		rearrangeInfo=self.getRearrangeInfoByOperator(operator)

		if rearrangeInfo!=None:
			rearrangeInfo.rearrange(charDesc)

	def getRearrangeInfoByOperator(self, operator):
		if self.isTemplateOperator(operator):
			return self.templateRearrangeInfo
		else:
			operatorName=operator.getName()
			rearrangeInfo=self.rearrangeInfoDict.get(operatorName)
		return rearrangeInfo

	def adjustTemplate(self):
		pass

class OperatorManager_AR(OperatorManager):
	def __init__(self, descMgr):
		OperatorManager.__init__(self, descMgr)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical(operatorLoong)
		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)

class OperatorManager_BS(OperatorManager):
	def __init__(self, descMgr):
		OperatorManager.__init__(self, descMgr)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)
		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical(operatorLoong)

class OperatorManager_CJ(OperatorManager):
	def __init__(self, descMgr):
		OperatorManager.__init__(self, descMgr)

class OperatorManager_DY(OperatorManager):
	def __init__(self, descMgr):
		OperatorManager.__init__(self, descMgr)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)
		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical(operatorLoong)

class OperatorManager_ZM(OperatorManager):
	def __init__(self, descMgr):
		OperatorManager.__init__(self, descMgr)
		operatorLoong=self.getOperatorByName('龍')

		self.rearrangeInfoDict['函']=RearrangeInfoSurroundingOpenUp(operatorLoong)
#		self.rearrangeInfoDict['起']=RearrangeInfoLShapeSimpleRadical()


