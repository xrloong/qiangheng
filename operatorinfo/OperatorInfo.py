
class OperatorInfo:
	def __init__(self, direction):
#		self.name=name
		self.direction=direction

	def getName(self):
		return self.name

	def getDirection(self):
		return self.direction

Arbitrary=OperatorInfo('+')
Surrounding=OperatorInfo('@')
Horizontal=OperatorInfo('-')
Vertical=OperatorInfo('|')

