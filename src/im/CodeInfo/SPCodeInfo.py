from gear.CodeInfo import CodeInfo

class SPCodeInfo(CodeInfo):
	def __init__(self):
		CodeInfo.__init__(self)

	@staticmethod
	def generateDefaultCodeInfo(characterCode):
		codeInfo=SPCodeInfo(characterCode)
		return codeInfo

	def toCode(self):
		return ""

