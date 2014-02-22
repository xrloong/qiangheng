from . import RearrangeInfo

class Operator:
	def __init__(self, name, direction):
		self.name=name
		self.direction=direction
		self.rearrangeInfo=None

	def __str__(self):
		return "%s"%self.name

	def equals(self, other):
		return self.getName()==other.getName()

	def getName(self):
		return self.name

	def setName(self, name):
		self.name=name

	def getDirection(self):
		return self.direction

	def getRearrangeInfo(self):
		return self.rearrangeInfo

	def isBuiltin(self):
		return False

class BuiltinOperator(Operator):
	def __init__(self, name, direction, rearrangeInfo):
		Operator.__init__(self, name, direction)
		self.rearrangeInfo=rearrangeInfo

	def getRearrangeInfo(self):
		return self.rearrangeInfo

	def isBuiltin(self):
		return True

class TemplateOperator(Operator):
	def __init__(self, name, direction):
		Operator.__init__(self, name, direction)
		self.rearrangeInfo=None

	def setRearrangeInfo(self, rearrangeInfo):
		self.rearrangeInfo=rearrangeInfo

# 龜
# 爲
# 龍東
# 蚕鴻回
# 起廖載斗
# 同函區左
# 衍衷瓥粦
# 錯

OperatorTurtle=BuiltinOperator('龜', '*', RearrangeInfo.RearrangeInfoSame())
OperatorEqual=BuiltinOperator('爲', '*', RearrangeInfo.RearrangeInfoSame())
OperatorLoong=BuiltinOperator('龍', '*', RearrangeInfo.RearrangeInfoSame())
OperatorEast=BuiltinOperator('東', '$', RearrangeInfo.RearrangeInfoSame())
OperatorSilkworm=BuiltinOperator('蚕', '|', RearrangeInfo.RearrangeInfoSame())
OperatorGoose=BuiltinOperator('鴻', '-', RearrangeInfo.RearrangeInfoSame())
OperatorLoop=BuiltinOperator('回', '@', RearrangeInfo.RearrangeInfoSame())

OperatorQi=BuiltinOperator('起', '*', RearrangeInfo.RearrangeInfoSame())
OperatorLiao=BuiltinOperator('廖', '*', RearrangeInfo.RearrangeInfoSame())
OperatorZai=BuiltinOperator('載', '*', RearrangeInfo.RearrangeInfoSame())
OperatorDou=BuiltinOperator('斗', '*', RearrangeInfo.RearrangeInfoSame())

OperatorTong=BuiltinOperator('同', '*', RearrangeInfo.RearrangeInfoSame())
OperatorHan=BuiltinOperator('函', '*', RearrangeInfo.RearrangeInfoSame())
OperatorQu=BuiltinOperator('區', '*', RearrangeInfo.RearrangeInfoSame())
OperatorZuo=BuiltinOperator('左', '*', RearrangeInfo.RearrangeInfoSame())

OperatorYan=BuiltinOperator('衍', '*', RearrangeInfo.RearrangeInfoSame())
OperatorZhong=BuiltinOperator('衷', '*', RearrangeInfo.RearrangeInfoSame())
OperatorGridShape=BuiltinOperator('瓥', '*', RearrangeInfo.RearrangeInfoSame())
OperatorTriangleShape=BuiltinOperator('粦', '*', RearrangeInfo.RearrangeInfoSame())

