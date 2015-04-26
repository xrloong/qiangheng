from model.base.CodeInfo import CodeInfo

class SPCodeInfo(CodeInfo):
	def __init__(self):
		super().__init__()

	@staticmethod
	def generateDefaultCodeInfo(characterCode):
		codeInfo=SPCodeInfo(characterCode)
		return codeInfo

	def toCode(self):
		return ""

