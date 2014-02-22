class Operator:
	availableOperation=[
		'龜', '水', '錯', '龍',
		'夾',
		'蚕', '鴻',
		'起', '廖', '載', '聖',
		'回', '同', '函', '區', '左',
		'好', '志', '算', '湘',
	]

	directionInfoList={
		'龜':'*',
		'龍':'*',
		'算':'|',
		'志':'|',
		'蚕':'|',
		'湘':'-',
		'好':'-',
		'鴻':'-',
		'載':'*',
		'廖':'*',
		'起':'*',
		'夾':'*',
		'回':'@',
		'同':'@',
		'函':'@',
		'區':'@',
		'左':'@',
		'水':'*',
	}

	def __init__(self, name='龜'):
		self.name=name

	def __str__(self):
		return "%s"%self.name

	def isAvailableOperation(self):
		return (self.getName() in Operator.availableOperation)

	def getName(self):
		return self.name

	def setName(self, name):
		self.name=name

	def getDirection(self):
		direction=Operator.directionInfoList.get(self.name, '*')
		return direction

class TemplateOperator(Operator):
	def __init(self, templateDescription):
		pass

