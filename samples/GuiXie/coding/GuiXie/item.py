from coding.Base import CodeInfo

from .constant import GXStroke
from .constant import GXCorner

from .util import computeStrokeCode

class GXLump:
	cornerToIndexDict = {
		GXCorner.TopLeft: 0,
		GXCorner.TopRight: 1,
		GXCorner.BottomLeft: 2,
		GXCorner.BottomRight: 3,
	}

	def __init__(self, corners, rectCount=0):
		[self._top_left, self._top_right, self._bottom_left, self._bottom_right] = corners
		self._corners = corners
		self._rectCount = rectCount

	def computeStrokes(self, cornerCodes):
		strokes = []
		for cornerCode in cornerCodes:
			index = GXLump.cornerToIndexDict[cornerCode]
			stroke = self._corners[index]
			strokes.append(stroke)
		return strokes

	def computeStrokesOnAllCorners(self):
		return self.computeStrokes((GXCorner.TopLeft, GXCorner.TopRight, GXCorner.BottomLeft, GXCorner.BottomRight))

	def computeStrokesOnMainDiagonal(self):
		return self.computeStrokes((GXCorner.TopLeft, GXCorner.BottomRight))

	def computeStrokesOnAntiDiagonal(self):
		return self.computeStrokes((GXCorner.TopRight, GXCorner.BottomLeft))

	def computeAllStrokes(self):
		return self.computeStrokes((GXCorner.TopLeft, GXCorner.TopRight, GXCorner.BottomLeft, GXCorner.BottomRight))

	def computeCode(self, cornerCodes = (GXCorner.TopLeft, GXCorner.TopRight, GXCorner.BottomLeft, GXCorner.BottomRight)):
		strokes = self.computeStrokes(cornerCodes)
		return "".join(computeStrokeCode(stroke) for stroke in strokes)


	def computeCodesOnMainDiagonal(self):
		return self.computeCodes((GXCorner.TopLeft, GXCorner.BottomRight))

	def computeCodesOnAntiDiagonal(self):
		return self.computeCodes((GXCorner.TopRight, GXCorner.BottomLeft))

	def computeCodesOfTop(self):
		return self.computeCodes((GXCorner.TopLeft, GXCorner.TopRight))

	def computeCodesOfBottom(self):
		return self.computeCodes((GXCorner.BottomLeft, GXCorner.BottomRight))

	def computeCodesOfAll(self):
		return self.computeCodes((GXCorner.TopLeft, GXCorner.TopRight, GXCorner.BottomLeft, GXCorner.BottomRight))

	def computeCodes(self, positions):
		cornerToIndex = {
			GXCorner.TopLeft: 0,
			GXCorner.TopRight: 1,
			GXCorner.BottomLeft: 2,
			GXCorner.BottomRight: 3,
			}

		cornerToBrick = {}
		bricks = []
		for pos in positions:
			index = cornerToIndex[pos]
			stroke = self.getStroke(pos)

			if isinstance(stroke, GXStroke):
				brick = GXBrick.instanceForStroke(stroke)
				cornerToBrick[pos] = brick
			elif isinstance(stroke, GXCorner):
				corner = stroke
				if corner in cornerToBrick:
					wrapperBrick = cornerToBrick[corner]
					brick = GXBrick.instanceForReference(wrapperBrick)
				else:
					stroke = self.getStroke(corner)
					brick = GXBrick.instanceForStroke(stroke)
				cornerToBrick[corner] = brick
			else:
				brick = GXBrick.instanceForInvalidate()

			bricks.append(brick)

		codes = []
		for brick in bricks:
			stroke = brick.getStrokeOrCorner()
			codes.append(stroke)
			brick.setUsedByPosition()

		return tuple(codes)

	def getStroke(self, pos):
		stroke = GXStroke.StrokeNone
		if pos == GXCorner.TopLeft:
			stroke = self.topLeft
		elif pos == GXCorner.TopRight:
			stroke = self.topRight
		elif pos == GXCorner.BottomLeft:
			stroke = self.bottomLeft
		elif pos == GXCorner.BottomRight:
			stroke = self.bottomRight
		else:
			stroke = GXStroke.StrokeNone
		return stroke

	@property
	def corners(self):
		return (self.topLeft, self.topRight, self.bottomLeft, self.bottomRight)

	@property
	def topLeft(self):
		return self._top_left

	@property
	def topRight(self):
		return self._top_right

	@property
	def bottomLeft(self):
		return self._bottom_left

	@property
	def bottomRight(self):
		return self._bottom_right

	@property
	def rectCount(self):
		return self._rectCount

