from enum import Enum

from parser import constant

class CodeVariance(Enum):
	STANDARD = (0, constant.VALUE_CODE_VARIANCE_TYPE_STANDARD)
	TOLERANT = (2, constant.VALUE_CODE_VARIANCE_TYPE_TOLERANT)

	@staticmethod
	def fromString(codeVarianceString):
		codeVarianceDict = {
			constant.VALUE_CODE_VARIANCE_TYPE_STANDARD: CodeVariance.STANDARD,
			constant.VALUE_CODE_VARIANCE_TYPE_TOLERANT: CodeVariance.TOLERANT,
		}
		return codeVarianceDict.get(codeVarianceString, CodeVariance.STANDARD)

	def __init__(self, value, strValue):
		self.__value = value
		self.__strValue = strValue

	def __mul__(self, other):
		if self.value < other.value:
			codeVariance = other
		else:
			codeVariance = self
		return codeVariance

	@property
	def strValue(self):
		return self.__strValue

