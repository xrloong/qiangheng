from .CodeVarianceType import CodeVarianceType

class CodeInfo:
	def __init__(self, propDict):
		self.setDataEmpty()
		self.setSingleDataEmpty()

		self.codeVariance=CodeVarianceType()

		self.setRadixCodeProperties(propDict)

		hasCharacter=bool("字符碼" in propDict)
		hasRadix=bool("字根碼" in propDict)
		if hasCharacter or hasRadix:
			self._isSupportCharacterCode=False
			self._isSupportRadixCode=False
			if hasCharacter:
				self._isSupportCharacterCode=True
			if hasRadix:
				self._isSupportRadixCode=True
		else:
			self._isSupportCharacterCode=True
			self._isSupportRadixCode=True

	def __str__(self):
		return "{{{0}}}".format(self.getCode())

	def __repr__(self):
		return str(self)

	def isSupportCharacterCode(self):
		return self._isSupportCharacterCode

	def isSupportRadixCode(self):
		return self._isSupportRadixCode

	def setRadixCodeProperties(self, propDict):
		pass

	def getCodeVarianceType(self):
		return self.codeVariance

	def setDataEmpty(self):
		pass

	def setSingleDataEmpty(self):
		pass

	def multiplyCodeVarianceType(self, codeVariance):
		self.codeVariance.multi(codeVariance)

	@property
	def variance(self):
		return self.codeVariance.getVarianceByString()

	@property
	def characterCode(self):
		return None

