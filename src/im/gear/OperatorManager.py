from . import Operator
from . import RearrangeInfo
import sys


class OperatorManager:
	def __init__(self, descMgr):
		self.descMgr=descMgr
		self.templateDB={}

		self.builtinOperatorDict={
			'龜':Operator.OperatorTurtle,
			'爲':Operator.OperatorEqual,
			'龍':Operator.OperatorLoong,
			'東':Operator.OperatorEast,
			'蚕':Operator.OperatorSilkworm,
			'鴻':Operator.OperatorGoose,
			'回':Operator.OperatorLoop,

			'起':Operator.OperatorQi,
			'廖':Operator.OperatorLiao,
			'載':Operator.OperatorZai,
			'斗':Operator.OperatorDou,

			'同':Operator.OperatorTong,
			'函':Operator.OperatorHan,
			'區':Operator.OperatorQu,
			'左':Operator.OperatorLeft,

			'衍':Operator.OperatorYan,
			'衷':Operator.OperatorZhong,
			'瓥':Operator.OperatorGridShape,
			'粦':Operator.OperatorTriangleShape,

			'畞':Operator.OperatorMu,
			'㘴':Operator.OperatorZuo,
			'幽':Operator.OperatorYou,
			'㒳':Operator.OperatorLiang,
			'夾':Operator.OperatorJia,
		}
		self.templateOperatorDict={
		}

		def operatorGenerator(operatorName):
			if operatorName in self.builtinOperatorDict:
				operator=self.builtinOperatorDict.get(operatorName)
			else:
				self.addTemplateOperatorIfNotExist(operatorName)
				operator=self.findTemplateOperator(operatorName)
			return operator

		operatorLoong=operatorGenerator('龍')
		self.operatorGenerator=operatorGenerator

	def addTemplateOperatorIfNotExist(self, templateName):
		if templateName in self.templateOperatorDict:
			operator=self.templateOperatorDict[templateName]
		else:
			operator=Operator.TemplateOperator(templateName)
			self.templateOperatorDict[templateName]=operator

	def findTemplateOperator(self, templateName):
		templateOperator=self.templateOperatorDict.get(templateName)
		return templateOperator

	def setTemplateDB(self, templateDB):
		self.templateDB=templateDB
		for templateName, templateDesc in templateDB.items():
			rearrangeInfoTemplate=RearrangeInfo.RearrangeInfoTemplate(templateDesc)

			self.addTemplateOperatorIfNotExist(templateName)
			templateOperator=self.findTemplateOperator(templateName)
			templateOperator.setRearrangeInfo(rearrangeInfoTemplate)

	def getOperatorGenerator(self):
		return self.operatorGenerator

	def rearrangeRecursively(self, charDesc):
		self.rearrangeDesc(charDesc)
		for childDesc in charDesc.getCompList():
			self.rearrangeRecursively(childDesc)
		return charDesc

	def rearrangeDesc(self, charDesc):
		operator=charDesc.getOperator()
		rearrangeInfo=operator.getRearrangeInfo()

		if rearrangeInfo!=None:
			rearrangeInfo.rearrange(charDesc)
			operator=charDesc.getOperator()
			if not operator.isBuiltin():
				self.rearrangeDesc(charDesc)

