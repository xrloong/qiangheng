from .CodeVarianceType import CodeVarianceType

class CodeInfo:
	def __init__(self, isSupportCharacterCode=True, isSupportRadixCode=True):
		self.codeVariance=CodeVarianceType()
		self._isSupportCharacterCode=isSupportCharacterCode
		self._isSupportRadixCode=isSupportRadixCode

	@staticmethod
	def computeSupportingFromProperty(propDict):
		hasCharacter=bool("字符碼" in propDict)
		hasRadix=bool("字根碼" in propDict)

		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupporting(hasCharacter, hasRadix)
		return [isSupportCharacterCode, isSupportRadixCode]

	@staticmethod
	def computeSupporting(hasCharacter, hasRadix):
		if hasCharacter or hasRadix:
			isSupportCharacterCode=False
			isSupportRadixCode=False
			if hasCharacter:
				isSupportCharacterCode=True
			if hasRadix:
				isSupportRadixCode=True
		else:
			isSupportCharacterCode=True
			isSupportRadixCode=True
		return [isSupportCharacterCode, isSupportRadixCode]

	def __str__(self):
		return "{{{0}}}".format(self.getCode())

	def __repr__(self):
		return str(self)

	def isSupportCharacterCode(self):
		return self._isSupportCharacterCode

	def isSupportRadixCode(self):
		return self._isSupportRadixCode

	def getCodeVarianceType(self):
		return self.codeVariance

	def multiplyCodeVarianceType(self, codeVariance):
		self.codeVariance.multi(codeVariance)

	@property
	def variance(self):
		return self.codeVariance.getVarianceByString()

	@property
	def characterCode(self):
		return None

