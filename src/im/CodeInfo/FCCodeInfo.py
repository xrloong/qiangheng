from gear.CodeInfo import CodeInfo

class FCCodeInfo(CodeInfo):
	def setRadixCodeProperties(self, propDict):
		self._top_left=''
		self._top_right=''
		self._bottom_left=''
		self._bottom_right=''

		characterCode=propDict.get('資訊表示式', '')
		if len(characterCode)==4:
			self._top_left=characterCode[0]
			self._top_right=characterCode[1]
			self._bottom_left=characterCode[2]
			self._bottom_right=characterCode[3]
#		self.setCharacterCode(characterCode)

	@property
	def characterCode(self):
		return self.getCharacterCode()

	def getCharacterCode(self):
		return "%s%s%s%s"%(self._top_left, self._top_right, self._bottom_left, self._bottom_right)
#		return self._characterCode

	def setCode(self, topLeft, topRight, bottomLeft, bottomRight):
		self._top_left=topLeft
		self._top_right=topRight
		self._bottom_left=bottomLeft
		self._bottom_right=bottomRight

	def getTopLeft(self):
		return self._top_left

	def getTopRight(self):
		return self._top_right

	def getBottomLeft(self):
		return self._bottom_left

	def getBottomRight(self):
		return self._bottom_right

#	def setCharacterCode(self, characterCode):
#		self._characterCode=characterCode

