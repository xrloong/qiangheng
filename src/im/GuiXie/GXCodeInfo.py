from ..base.CodeInfo import CodeInfo

class GXCodeInfo(CodeInfo):
	def __init__(self, characterCode):
		super().__init__()

	@staticmethod
	def generateDefaultCodeInfo(characterCode):
		codeInfo=GXCodeInfo(characterCode)
		return codeInfo

	def toCode(self):
		return ""

