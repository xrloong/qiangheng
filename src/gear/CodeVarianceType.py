import Constant

class CodeVarianceType:
	CODE_TYPE_STANDARD=0
	CODE_TYPE_SIMPLIFIED=1
	CODE_TYPE_TOLERANT=2
	codeVarianceDict={
		CODE_TYPE_STANDARD:Constant.VALUE_CODE_VARIANCE_TYPE_STANDARD,
		CODE_TYPE_SIMPLIFIED:Constant.VALUE_CODE_VARIANCE_TYPE_SIMPLIFIED,
		CODE_TYPE_TOLERANT:Constant.VALUE_CODE_VARIANCE_TYPE_TOLERANT,
	}

	codeVarianceStringDict={
		Constant.VALUE_CODE_VARIANCE_TYPE_STANDARD:CODE_TYPE_STANDARD,
		Constant.VALUE_CODE_VARIANCE_TYPE_SIMPLIFIED:CODE_TYPE_SIMPLIFIED,
		Constant.VALUE_CODE_VARIANCE_TYPE_TOLERANT:CODE_TYPE_TOLERANT,
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

