from ..CodeInfo.GXCodeInfo import GXCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder
from gear.CodeInfo import CodeInfo

class GXCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, characterCode):
		return GXCodeInfo.generateDefaultCodeInfo(characterCode)

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=GXCodeInfo.generateCodeInfo(propDict)
		codeInfo.multiplyCodeVarianceType(codeVariance)
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
		codeInfo=self.generateDefaultCodeInfo('GGGG')
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

