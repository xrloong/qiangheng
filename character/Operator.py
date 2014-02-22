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

class TemplateOperator(Operator):
	def __init(self, templateDescription):
		pass

