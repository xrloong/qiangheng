from . import Operator
import sys

class RearrangeInfoSame:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		pass

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

			'東':RearrangeInfoSame(),

			'蚕':RearrangeInfoSame(),
			'鴻':RearrangeInfoSame(),
			'回':RearrangeInfoSame(),


			'錯':RearrangeInfoSame(),
		}

		self.directionInfoList={
			'龜':'*',
			'爲':'*',
			'龍':'*',

			'東':'$',

			'蚕':'|',
			'鴻':'-',
			'回':'@',

			'錯':'*',
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

#OperatorManager_AR=OperatorManager
#OperatorManager_BS=OperatorManager
#OperatorManager_CJ=OperatorManager
#OperatorManager_DY=OperatorManager
#OperatorManager_ZM=OperatorManager

