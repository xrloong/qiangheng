
class CharInfo:
	def __init__(self, charname, prop):
		self.charname=charname

		self.showFlag=False if len(self.charname)>1 else True
		self.setFlag=False

	def __str__(self):
		return "{{{0}}}".format(self.charname)

	def __repr__(self):
		return str(self)

	def isToShow(self):
		return self.showFlag

	def isToSetTree(self):
		# 若非空且之前没設過值
		return (not self.setFlag)

	def setByComps(self, complist, direction):
		# 多型
		# 計算倉頡碼時，需要知道此字的組成方向
		# 計算行列、大易、嘸蝦米及鄭碼時，不需要知道此字的組成方向
		pass

	def getCode(self):
		#多型
		return ""

NoneChar=CharInfo('[瑲珩預設空字符]', [])
NoneChar.noneFlag=True

