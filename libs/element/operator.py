class Operator:
	def __init__(self, name):
		self.__name = name

	def __str__(self):
		return self.__name

	def __eq__(self, other):
		return self.name == other.name

	@property
	def name(self):
		return self.__name

	@staticmethod
	def generateBuiltin(operatorName):
		return Operator(operatorName)

# 龜
# 爲
# 龍雀
# 蚕鴻回
# 起廖載斗
# 同函區左
# 衍衷瓥粦
# 錯

OperatorTurtle = Operator.generateBuiltin('龜')
OperatorLoong = Operator.generateBuiltin('龍')
OperatorSparrow = Operator.generateBuiltin('雀')
OperatorEqual = Operator.generateBuiltin('爲')

OperatorSilkworm = Operator.generateBuiltin('蚕')
OperatorGoose = Operator.generateBuiltin('鴻')
OperatorLoop = Operator.generateBuiltin('回')

OperatorQi = Operator.generateBuiltin('起')
OperatorZhe = Operator.generateBuiltin('這')
OperatorLiao = Operator.generateBuiltin('廖')
OperatorZai = Operator.generateBuiltin('載')
OperatorDou = Operator.generateBuiltin('斗')

OperatorTong = Operator.generateBuiltin('同')
OperatorHan = Operator.generateBuiltin('函')
OperatorQu = Operator.generateBuiltin('區')
OperatorLeft = Operator.generateBuiltin('左')

OperatorMu = Operator.generateBuiltin('畞')
OperatorZuo = Operator.generateBuiltin('㘴')
OperatorYou = Operator.generateBuiltin('幽')
OperatorLiang = Operator.generateBuiltin('㒳')
OperatorJia = Operator.generateBuiltin('夾')

OperatorLuan = Operator.generateBuiltin('䜌')
OperatorBan = Operator.generateBuiltin('辦')
OperatorLin = Operator.generateBuiltin('粦')
OperatorLi = Operator.generateBuiltin('瓥')
OperatorYi = Operator.generateBuiltin('燚')

