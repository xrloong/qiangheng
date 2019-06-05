from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

from .constant import FCStroke
from .constant import FCCorner

from .item import FCLump

from .util import convertCornerCodeToCornerUnits
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
		return "%s%s%s%s"%(computeCornerUnitCode(self.topLeft),
				computeCornerUnitCode(self.topRight),
				computeCornerUnitCode(self.bottomLeft),
				computeCornerUnitCode(self.bottomRight))

	@property
	def topLeft(self):
		return self.lump.topLeft

	@property
	def topRight(self):
		return self.lump.topRight

	@property
	def bottomLeft(self):
		return self.lump.bottomLeft

	@property
	def bottomRight(self):
		return self.lump.bottomRight


class FCCodeInfoEncoder(CodeInfoEncoder):
	def generateDefaultCodeInfo(self, corners):
		lump = FCLump(corners)
		return FCCodeInfo.generateDefaultCodeInfo(lump)

	def isAvailableOperation(self, codeInfoList):
		return True


	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		print("不合法的運算：龜", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """
		print("不合法的運算：龍", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsSparrow(self, codeInfoList):
		"""運算 "雀" """
		print("不合法的運算：雀", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		targetCodeInfo=codeInfoList[0]
		corners=[targetCodeInfo.topLeft,
			targetCodeInfo.topRight,
			targetCodeInfo.bottomLeft,
			targetCodeInfo.bottomRight ]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo


	def encodeAsLoop(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]
		grid=FCGrid()
		grid.setAsOut_In(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsTop_Bottom(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsLeft_Right(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsQi(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsBottomLeft_TopRight(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsLiao(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsTopLeft_BottomRight(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsTopRight_BottomLeft(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsDou(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsBottomRight_TopLeft(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsMu(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsTop_BottomLeft_BottomRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsZuo(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_TopLeft_TopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsYou(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_InTopLeft_InTopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsTop_InBottomLeft_InBottomRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsJia(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_InTopLeft_InTopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
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
			FCCorner.TopLeft:[0, 0, left.topLeft],
			FCCorner.TopRight:[1, 0, left.topRight],
			FCCorner.BottomLeft:[0, 3, left.bottomLeft],
			FCCorner.BottomRight:[1, 3, left.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 0, right.topLeft],
			FCCorner.TopRight:[3, 0, right.topRight],
			FCCorner.BottomLeft:[2, 3, right.bottomLeft],
			FCCorner.BottomRight:[3, 3, right.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTop_Bottom(self, top, bottom):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, top.topLeft],
			FCCorner.TopRight:[3, 0, top.topRight],
			FCCorner.BottomLeft:[0, 1, top.bottomLeft],
			FCCorner.BottomRight:[3, 1, top.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 2, bottom.topLeft],
			FCCorner.TopRight:[3, 2, bottom.topRight],
			FCCorner.BottomLeft:[0, 3, bottom.bottomLeft],
			FCCorner.BottomRight:[3, 3, bottom.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTopLeft_BottomRight(self, left, right):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, left.topLeft],
			FCCorner.TopRight:[3, 0, left.topRight],
			FCCorner.BottomLeft:[0, 3, left.bottomLeft],
			FCCorner.BottomRight:[1, 3, left.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 2, right.topLeft],
			FCCorner.TopRight:[3, 2, right.topRight],
			FCCorner.BottomLeft:[2, 3, right.bottomLeft],
			FCCorner.BottomRight:[3, 3, right.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTopRight_BottomLeft(self, left, right):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, left.topLeft],
			FCCorner.TopRight:[3, 0, left.topRight],
			FCCorner.BottomLeft:[2, 3, left.bottomLeft],
			FCCorner.BottomRight:[3, 3, left.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 2, right.topLeft],
			FCCorner.TopRight:[1, 2, right.topRight],
			FCCorner.BottomLeft:[0, 3, right.bottomLeft],
			FCCorner.BottomRight:[1, 3, right.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottomLeft_TopRight(self, left, right):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, left.topLeft],
			FCCorner.TopRight:[1, 0, left.topRight],
			FCCorner.BottomLeft:[0, 3, left.bottomLeft],
			FCCorner.BottomRight:[3, 3, left.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 0, right.topLeft],
			FCCorner.TopRight:[3, 0, right.topRight],
			FCCorner.BottomLeft:[2, 1, right.bottomLeft],
			FCCorner.BottomRight:[3, 1, right.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottomRight_TopLeft(self, left, right):
		cornerInfoDict={
			FCCorner.TopLeft:[2, 0, left.topLeft],
			FCCorner.TopRight:[3, 0, left.topRight],
			FCCorner.BottomLeft:[0, 3, left.bottomLeft],
			FCCorner.BottomRight:[3, 3, left.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, right.topLeft],
			FCCorner.TopRight:[1, 0, right.topRight],
			FCCorner.BottomLeft:[0, 1, right.bottomLeft],
			FCCorner.BottomRight:[1, 1, right.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsOut_In(self, outer, inner):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, outer.topLeft],
			FCCorner.TopRight:[3, 0, outer.topRight],
			FCCorner.BottomLeft:[0, 3, outer.bottomLeft],
			FCCorner.BottomRight:[3, 3, outer.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[1, 1, inner.topLeft],
			FCCorner.TopRight:[2, 1, inner.topRight],
			FCCorner.BottomLeft:[1, 2, inner.bottomLeft],
			FCCorner.BottomRight:[2, 2, inner.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTop_BottomLeft_BottomRight(self, first, second, third):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, first.topLeft],
			FCCorner.TopRight:[3, 0, first.topRight],
			FCCorner.BottomLeft:[0, 1, first.bottomLeft],
			FCCorner.BottomRight:[3, 1, first.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 2, second.topLeft],
			FCCorner.TopRight:[1, 2, second.topRight],
			FCCorner.BottomLeft:[0, 3, second.bottomLeft],
			FCCorner.BottomRight:[1, 3, second.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 2, third.topLeft],
			FCCorner.TopRight:[3, 2, third.topRight],
			FCCorner.BottomLeft:[2, 3, third.bottomLeft],
			FCCorner.BottomRight:[3, 3, third.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottom_TopLeft_TopRight(self, first, second, third):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 2, first.topLeft],
			FCCorner.TopRight:[3, 2, first.topRight],
			FCCorner.BottomLeft:[0, 3, first.bottomLeft],
			FCCorner.BottomRight:[3, 3, first.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, second.topLeft],
			FCCorner.TopRight:[1, 0, second.topRight],
			FCCorner.BottomLeft:[0, 1, second.bottomLeft],
			FCCorner.BottomRight:[1, 1, second.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 0, third.topLeft],
			FCCorner.TopRight:[3, 0, third.topRight],
			FCCorner.BottomLeft:[2, 1, third.bottomLeft],
			FCCorner.BottomRight:[3, 1, third.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsTop_InBottomLeft_InBottomRight(self, first, second, third):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, first.topLeft],
			FCCorner.TopRight:[3, 0, first.topRight],
			FCCorner.BottomLeft:[0, 3, first.bottomLeft],
			FCCorner.BottomRight:[3, 3, first.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 1, second.topLeft],
			FCCorner.TopRight:[1, 1, second.topRight],
			FCCorner.BottomLeft:[0, 2, second.bottomLeft],
			FCCorner.BottomRight:[1, 2, second.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 1, third.topLeft],
			FCCorner.TopRight:[3, 1, third.topRight],
			FCCorner.BottomLeft:[2, 2, third.bottomLeft],
			FCCorner.BottomRight:[3, 2, third.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def setAsBottom_InTopLeft_InTopRight(self, first, second, third):
		cornerInfoDict={
			FCCorner.TopLeft:[0, 0, first.topLeft],
			FCCorner.TopRight:[3, 0, first.topRight],
			FCCorner.BottomLeft:[0, 3, first.bottomLeft],
			FCCorner.BottomRight:[3, 3, first.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[0, 1, second.topLeft],
			FCCorner.TopRight:[1, 1, second.topRight],
			FCCorner.BottomLeft:[0, 2, second.bottomLeft],
			FCCorner.BottomRight:[1, 2, second.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

		cornerInfoDict={
			FCCorner.TopLeft:[2, 1, third.topLeft],
			FCCorner.TopRight:[3, 1, third.topRight],
			FCCorner.BottomLeft:[2, 2, third.bottomLeft],
			FCCorner.BottomRight:[3, 2, third.bottomRight],
		}
		self.setStrokeCode(cornerInfoDict)

	def getFourCorner(self):
		return self.getStrokeCode()

class FCRadixParser(CodingRadixParser):
	ATTRIB_CODE_EXPRESSION='編碼表示式'
	ATTRIB_ARCHITECTURE='結構'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo = radixInfo.getCodeElement()

		cornerCodeList = elementCodeInfo.get(FCRadixParser.ATTRIB_ARCHITECTURE)
		corners = tuple(convertCornerCodeToCornerUnits(cornerCode) for cornerCode in cornerCodeList)

		fcLump = FCLump(corners[0])
		codeInfo = FCCodeInfo(fcLump)
		return codeInfo

