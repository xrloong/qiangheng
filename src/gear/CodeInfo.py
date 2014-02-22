from .CodeVarianceType import CodeVarianceType

class CodeInfo:
	def __init__(self, propDict={}):
		self.setDataEmpty()
		self.setSingleDataEmpty()

		self.codeVariance=CodeVarianceType()
		self.setRadixCodeProperties(propDict)

	def __str__(self):
		return "{{{0}}}".format(self.getCode())

	def __repr__(self):
		return str(self)

	def setRadixCodeProperties(self, propDict):
		pass

	def setCompositions(self, operator, complist):
		for codeInfo in complist:
			codeVariance=codeInfo.getCodeVarianceType()
			self.codeVariance.multi(codeVariance)

		self.setByComps(operator, complist)

	def setByComps(self, operator, complist):
		pass

	def getCodeVarianceType(self):
		return self.codeVariance

	def getCodeProperties(self):
		characterCode=self.characterCode
		if characterCode:
			return [characterCode, self.codeVariance.getVarianceByString()]
		else:
			return []

	def setDataEmpty(self):
		pass

	def setSingleDataEmpty(self):
		pass

	def multiCodeVarianceType(self, codeVariance):
		self.codeVariance.multi(codeVariance)

	@property
	def code(self):
		return self.characterCode

	@property
	def characterCode(self):
		return None

