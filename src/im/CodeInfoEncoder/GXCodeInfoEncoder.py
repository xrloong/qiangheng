from ..CodeInfo.GXCodeInfo import GXCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class GXCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=GXCodeInfo(propDict, codeVariance)
		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getCharacterCode(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfo, codeInfoList):
		"""運算 "龜" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsLoong(self, codeInfo, codeInfoList):
		"""運算 "龍" """

		codeInfo.setCharacterCode('GGGG')

	def encodeAsEast(self, codeInfo, codeInfoList):
		"""運算 "東" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsEqual(self, codeInfo, codeInfoList):
		"""運算 "爲" """
		self.encodeAsLoong(codeInfo, codeInfoList)
