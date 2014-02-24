from . import RearrangeInfo

class Operator:
	def __init__(self, name):
		self.name=name
		self.rearrangeInfo=RearrangeInfo.RearrangeInfoSame()

	def __str__(self):
		return "%s"%self.name

	def equals(self, other):
		return self.getName()==other.getName()

	def getName(self):
		return self.name

	def setName(self, name):
		self.name=name

	def getRearrangeInfo(self):
		return self.rearrangeInfo

	def isBuiltin(self):
		return False

class BuiltinOperator(Operator):
	def getRearrangeInfo(self):
		return self.rearrangeInfo

	def isBuiltin(self):
		return True

class TemplateOperator(Operator):
	def __init__(self, name):
		super().__init__(name)
		self.rearrangeInfo=None

	def setRearrangeInfo(self, rearrangeInfo):
		self.rearrangeInfo=rearrangeInfo

	def isBuiltin(self):
		return False

# 龜
# 爲
# 龍雀
# 蚕鴻回
# 起廖載斗
# 同函區左
# 衍衷瓥粦
# 錯

OperatorTurtle=BuiltinOperator('龜')
OperatorLoong=BuiltinOperator('龍')
OperatorEast=BuiltinOperator('雀')
OperatorEqual=BuiltinOperator('爲')

OperatorSilkworm=BuiltinOperator('蚕')
OperatorGoose=BuiltinOperator('鴻')
OperatorLoop=BuiltinOperator('回')

OperatorQi=BuiltinOperator('起')
OperatorZhe=BuiltinOperator('這')
OperatorLiao=BuiltinOperator('廖')
OperatorZai=BuiltinOperator('載')
OperatorDou=BuiltinOperator('斗')

OperatorTong=BuiltinOperator('同')
OperatorHan=BuiltinOperator('函')
OperatorQu=BuiltinOperator('區')
OperatorLeft=BuiltinOperator('左')

OperatorYan=BuiltinOperator('衍')
OperatorZhong=BuiltinOperator('衷')

OperatorMu=BuiltinOperator('畞')
OperatorZuo=BuiltinOperator('㘴')
OperatorYou=BuiltinOperator('幽')
OperatorLiang=BuiltinOperator('㒳')
OperatorJia=BuiltinOperator('夾')

OperatorLin=BuiltinOperator('粦')
OperatorLi=BuiltinOperator('瓥')
OperatorLuan=BuiltinOperator('䜌')
OperatorBan=BuiltinOperator('辦')

