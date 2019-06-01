from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

from .constant import FCStroke
from .constant import FCCorner

from .item import FCLump

from .util import convertCharToCornerUnit
from .util import computeCornerUnitCode

class FCCodeInfo(CodeInfo):
	def __init__(self, lump):
		super().__init__()

		self.lump = lump

	@staticmethod
	def generateDefaultCodeInfo(lump):
		codeInfo=FCCodeInfo(lump)
		return codeInfo

	def toCode(self):
		return "%s%s%s%s"%(self.topLeft, self.topRight, self.bottomLeft, self.bottomRight)

	@property
	def topLeft(self):
		return computeCornerUnitCode(self.getTopLeft())

	@property
	def topRight(self):
		return computeCornerUnitCode(self.getTopRight())

	@property
	def bottomLeft(self):
		return computeCornerUnitCode(self.getBottomLeft())

	@property
	def bottomRight(self):
		return computeCornerUnitCode(self.getBottomRight())

	def getTopLeft(self):
		return self.lump.topLeft

	def getTopRight(self):
		return self.lump.topRight

	def getBottomLeft(self):
		return self.lump.bottomLeft

	def getBottomRight(self):
		return self.lump.bottomRight


class FCCodeInfoEncoder(CodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, corners):
		lump = FCLump(corners)
		return FCCodeInfo.generateDefaultCodeInfo(lump)

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
		self._usedByCorner=FCCorner.CornerNone

	def __str__(self):
		if self.isStroke():
			return "(1, %s)"%self.stroke
		elif self.isReference():
			return "(2, %s)"%self.wrapperBrick.getStroke()
		elif self.isInvalidate():
			return "%s"%FCStroke.StrokeNone
		else:
			return "%s"%FCStroke.StrokeNone

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
		return self.getUsedCorner()!=FCCorner.CornerNone

	def getUsedCorner(self):
		if self.isStroke():
			return self._usedByCorner
		elif self.isReference():
			return self.wrapperBrick.getUsedCorner()
		elif self.isInvalidate():
			return FCCorner.CornerNone
		else:
			return FCCorner.CornerNone

	def getStroke(self):
		if self.isStroke():
			return self.stroke
		elif self.isReference():
			return self.wrapperBrick.getStroke()
		elif self.isInvalidate():
			return FCStroke.StrokeNone
		else:
			return FCStroke.StrokeNone

class FCGrid:
	def __init__(self, width=4, height=4):
		self.width=width
		self.height=height

		self.grid=[[FCBrick() for j in range(self.width)] for i in range(self.height)]

	def setStrokeCodeOfCorner(self, brick, stroke, cornerInfoDict):
		if isinstance(stroke, FCStroke):
			brick.setAsStroke(stroke)
		elif isinstance(stroke, FCCorner):
			referenceCorner=stroke
			[referenceX, referenceY, tmpStroke]=cornerInfoDict.get(referenceCorner)
			wrapperBrick=self.grid[referenceX][referenceY]
			brick.setAsReference(wrapperBrick)

	def setStrokeCode(self, cornerInfoDict):
		[x, y, stroke]=cornerInfoDict.get(FCCorner.TopLeft)
		brick=self.grid[x][y]
		self.setStrokeCodeOfCorner(brick, stroke, cornerInfoDict)

		[x, y, stroke]=cornerInfoDict.get(FCCorner.TopRight)
		brick=self.grid[x][y]
		self.setStrokeCodeOfCorner(brick, stroke, cornerInfoDict)

		[x, y, stroke]=cornerInfoDict.get(FCCorner.BottomLeft)
		brick=self.grid[x][y]
		self.setStrokeCodeOfCorner(brick, stroke, cornerInfoDict)

		[x, y, stroke]=cornerInfoDict.get(FCCorner.BottomRight)
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
		top_left_stroke=self.getStrokeCodeOfCorner(0, 0, FCCorner.TopLeft)
		top_right_stroke=self.getStrokeCodeOfCorner(3, 0, FCCorner.TopRight)
		bottom_left_stroke=self.getStrokeCodeOfCorner(0, 3, FCCorner.BottomLeft)
		bottom_right_stroke=self.getStrokeCodeOfCorner(3, 3, FCCorner.BottomRight)

		return [top_left_stroke, top_right_stroke, bottom_left_stroke, bottom_right_stroke]

	def setAsLeft_Right(self, left, right):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, left.getTopLeft()],
			FCCorner.TopRight:[1, 0, left.getTopRight()],
			FCCorner.BottomLeft:[0, 3, left.getBottomLeft()],
			FCCorner.BottomRight:[1, 3, left.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 0, right.getTopLeft()],
			FCCorner.TopRight:[3, 0, right.getTopRight()],
			FCCorner.BottomLeft:[2, 3, right.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, right.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTop_Bottom(self, top, bottom):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, top.getTopLeft()],
			FCCorner.TopRight:[3, 0, top.getTopRight()],
			FCCorner.BottomLeft:[0, 1, top.getBottomLeft()],
			FCCorner.BottomRight:[3, 1, top.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 2, bottom.getTopLeft()],
			FCCorner.TopRight:[3, 2, bottom.getTopRight()],
			FCCorner.BottomLeft:[0, 3, bottom.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, bottom.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTopLeft_BottomRight(self, left, right):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, left.getTopLeft()],
			FCCorner.TopRight:[3, 0, left.getTopRight()],
			FCCorner.BottomLeft:[0, 3, left.getBottomLeft()],
			FCCorner.BottomRight:[1, 3, left.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 2, right.getTopLeft()],
			FCCorner.TopRight:[3, 2, right.getTopRight()],
			FCCorner.BottomLeft:[2, 3, right.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, right.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTopRight_BottomLeft(self, left, right):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, left.getTopLeft()],
			FCCorner.TopRight:[3, 0, left.getTopRight()],
			FCCorner.BottomLeft:[2, 3, left.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, left.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 2, right.getTopLeft()],
			FCCorner.TopRight:[1, 2, right.getTopRight()],
			FCCorner.BottomLeft:[0, 3, right.getBottomLeft()],
			FCCorner.BottomRight:[1, 3, right.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottomLeft_TopRight(self, left, right):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, left.getTopLeft()],
			FCCorner.TopRight:[1, 0, left.getTopRight()],
			FCCorner.BottomLeft:[0, 3, left.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, left.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 0, right.getTopLeft()],
			FCCorner.TopRight:[3, 0, right.getTopRight()],
			FCCorner.BottomLeft:[2, 1, right.getBottomLeft()],
			FCCorner.BottomRight:[3, 1, right.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottomRight_TopLeft(self, left, right):
		cornerInfoDict={
			FCCorner.TopLeft:[2, 0, left.getTopLeft()],
			FCCorner.TopRight:[3, 0, left.getTopRight()],
			FCCorner.BottomLeft:[0, 3, left.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, left.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, right.getTopLeft()],
			FCCorner.TopRight:[1, 0, right.getTopRight()],
			FCCorner.BottomLeft:[0, 1, right.getBottomLeft()],
			FCCorner.BottomRight:[1, 1, right.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsOut_In(self, outer, inner):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, outer.getTopLeft()],
			FCCorner.TopRight:[3, 0, outer.getTopRight()],
			FCCorner.BottomLeft:[0, 3, outer.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, outer.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[1, 1, inner.getTopLeft()],
			FCCorner.TopRight:[2, 1, inner.getTopRight()],
			FCCorner.BottomLeft:[1, 2, inner.getBottomLeft()],
			FCCorner.BottomRight:[2, 2, inner.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTop_BottomLeft_BottomRight(self, first, second, third):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, first.getTopLeft()],
			FCCorner.TopRight:[3, 0, first.getTopRight()],
			FCCorner.BottomLeft:[0, 1, first.getBottomLeft()],
			FCCorner.BottomRight:[3, 1, first.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 2, second.getTopLeft()],
			FCCorner.TopRight:[1, 2, second.getTopRight()],
			FCCorner.BottomLeft:[0, 3, second.getBottomLeft()],
			FCCorner.BottomRight:[1, 3, second.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 2, third.getTopLeft()],
			FCCorner.TopRight:[3, 2, third.getTopRight()],
			FCCorner.BottomLeft:[2, 3, third.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, third.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottom_TopLeft_TopRight(self, first, second, third):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 2, first.getTopLeft()],
			FCCorner.TopRight:[3, 2, first.getTopRight()],
			FCCorner.BottomLeft:[0, 3, first.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, first.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, second.getTopLeft()],
			FCCorner.TopRight:[1, 0, second.getTopRight()],
			FCCorner.BottomLeft:[0, 1, second.getBottomLeft()],
			FCCorner.BottomRight:[1, 1, second.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 0, third.getTopLeft()],
			FCCorner.TopRight:[3, 0, third.getTopRight()],
			FCCorner.BottomLeft:[2, 1, third.getBottomLeft()],
			FCCorner.BottomRight:[3, 1, third.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTop_InBottomLeft_InBottomRight(self, first, second, third):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, first.getTopLeft()],
			FCCorner.TopRight:[3, 0, first.getTopRight()],
			FCCorner.BottomLeft:[0, 3, first.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, first.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 1, second.getTopLeft()],
			FCCorner.TopRight:[1, 1, second.getTopRight()],
			FCCorner.BottomLeft:[0, 2, second.getBottomLeft()],
			FCCorner.BottomRight:[1, 2, second.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 1, third.getTopLeft()],
			FCCorner.TopRight:[3, 1, third.getTopRight()],
			FCCorner.BottomLeft:[2, 2, third.getBottomLeft()],
			FCCorner.BottomRight:[3, 2, third.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottom_InTopLeft_InTopRight(self, first, second, third):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, first.getTopLeft()],
			FCCorner.TopRight:[3, 0, first.getTopRight()],
			FCCorner.BottomLeft:[0, 3, first.getBottomLeft()],
			FCCorner.BottomRight:[3, 3, first.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 1, second.getTopLeft()],
			FCCorner.TopRight:[1, 1, second.getTopRight()],
			FCCorner.BottomLeft:[0, 2, second.getBottomLeft()],
			FCCorner.BottomRight:[1, 2, second.getBottomRight()],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 1, third.getTopLeft()],
			FCCorner.TopRight:[3, 1, third.getTopRight()],
			FCCorner.BottomLeft:[2, 2, third.getBottomLeft()],
			FCCorner.BottomRight:[3, 2, third.getBottomRight()],
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
			top_left = convertCharToCornerUnit(characterCode[0])
			top_right = convertCharToCornerUnit(characterCode[1])
			bottom_left = convertCharToCornerUnit(characterCode[2])
			bottom_right = convertCharToCornerUnit(characterCode[3])

		corners = [top_left, top_right, bottom_left, bottom_right]
		fcLump = FCLump(corners)
		codeInfo = FCCodeInfo(fcLump)
		return codeInfo

