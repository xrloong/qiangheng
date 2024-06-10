from enum import StrEnum

class FontVariance(StrEnum):
	All = '全'
	Traditional = '傳'
	Simplified = '簡'

	def contains(self, other):
		return other.belongsTo(self)

	def belongsTo(self, targetFontVariance):
		match targetFontVariance:
			case FontVariance.All:
				return True
			case FontVariance.Traditional:
				return self in [FontVariance.All, FontVariance.Traditional]
			case FontVariance.Simplified:
				return self in [FontVariance.All, FontVariance.Simplified]
			case _:
				return False

class CodeVariance(StrEnum):
	STANDARD = "標準"
	SIMPLIFIED = "簡快"
	TOLERANT = "容錯"

	def __init__(self, *args, **kwds):
		self.__intValue = None

	def __mul__(self, other):
		if self.intValue < other.intValue:
			codeVariance = other
		else:
			codeVariance = self
		return codeVariance

	@property
	def intValue(self):
		if not self.__intValue:
			self.__intValue = self.__computeIntValue()
		return self.__intValue

	def __computeIntValue(self):
		match self:
			case CodeVariance.STANDARD: return 0
			case CodeVariance.SIMPLIFIED: return 1
			case CodeVariance.TOLERANT: return 2

