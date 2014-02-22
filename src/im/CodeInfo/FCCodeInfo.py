from gear.CodeInfo import CodeInfo

class FCCodeInfo(CodeInfo):
	def setRadixCodeProperties(self, propDict):
		characterCode=propDict.get('資訊表示式', '')
		self.setCharacterCode(characterCode)

	@property
	def characterCode(self):
		return self.getCharacterCode()

	def getCharacterCode(self):
		return self._characterCode

	def setCharacterCode(self, characterCode):
		self._characterCode=characterCode

