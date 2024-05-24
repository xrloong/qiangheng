from enum import Enum

from parser import constant

class CodeVarianceType(Enum):
	STANDARD = (0, constant.VALUE_CODE_VARIANCE_TYPE_STANDARD)
	TOLERANT = (2, constant.VALUE_CODE_VARIANCE_TYPE_TOLERANT)

	@staticmethod
	def fromString(codeVarianceString):
		codeVarianceTypeDict = {
			constant.VALUE_CODE_VARIANCE_TYPE_STANDARD: CodeVarianceType.STANDARD,
			constant.VALUE_CODE_VARIANCE_TYPE_TOLERANT: CodeVarianceType.TOLERANT,
		}
		return codeVarianceTypeDict.get(codeVarianceString, CodeVarianceType.STANDARD)

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

