class Operator:
	# 分成以下層級
	# SpecialCase:  錯、龜、爲
	# 橫、縱：鴻：不定個數橫向組同，蚕：不定個數縱向組合，龍：不定個數的組同。
	# Base:         好、志、湘、算
	# Surrounding:  回、同、區、函、左
	# LShape:       廖、載、聖、起
	# Insertion:    夾
	availableOperation=[
		'龜', '爲', '錯', '龍',
		'蚕', '鴻',
		'好', '志', '算', '湘',
		'夾', '起', '廖', '載', '聖',
		'回', '同', '函', '區', '左',
	]

	directionInfoList={
		'龜':'*',
		'爲':'*',
		'龍':'*',

		'算':'|',
		'志':'|',
		'蚕':'|',

		'湘':'-',
		'好':'-',
		'鴻':'-',

		'夾':'*',
		'載':'*',
		'廖':'*',
		'起':'*',
		'聖':'*',

		'回':'@',
		'同':'@',
		'函':'@',
		'區':'@',
		'左':'@',
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

