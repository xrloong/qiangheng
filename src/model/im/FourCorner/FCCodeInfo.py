from model.base.CodeInfo import CodeInfo

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

	def __init__(self, corners):
		super().__init__()
		[self._top_left, self._top_right, self._bottom_left, self._bottom_right]=corners

	@staticmethod
	def generateDefaultCodeInfo(corners):
		codeInfo=FCCodeInfo(corners)
		return codeInfo

	def toCode(self):
		return "%s%s%s%s"%(self.getTopLeft(), self.getTopRight(), self.getBottomLeft(), self.getBottomRight())

	def getTopLeft(self):
		return self._top_left

	def getTopRight(self):
		return self._top_right

	def getBottomLeft(self):
		return self._bottom_left

	def getBottomRight(self):
		return self._bottom_right
