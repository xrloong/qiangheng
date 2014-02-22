from gear.CodeInfo import CodeInfo

class SPCodeInfo(CodeInfo):
	def __init__(self, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

	@staticmethod
	def generateCodeInfo(propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupportingFromProperty(propDict)
		characterCode=propDict.get('資訊表示式', '')

		codeInfo=SPCodeInfo(characterCode, isSupportCharacterCode, isSupportRadixCode)
		return codeInfo

	@property
	def characterCode(self):
		return self.getCharacterCode()

	def getCharacterCode(self):
		return self._characterCode

