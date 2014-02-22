class CodeInfo:
	def __init__(self, propDict={}):
		self.setDataEmpty()
		self.setSingleDataEmpty()

		self.setRadixCodeProperties(propDict)

	def __str__(self):
		return "{{{0}}}".format(self.getCode())

	def __repr__(self):
		return str(self)

	def setRadixCodeProperties(self, propDict):
		pass

	def setByComps(self, operator, complist):
		# 多型
		# 計算倉頡碼時，需要知道此字的組成方向
		# 計算行列、大易、嘸蝦米及鄭碼時，不需要知道此字的組成方向
		pass

	def getCode(self):
		characterCode=self.characterCode
		if characterCode:
			return characterCode

	def setDataEmpty(self):
		pass

	def setSingleDataEmpty(self):
		pass

	@property
	def code(self):
		return self.characterCode

	@property
	def characterCode(self):
		return None

	@property
	def radixCode(self):
		return None

