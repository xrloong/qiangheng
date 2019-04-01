from model.BaseCoding import CodingInfo
from model.BaseCoding import CodeInfo
from model.BaseCoding import CodeInfoEncoder
from model.BaseCoding import CodingRadixParser

class FourCornerInfo(CodingInfo):
	"四角號碼"

	IMName="四角"
	def __init__(self):
		self.keyMaps=[
			['0', '0',],
			['1', '1',],
			['2', '2',],
			['3', '3',],
			['4', '4',],
			['5', '5',],
			['6', '6',],
			['7', '7',],
			['8', '8',],
			['9', '9',],
			]
		self.nameDict={
				'cn':'四角',
				'tw':'四角',
				'hk':'四角',
				'en':'FourCourner',
				}
		self.iconfile="qhfc.svg"
		self.maxkeylength=4

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
		return self._top_left if self._top_left not in ['a', 'b', 'c'] else '0'

	def getTopRight(self):
		return self._top_right if self._top_right not in ['a', 'b', 'c'] else '0'

	def getBottomLeft(self):
		return self._bottom_left if self._bottom_left not in ['a', 'b', 'c'] else '0'

	def getBottomRight(self):
		return self._bottom_right if self._bottom_right not in ['a', 'b', 'c'] else '0'


class FCCodeInfoEncoder(CodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, corners):
		return FCCodeInfo.generateDefaultCodeInfo(corners)

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		return True


	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		print("不合法的運算：龜", file=sys.stderr)
		codeInfo=cls.encodeAsInvalidate(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """
		print("不合法的運算：龍", file=sys.stderr)
		codeInfo=cls.encodeAsInvalidate(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsSparrow(cls, codeInfoList):
		"""運算 "雀" """
		print("不合法的運算：雀", file=sys.stderr)
		codeInfo=cls.encodeAsInvalidate(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsEqual(cls, codeInfoList):
		"""運算 "爲" """
		targetCodeInfo=codeInfoList[0]
		corners=[targetCodeInfo.getTopLeft(),
			targetCodeInfo.getTopRight(),
			targetCodeInfo.getBottomLeft(),
			targetCodeInfo.getBottomRight() ]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo


	@classmethod
	def encodeAsLoop(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]
		grid=FCGrid()
		grid.setAsOut_In(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsSilkworm(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsTop_Bottom(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsGoose(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsLeft_Right(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsQi(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsBottomLeft_TopRight(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsLiao(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsTopLeft_BottomRight(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsZai(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsTopRight_BottomLeft(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsDou(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsBottomRight_TopLeft(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsMu(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsTop_BottomLeft_BottomRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsZuo(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_TopLeft_TopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsYou(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_InTopLeft_InTopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsLiang(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsTop_InBottomLeft_InBottomRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

	@classmethod
	def encodeAsJia(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_InTopLeft_InTopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=cls.generateDefaultCodeInfo(corners)
		return codeInfo

class FCBrick:
	TYPE_INVALIDATE=0
	TYPE_STROKE=1
	TYPE_REFERENCE=2
	def __init__(self):
		self.setAsInvalidate()
		self._usedByCorner=None

	def __str__(self):
		if self.isStroke():
			return "(1, %s)"%self.stroke
		elif self.isReference():
			return "(2, %s)"%self.wrapperBrick.getStroke()
		elif self.isInvalidate():
			return ""%FCCodeInfo.STROKE_NONE
		else:
			return ""%FCCodeInfo.STROKE_NONE

	def setAsInvalidate(self):
		self._type=FCBrick.TYPE_INVALIDATE

	def setAsStroke(self, stroke):
		self._type=FCBrick.TYPE_STROKE
		self.stroke=stroke

	def setAsReference(self, wrapperBrick):
		self._type=FCBrick.TYPE_REFERENCE
		self.wrapperBrick=wrapperBrick

	def isInvalidate(self):
		return self._type==FCBrick.TYPE_INVALIDATE

	def isStroke(self):
		return self._type==FCBrick.TYPE_STROKE

	def isReference(self):
		return self._type==FCBrick.TYPE_REFERENCE

	def setUsedByCorner(self, corner):
		if self.isReference():
			self.wrapperBrick.setUsedByCorner(corner)
			return
		self._usedByCorner=corner

	def isUsed(self):
		if self.isReference():
			return self.wrapperBrick.isUsed()
		return self.getUsedCorner()!=FCCodeInfo.CORNER_NONE

	def getUsedCorner(self):
		if self.isStroke():
			return self._usedByCorner
		elif self.isReference():
			return self.wrapperBrick.getUsedCorner()
		elif self.isInvalidate():
			return FCCodeInfo.CORNER_NONE
		else:
			return FCCodeInfo.CORNER_NONE

	def getStroke(self):
		if self.isStroke():
			return self.stroke
		elif self.isReference():
			return self.wrapperBrick.getStroke()
		elif self.isInvalidate():
			return FCCodeInfo.STROKE_NONE
		else:
			return FCCodeInfo.STROKE_NONE

class FCGrid:
	def __init__(self, width=4, height=4):
		self.width=width
		self.height=height

		self.grid=[[FCBrick() for j in range(self.width)] for i in range(self.height)]

	def setStrokeCodeOfCorner(self, brick, stroke, cornerInfoDict):
		if stroke in FCCodeInfo.STROKES:
			brick.setAsStroke(stroke)
		elif stroke in FCCodeInfo.CORNERS:
			referenceCorner=stroke
			[referenceX, referenceY, tmpStroke]=cornerInfoDict.get(referenceCorner)
			wrapperBrick=self.grid[referenceX][referenceY]
			brick.setAsReference(wrapperBrick)

	def setStrokeCode(self, cornerInfoDict):
		[x, y, stroke]=cornerInfoDict.get(FCCodeInfo.CORNER_TOP_LEFT)
		brick=self.grid[x][y]
		self.setStrokeCodeOfCorner(brick, stroke, cornerInfoDict)

		[x, y, stroke]=cornerInfoDict.get(FCCodeInfo.CORNER_TOP_RIGHT)
		brick=self.grid[x][y]
		self.setStrokeCodeOfCorner(brick, stroke, cornerInfoDict)

		[x, y, stroke]=cornerInfoDict.get(FCCodeInfo.CORNER_BOTTOM_LEFT)
		brick=self.grid[x][y]
		self.setStrokeCodeOfCorner(brick, stroke, cornerInfoDict)

		[x, y, stroke]=cornerInfoDict.get(FCCodeInfo.CORNER_BOTTOM_RIGHT)
		brick=self.grid[x][y]
		self.setStrokeCodeOfCorner(brick, stroke, cornerInfoDict)

	def getStrokeCodeOfCorner(self, x, y, corner):
		brick=self.grid[x][y]
		if brick.isUsed():
			ans=brick.getUsedCorner()
		else:
			ans=brick.getStroke()
		brick.setUsedByCorner(corner)
		return ans

	def getStrokeCode(self):
		top_left_stroke=self.getStrokeCodeOfCorner(0, 0, FCCodeInfo.CORNER_TOP_LEFT)
		top_right_stroke=self.getStrokeCodeOfCorner(3, 0, FCCodeInfo.CORNER_TOP_RIGHT)
		bottom_left_stroke=self.getStrokeCodeOfCorner(0, 3, FCCodeInfo.CORNER_BOTTOM_LEFT)
		bottom_right_stroke=self.getStrokeCodeOfCorner(3, 3, FCCodeInfo.CORNER_BOTTOM_RIGHT)

		return [top_left_stroke, top_right_stroke, bottom_left_stroke, bottom_right_stroke]

	def setAsLeft_Right(self, left, right):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, left.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[1, 0, left.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, left.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[1, 3, left.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[2, 0, right.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, right.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[2, 3, right.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, right.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTop_Bottom(self, top, bottom):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, top.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, top.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 1, top.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 1, top.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 2, bottom.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 2, bottom.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, bottom.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, bottom.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTopLeft_BottomRight(self, left, right):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, left.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, left.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, left.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[1, 3, left.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[2, 2, right.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 2, right.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[2, 3, right.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, right.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTopRight_BottomLeft(self, left, right):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, left.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, left.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[2, 3, left.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, left.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 2, right.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[1, 2, right.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, right.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[1, 3, right.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottomLeft_TopRight(self, left, right):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, left.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[1, 0, left.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, left.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, left.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[2, 0, right.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, right.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[2, 1, right.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 1, right.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottomRight_TopLeft(self, left, right):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[2, 0, left.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, left.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, left.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, left.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, right.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[1, 0, right.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 1, right.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[1, 1, right.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsOut_In(self, outer, inner):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, outer.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, outer.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, outer.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, outer.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[1, 1, inner.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[2, 1, inner.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[1, 2, inner.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[2, 2, inner.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTop_BottomLeft_BottomRight(self, first, second, third):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, first.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, first.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 1, first.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 1, first.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 2, second.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[1, 2, second.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, second.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[1, 3, second.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[2, 2, third.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 2, third.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[2, 3, third.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, third.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottom_TopLeft_TopRight(self, first, second, third):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 2, first.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 2, first.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, first.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, first.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, second.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[1, 0, second.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 1, second.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[1, 1, second.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[2, 0, third.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, third.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[2, 1, third.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 1, third.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTop_InBottomLeft_InBottomRight(self, first, second, third):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, first.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, first.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, first.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, first.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 1, second.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[1, 1, second.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 2, second.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[1, 2, second.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[2, 1, third.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 1, third.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[2, 2, third.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 2, third.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottom_InTopLeft_InTopRight(self, first, second, third):
		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 0, first.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 0, first.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 3, first.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 3, first.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[0, 1, second.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[1, 1, second.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[0, 2, second.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[1, 2, second.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCodeInfo.CORNER_TOP_LEFT:[2, 1, third.getTopLeft()],
			FCCodeInfo.CORNER_TOP_RIGHT:[3, 1, third.getTopRight()],
			FCCodeInfo.CORNER_BOTTOM_LEFT:[2, 2, third.getBottomLeft()],
			FCCodeInfo.CORNER_BOTTOM_RIGHT:[3, 2, third.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def getFourCorner(self):
		return self.getStrokeCode()

class FCRadixParser(CodingRadixParser):
	ATTRIB_CODE_EXPRESSION='資訊表示式'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict=elementCodeInfo

		top_left=''
		top_right=''
		bottom_left=''
		bottom_right=''

		characterCode=infoDict.get(FCRadixParser.ATTRIB_CODE_EXPRESSION)
		if len(characterCode)==4:
			top_left=characterCode[0]
			top_right=characterCode[1]
			bottom_left=characterCode[2]
			bottom_right=characterCode[3]

		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=FCCodeInfo(corners)
		return codeInfo

CodingInfo = FourCornerInfo
CodeInfoEncoder = FCCodeInfoEncoder
CodingRadixParser = FCRadixParser

