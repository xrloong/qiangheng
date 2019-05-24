from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

class GXCodeInfo(CodeInfo):
	def __init__(self):
		super().__init__()

	@staticmethod
	def generateDefaultCodeInfo():
		return GXCodeInfo()

	def toCode(self):
		return ""

class GXCodeInfoEncoder(CodeInfoEncoder):
	def generateDefaultCodeInfo(self):
		return GXCodeInfo.generateDefaultCodeInfo()

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.toCode(), codeInfoList))
		return isAllWithCode

class GXRadixParser(CodingRadixParser):
	def convertRadixDescToCodeInfo(self, radixDesc):
		return GXCodeInfo.generateDefaultCodeInfo()

