class Operator:
	def __init__(self, name, builtin=False):
		self.name=name
		self.builtin=builtin

	def __str__(self):
		return self.name

	def equals(self, other):
		return self.getName()==other.getName()

	def getName(self):
		return self.name

	def setName(self, name):
		self.name=name

	def isBuiltin(self):
		return self.builtin

def _generateBuiltinOperator(operatorName):
	return Operator(operatorName, builtin=True)

# 龜
# 爲
# 龍雀
# 蚕鴻回
# 起廖載斗
# 同函區左
# 衍衷瓥粦
# 錯

OperatorTurtle=_generateBuiltinOperator('龜')
OperatorLoong=_generateBuiltinOperator('龍')
OperatorSparrow=_generateBuiltinOperator('雀')
OperatorEqual=_generateBuiltinOperator('爲')

OperatorSilkworm=_generateBuiltinOperator('蚕')
OperatorGoose=_generateBuiltinOperator('鴻')
OperatorLoop=_generateBuiltinOperator('回')

OperatorQi=_generateBuiltinOperator('起')
OperatorZhe=_generateBuiltinOperator('這')
OperatorLiao=_generateBuiltinOperator('廖')
OperatorZai=_generateBuiltinOperator('載')
OperatorDou=_generateBuiltinOperator('斗')

OperatorTong=_generateBuiltinOperator('同')
OperatorHan=_generateBuiltinOperator('函')
OperatorQu=_generateBuiltinOperator('區')
OperatorLeft=_generateBuiltinOperator('左')

OperatorMu=_generateBuiltinOperator('畞')
OperatorZuo=_generateBuiltinOperator('㘴')
OperatorYou=_generateBuiltinOperator('幽')
OperatorLiang=_generateBuiltinOperator('㒳')
OperatorJia=_generateBuiltinOperator('夾')

OperatorLuan=_generateBuiltinOperator('䜌')
OperatorBan=_generateBuiltinOperator('辦')
OperatorLin=_generateBuiltinOperator('粦')
OperatorLi=_generateBuiltinOperator('瓥')
OperatorYi=_generateBuiltinOperator('燚')

