from state import StateManager

class HanZiCodeInfo:
	def __init__(self, propDict, codeVariance,):
		codeInfo=StateManager.codeInfoGenerator(propDict)
		self.codeInfo=codeInfo
		self.codeInfo.multiCodeVarianceType(codeVariance)

		hasCharacter=bool("字符碼" in propDict)
		hasRadix=bool("字根碼" in propDict)
		if hasCharacter or hasRadix:
			self._isSupportCharacterCode=False
			self._isSupportRadixCode=False
			if hasCharacter:
				self._isSupportCharacterCode=True
			if hasRadix:
				self._isSupportRadixCode=True
		else:
			self._isSupportCharacterCode=True
			self._isSupportRadixCode=True

	def isSupportCharacterCode(self):
		return self._isSupportCharacterCode

	def isSupportRadixCode(self):
		return self._isSupportRadixCode

	def setRadixCodeProperties(self, propDict):
		self.codeInfo.setRadixCodeProperties(propDict)
		pass

	def setCompositions(self, operator, complist):
		tmpCompList=[comp.codeInfo for comp in complist]
		self.codeInfo.setCompositions(operator, tmpCompList)

	def getCodeVarianceType(self):
		return self.codeInfo.getCodeVarianceType()

	def getCodeProperties(self):
		return self.codeInfo.getCodeProperties()

