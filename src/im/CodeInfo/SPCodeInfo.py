from gear.CodeInfo import CodeInfo

class SPCodeInfo(CodeInfo):
	def __init__(self, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

	@property
	def characterCode(self):
		return self.getCharacterCode()

	def getCharacterCode(self):
		return self._characterCode

