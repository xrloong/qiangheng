class CodeVarianceType:
	CODE_TYPE_STANDARD=0
	CODE_TYPE_SIMPLIFIED=1
	CODE_TYPE_TOLERANT=2
	codeVarianceDict={
		CODE_TYPE_STANDARD:"標準",
		CODE_TYPE_SIMPLIFIED:"簡快",
		CODE_TYPE_TOLERANT:"容錯",
	}

	codeVarianceStringDict={
		"標準":CODE_TYPE_STANDARD,
		"簡快":CODE_TYPE_SIMPLIFIED,
		"容錯":CODE_TYPE_TOLERANT,
	}

	def __init__(self):
		self.codeVariance=CodeVarianceType.CODE_TYPE_STANDARD

	def setVariance(self, codeVariance):
		self.codeVariance=codeVariance

	def getVariance(self):
		return self.codeVariance

	def setVarianceByString(self, codeVarianceString):
		codeVariance=CodeVarianceType.codeVarianceStringDict.get(codeVarianceString, CodeVarianceType.CODE_TYPE_STANDARD)
		self.setVariance(codeVariance)

	def getVarianceByString(self):
		codeVariance=self.getVariance()
		codeVarianceString=CodeVarianceType.codeVarianceDict.get(codeVariance)
		return codeVarianceString

	def multi(self, xType):
		codeVariance=self.getVariance()
		if codeVariance<xType.getVariance():
			codeVariance=xType.getVariance()
		self.setVariance(codeVariance)

