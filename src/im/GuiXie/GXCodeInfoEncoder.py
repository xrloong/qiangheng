from .GXCodeInfo import GXCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder

class GXCodeInfoEncoder(CodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, characterCode):
		return GXCodeInfo.generateDefaultCodeInfo(characterCode)

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		isAllWithCode=all(map(lambda x: x.toCode(), codeInfoList))
		return isAllWithCode

	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """
		codeInfo=cls.generateDefaultCodeInfo('GGGG')
		return codeInfo

	@classmethod
	def encodeAsEast(cls, codeInfoList):
		"""運算 "東" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsEqual(cls, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

