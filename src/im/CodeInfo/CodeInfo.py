from description.CodeType import CodeType

class CodeInfo:
	def __init__(self, propDict={}):
		self.setDataEmpty()
		self.setSingleDataEmpty()

		self.codeType=CodeType()
		self.setRadixCodeProperties(propDict)

	def __str__(self):
		return "{{{0}}}".format(self.getCode())

	def __repr__(self):
		return str(self)

	def setRadixCodeProperties(self, propDict):
		pass

	def setCompositions(self, operator, complist):
		# 計算倉頡碼時，需要知道此字的組成方向
		# 計算行列、大易、嘸蝦米及鄭碼時，不需要知道此字的組成方向
		for codeInfo in complist:
			codeType=codeInfo.getCodeType()
			self.codeType.multi(codeType)

		self.setByComps(operator, complist)

	def setByComps(self, operator, complist):
		pass

	def getCodeType(self):
		return self.codeType

	def getCodeProperties(self):
		characterCode=self.characterCode
		if characterCode:
			return [characterCode, self.codeType.getTypeString()]
		else:
			return []

	def setDataEmpty(self):
		pass

	def setSingleDataEmpty(self):
		pass

	def multiCodeType(self, codeType):
		self.codeType.multi(codeType)

	@property
	def code(self):
		return self.characterCode

	@property
	def characterCode(self):
		return None

	@property
	def radixCode(self):
		return None

