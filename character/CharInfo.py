
class CharInfo:
	class CharInfoProp:
		def __init__(self):
			pass

	def __init__(self, propDict={}):
		self.setFlag=False

	def __str__(self):
#		return "{{{0}}}".format(self.charname)
		return "{{{0}}}".format(self.getCode())

	def __repr__(self):
		return str(self)

	def isToSetTree(self):
		# 若非空且之前没設過值
		return (not self.setFlag)

	def setByComps(self, operator, complist):
		# 多型
		# 計算倉頡碼時，需要知道此字的組成方向
		# 計算行列、大易、嘸蝦米及鄭碼時，不需要知道此字的組成方向
		pass

	def getCode(self):
		#多型
		return ""

