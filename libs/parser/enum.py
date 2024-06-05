from enum import IntEnum, StrEnum

from parser import constant

class CodingType(IntEnum):
	Input = 1
	Drawing = 2

class FontVariance(StrEnum):
	All = '全'
	Traditional = '傳'
	Simplified = '簡'

class CodeVariance(IntEnum):
	STANDARD = 0
	TOLERANT = 2

	def __init__(self, *args, **kwds):
		self.__strValue = None

	@staticmethod
	def fromString(codeVarianceString):
		codeVarianceDict = {
			constant.VALUE_CODE_VARIANCE_TYPE_STANDARD: CodeVariance.STANDARD,
			constant.VALUE_CODE_VARIANCE_TYPE_TOLERANT: CodeVariance.TOLERANT,
		}
		return codeVarianceDict.get(codeVarianceString, CodeVariance.STANDARD)

	def __mul__(self, other):
		if self.value < other.value:
			codeVariance = other
		else:
			codeVariance = self
		return codeVariance

	@property
	def strValue(self):
		if not self.__strValue:
			self.__strValue = self.__computeStrValue()
		return self.__strValue

	def __computeStrValue(self):
		match self:
			case CodeVariance.STANDARD: return constant.VALUE_CODE_VARIANCE_TYPE_STANDARD
			case CodeVariance.TOLERANT: return constant.VALUE_CODE_VARIANCE_TYPE_TOLERANT

