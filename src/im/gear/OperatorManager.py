from . import Operator
from . import RearrangeInfo
import sys

class OperatorManager:
	# 使用享元模式

	def __init__(self, imPackage):
		self.builtinOperatorDict={
			'龜':Operator.OperatorTurtle,
			'爲':Operator.OperatorEqual,
			'龍':Operator.OperatorLoong,
			'雀':Operator.OperatorSparrow,
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
			'瓥':Operator.OperatorLi,
			'粦':Operator.OperatorLin,

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

		self.operatorGenerator=operatorGenerator
		self.structureRearranger=imPackage.StructureRearranger()
		self.structureRearranger.setOperatorGenerator(operatorGenerator)


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
		for templateName, templateDesc in templateDB.items():
			rearrangeInfoTemplate=RearrangeInfo.RearrangeInfoTemplate(templateDesc)

			self.addTemplateOperatorIfNotExist(templateName)
			templateOperator=self.findTemplateOperator(templateName)
			templateOperator.setRearrangeInfo(rearrangeInfoTemplate)

	def getOperatorGenerator(self):
		return self.operatorGenerator

	def getStructureRearranger(self):
		return self.structureRearranger

	def rearrangeStructure(self, structDesc):
		self.structureRearranger.rearrangeOn(structDesc)

