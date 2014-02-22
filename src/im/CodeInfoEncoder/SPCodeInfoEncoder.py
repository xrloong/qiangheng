from ..CodeInfo.SPCodeInfo import SPCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class SPCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfoEncoder.computeSupportingFromProperty(propDict)
		codeInfo=SPCodeInfo(isSupportCharacterCode, isSupportRadixCode)
		codeInfo.setRadixCodeProperties(propDict)
		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getCharacterCode(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """
		codeInfo=self.generateDefaultCodeInfo()
		codeInfo.setCharacterCode('YYYY')
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

