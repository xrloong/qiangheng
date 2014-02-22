class CodeInfo:
	def __init__(self, propDict={}):
		self.setDataEmpty()
		self.setSingleDataEmpty()

		self.setPropDict(propDict)

	def __str__(self):
#		return "{{{0}}}".format(self.charname)
		return "{{{0}}}".format(self.getCode())

	def __repr__(self):
		return str(self)

	def setPropDict(self, propDict):
		pass

	def setByComps(self, operator, complist):
		# 多型
		# 計算倉頡碼時，需要知道此字的組成方向
		# 計算行列、大易、嘸蝦米及鄭碼時，不需要知道此字的組成方向
		pass

	def getCode(self):
		code=self.code
		if code: return code

	def setDataEmpty(self):
		self.dataInitialized=False

	def setSingleDataEmpty(self):
		pass

	def setDataInitialized(self):
		self.dataInitialized=True

	def isDataInitialized(self):
		return self.dataInitialized

	def isToSetTree(self):
		# 若非空且之前没設過值
		return (not self.isDataInitialized())

