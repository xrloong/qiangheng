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

			'好':RearrangeInfoSame(),
			'志':RearrangeInfoSame(),
			'算':RearrangeInfoSame(),
			'湘':RearrangeInfoSame(),
		}
		def operatorGenerator(operatorName):
			return Operator.Operator(operatorName)

		self.operatorGenerator=operatorGenerator

	def isTemplateName(self, operatorName):
		return (operatorName in self.templateDB.keys())

	def setTemplateDB(self, templateDB):
		self.templateDB=templateDB

	def getCharDescFromTemplate(self, charDesc):
		operator=charDesc.getOperator()
		compList=charDesc.getCompList()

		templateName=operator.getName()
		templateDesc=self.templateDB.get(templateName)

		resultDesc=templateDesc.getReplacedCharDesc(compList)
		resultDesc.setExpandName(charDesc.getExpandName())
		return resultDesc

	def getOperatorGenerator(self):
		return self.operatorGenerator

	def isTemplateOperator(self, operator):
		return len(operator.getName())>1

	def rearrangeRecursively(self, charDesc):
		if self.isTemplateOperator(charDesc.getOperator()):
			charDesc=self.getCharDescFromTemplate(charDesc)
			charDesc=self.rearrangeRecursively(charDesc)
		l=[]
		for childDesc in charDesc.getCompList():
			newChildDesc=self.rearrangeRecursively(childDesc)
			l.append(newChildDesc)
		charDesc.setCompList(l)
		self.rearrangeDesc(charDesc)
		return charDesc

	def getOperatorByName(self, operatorName):
		return Operator.Operator(operatorName)

	def rearrangeDesc(self, charDesc):
		operator=charDesc.getOperator()
		operatorName=operator.getName()
		rearrangeInfo=self.rearrangeInfoDict.get(operatorName)

		if rearrangeInfo!=None:
			rearrangeInfo.rearrange(charDesc)

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


