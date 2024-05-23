from parser import constant

class CodeVarianceType:
	CODE_TYPE_STANDARD = 0
	CODE_TYPE_TOLERANT = 2

	codeVarianceDict = {
		CODE_TYPE_STANDARD: constant.VALUE_CODE_VARIANCE_TYPE_STANDARD,
		CODE_TYPE_TOLERANT: constant.VALUE_CODE_VARIANCE_TYPE_TOLERANT,
	}

	codeVarianceStringDict = {
		constant.VALUE_CODE_VARIANCE_TYPE_STANDARD: CODE_TYPE_STANDARD,
		constant.VALUE_CODE_VARIANCE_TYPE_TOLERANT: CODE_TYPE_TOLERANT,
	}

	def __init__(self, codeVariance):
		self.codeVariance = codeVariance
		self.codeVarianceString = CodeVarianceType.codeVarianceDict.get(codeVariance)

	def __mul__(self, other):
		codeVariance = self.getVariance()
		if codeVariance<other.getVariance():
			codeVariance = other.getVariance()
		return CodeVarianceTypeFactory.generate(codeVariance)

	def getVariance(self):
		return self.codeVariance

	def getVarianceByString(self):
		return self.codeVarianceString

class CodeVarianceTypeFactory:
	# 使用享元模式

	def __init__(self):
		codeVarianceTypeStandard = CodeVarianceType(CodeVarianceType.CODE_TYPE_STANDARD)
		codeVarianceTypeTolerant = CodeVarianceType(CodeVarianceType.CODE_TYPE_TOLERANT)
		self.codeVarianceTypeDict = {
			CodeVarianceType.CODE_TYPE_STANDARD: codeVarianceTypeStandard,
			CodeVarianceType.CODE_TYPE_TOLERANT: codeVarianceTypeTolerant,
		}

	@staticmethod
	def generate(codeVarianceType = CodeVarianceType.CODE_TYPE_STANDARD):
		return CodeVarianceTypeFactory._factory.codeVarianceTypeDict[codeVarianceType]

	@staticmethod
	def generateByString(codeVarianceString):
		codeVariance = CodeVarianceType.codeVarianceStringDict.get(codeVarianceString, CodeVarianceType.CODE_TYPE_STANDARD)
		return CodeVarianceTypeFactory.generate(codeVariance)

CodeVarianceTypeFactory._factory = CodeVarianceTypeFactory()

