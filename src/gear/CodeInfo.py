from .CodeVarianceType import CodeVarianceType

class CodeInfo:
	def __init__(self, propDict, codeVariance):
		self.setDataEmpty()
		self.setSingleDataEmpty()

		self.codeVariance=CodeVarianceType()
		self.codeVariance.multi(codeVariance)
#		self.codeVariance=codeVariance

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

	def encode(self, operator, complist):
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

