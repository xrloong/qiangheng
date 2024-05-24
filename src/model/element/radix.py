from .CodeVariance import CodeVariance

class RadixCodeInfoDescription:
	def __init__(self, variance: CodeVariance, isSupportRadixCode: bool, codeElementCodeInfo):
		self.__codeVariance = variance
		self.__isSupportRadixCode = isSupportRadixCode
		self.__codeElementCodeInfo = codeElementCodeInfo

	@property
	def codeVariance(self):
		return self.__codeVariance

	@property
	def isSupportRadixCode(self):
		return self.__isSupportRadixCode

	@property
	def codeElement(self):
		return self.__codeElementCodeInfo

class RadixDescription:
	def __init__(self, radixName, radixCodeInfoList):
		self.radixName = radixName
		self.radixCodeInfoList = radixCodeInfoList

	def getRadixName(self):
		return self.radixName

	def getRadixCodeInfoDescriptionList(self):
		return self.radixCodeInfoList

	def getRadixCodeInfoDescription(self, index):
		if index in range(leng(self.radixCodeInfoList)):
			return self.radixCodeInfoList[index]

