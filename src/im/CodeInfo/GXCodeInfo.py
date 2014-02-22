from gear.CodeInfo import CodeInfo

class GXCodeInfo(CodeInfo):
	def __init__(self, characterCode, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

	def getCharacterCode(self):
		return self._characterCode

