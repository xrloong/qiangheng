from parser.model import RadixCodeInfoModel

from .CodeVariance import CodeVariance

class RadixCodeInfoDescription:
	def __init__(self, model: RadixCodeInfoModel):
		self.__codeVariance = model.variance
		self.__isSupportRadixCode = model.isSupportRadixCode
		self.__codeElementCodeInfo = model.dict()

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

