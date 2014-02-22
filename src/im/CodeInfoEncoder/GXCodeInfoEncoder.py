from ..CodeInfo.GXCodeInfo import GXCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class GXCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfoEncoder.computeSupportingFromProperty(propDict)
		characterCode=propDict.get('資訊表示式', '')
		codeInfo=GXCodeInfo(isSupportCharacterCode, isSupportRadixCode)
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
		codeInfo.setCharacterCode('GGGG')
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

