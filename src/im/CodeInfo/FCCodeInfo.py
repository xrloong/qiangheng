from gear.CodeInfo import CodeInfo

class FCCodeInfo(CodeInfo):
	STROKE_NONE=None
	STROKE_0='0'
	STROKE_1='1'
	STROKE_2='2'
	STROKE_3='3'
	STROKE_4='4'
	STROKE_5='5'
	STROKE_6='6'
	STROKE_7='7'
	STROKE_8='8'
	STROKE_9='9'

	STROKES=[
		STROKE_0,
		STROKE_1,
		STROKE_2,
		STROKE_3,
		STROKE_4,
		STROKE_5,
		STROKE_6,
		STROKE_7,
		STROKE_8,
		STROKE_9,
	]

	CORNER_NONE=None
	CORNER_TOP_LEFT='a'
	CORNER_TOP_RIGHT='b'
	CORNER_BOTTOM_LEFT='c'
	CORNER_BOTTOM_RIGHT='d'

	CORNERS=[
		CORNER_TOP_LEFT,
		CORNER_TOP_RIGHT,
		CORNER_BOTTOM_LEFT,
		CORNER_BOTTOM_RIGHT,
	]

	def __init__(self):
		CodeInfo.__init__(self)

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

