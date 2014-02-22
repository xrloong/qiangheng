class Operator:
	def __init__(self, name, direction):
		self.name=name
		self.direction=direction

	def __str__(self):
		return "%s"%self.name

	def getName(self):
		return self.name

	def setName(self, name):
		self.name=name

	def getDirection(self):
		return self.direction

class BuiltinOperator:
	def __init__(self, name, direction):
		Operator.__init__(self, name, direction)

class TemplateOperator(Operator):
	def __init(self, templateDescription):
		pass

# 龜
# 爲
# 龍東
# 蚕鴻回
# 起廖載聖
# 同函區左
# 衍衷瓥粦
# 錯

OperatorSilkWorm=BuiltinOperator('蚕', '|')
OperatorGoose=BuiltinOperator('鴻', '-')

