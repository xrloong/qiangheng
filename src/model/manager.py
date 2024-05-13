from injector import inject

from .element import Operator

class OperatorManager:
	# 使用享元模式

	@inject
	def __init__(self):
		self.builtinOperatorDict={
			'龜':Operator.OperatorTurtle,
			'龍':Operator.OperatorLoong,
			'雀':Operator.OperatorSparrow,
			'爲':Operator.OperatorEqual,

			'蚕':Operator.OperatorSilkworm,
			'鴻':Operator.OperatorGoose,
			'回':Operator.OperatorLoop,

			'起':Operator.OperatorQi,
			'這':Operator.OperatorZhe,
			'廖':Operator.OperatorLiao,
			'載':Operator.OperatorZai,
			'斗':Operator.OperatorDou,

			'同':Operator.OperatorTong,
			'區':Operator.OperatorQu,
			'函':Operator.OperatorHan,
			'左':Operator.OperatorLeft,

			'畞':Operator.OperatorMu,
			'㘴':Operator.OperatorZuo,
			'幽':Operator.OperatorYou,
			'㒳':Operator.OperatorLiang,
			'夾':Operator.OperatorJia,

			'䜌':Operator.OperatorLuan,
			'辦':Operator.OperatorBan,
			'粦':Operator.OperatorLin,
			'瓥':Operator.OperatorLi,
			'燚':Operator.OperatorYi,
		}
		self.templateOperatorDict={
		}

	def generateOperator(self, operatorName):
		if operatorName in self.builtinOperatorDict:
			operator=self.builtinOperatorDict.get(operatorName)
		else:
			if operatorName not in self.templateOperatorDict:
				operator=Operator.Operator(operatorName)
				self.templateOperatorDict[operatorName]=operator
			operator=self.templateOperatorDict.get(operatorName)
		return operator

