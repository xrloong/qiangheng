from gear.CodeInfo import CodeInfo

class GXCodeInfo(CodeInfo):
	def __init__(self, characterCode, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

	def getCharacterCode(self):
		return self._characterCode

	@staticmethod
	def generateCodeInfo(propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupportingFromProperty(propDict)
		characterCode=propDict.get('資訊表示式', '')

		codeInfo=GXCodeInfo(characterCode, isSupportCharacterCode, isSupportRadixCode)
		return codeInfo

