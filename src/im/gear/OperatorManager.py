import Constant

from . import Operator
from gear import TreeRegExp
import yaml

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

			'燚':Operator.OperatorYi,
		}
		self.templateOperatorDict={
		}

		self.templatePatternDict={
		}

		self.substitutePatternList=[]

	def generateOperatorTurtle(self):
		return self.generateOperator()

	def generateOperator(self, operatorName):
		if operatorName in self.builtinOperatorDict:
			operator=self.builtinOperatorDict.get(operatorName)
		else:
			self.addTemplateOperatorIfNotExist(operatorName)
			operator=self.findTemplateOperator(operatorName)
		return operator

	def addTemplateOperatorIfNotExist(self, templateName):
		if templateName not in self.templateOperatorDict:
			operator=Operator.Operator(templateName)
			self.templateOperatorDict[templateName]=operator

	def findTemplateOperator(self, templateName):
		templateOperator=self.templateOperatorDict.get(templateName)
		return templateOperator

	def loadTemplates(self, toTemplateFile):
		node=yaml.load(open(toTemplateFile), yaml.CLoader)
		templatePatternDict={}
		templateGroupNode=node.get(Constant.TAG_TEMPLATE_SET)
		for node in templateGroupNode:
			templateName=node.get(Constant.TAG_NAME)
			matchPattern=node.get(Constant.TAG_MATCH)
			replacePattern=node.get(Constant.TAG_PATTERN)
			tre=TreeRegExp.compile(matchPattern)

			templatePatternDict[templateName]=[tre, replacePattern]

		self.templatePatternDict=templatePatternDict

	def loadSubstituteRules(self, toSubstituteFile):
		rootNode=yaml.load(open(toSubstituteFile))
		ruleSetNode=rootNode.get(Constant.TAG_RULE_SET)
		self.substitutePatternList=[]

		if not ruleSetNode:
			return

		for node in ruleSetNode:
			matchPattern=node.get(Constant.TAG_MATCH)
			resultPattern=node.get(Constant.TAG_SUBSTITUTE)
			self.substitutePatternList.append([TreeRegExp.compile(matchPattern), resultPattern])

	def getTemplatePatternList(self):
		return list(self.templatePatternDict.values())

	def getSubstitutePatternList(self):
		return self.substitutePatternList

