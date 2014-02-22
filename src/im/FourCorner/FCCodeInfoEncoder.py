from .FCCodeInfo import FCCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder
from ..base.CodeInfo import CodeInfo

import sys

class FCCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, corners):
		return FCCodeInfo.generateDefaultCodeInfo(corners)

	def isAvailableOperation(self, codeInfoList):
		return True

	def encodeAsTurtle(self, codeInfoList):
		print("不合法的運算：龜", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		print("不合法的運算：龍", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		print("不合法的運算：東", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		targetCodeInfo=codeInfoList[0]
		corners=[targetCodeInfo.getTopLeft(),
			targetCodeInfo.getTopRight(),
			targetCodeInfo.getBottomLeft(),
			targetCodeInfo.getBottomRight() ]
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
		# 以 "㘴" 來說 first: 口，second: 人，third: 土
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_TopLeft_TopRight(thirdCodeInfo, firstCodeInfo, secondCodeInfo)
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

	def encodeAsYin(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]
		grid=FCGrid()
		grid.setAsOut_In(firstCodeInfo, lastCodeInfo)
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
		self._usedByCorner=None

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
		self._usedByCorner=corner

	def isUsed(self):
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

