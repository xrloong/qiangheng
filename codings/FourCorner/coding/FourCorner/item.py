from .constant import FCStroke
from .constant import FCCorner

class FCLump:
	def __init__(self, obj, sl = False):
		self.sl = sl
		if isinstance(obj, FCLump):
			lump = obj
			self.sl = lump.sl
			self._top_left = lump.topLeft
			self._top_right = lump.topRight
			self._bottom_left = lump.bottomLeft
			self._bottom_right = lump.bottomRight
		elif isinstance(obj, (list, tuple)):
			corners = obj
			_top_left, _top_right, _bottom_left, _bottom_right = corners
			self._top_left = _top_left
			self._top_right = _top_right
			self._bottom_left = _bottom_left
			self._bottom_right = _bottom_right

	def computeCodesOfTopLeft(self):
		return self.computeCodes((FCCorner.TopLeft, ))

	def computeCodesOfTopRight(self):
		return self.computeCodes((FCCorner.TopRight, ))

	def computeCodesOfBottomLeft(self):
		return self.computeCodes((FCCorner.BottomLeft, ))

	def computeCodesOfBottomRight(self):
		return self.computeCodes((FCCorner.BottomRight, ))

	def computeCodesOfTop(self):
		return self.computeCodes((FCCorner.TopLeft, FCCorner.TopRight))

	def computeCodesOfBottom(self):
		return self.computeCodes((FCCorner.BottomLeft, FCCorner.BottomRight))

	def computeCodesOfLeft(self):
		return self.computeCodes((FCCorner.TopLeft, FCCorner.BottomLeft))

	def computeCodesOfRight(self):
		return self.computeCodes((FCCorner.TopRight, FCCorner.BottomRight))

	def computeCodesOfExceptTopLeft(self):
		return self.computeCodes((FCCorner.TopRight, FCCorner.BottomLeft, FCCorner.BottomRight))

	def computeCodesOfExceptTopRight(self):
		return self.computeCodes((FCCorner.TopLeft, FCCorner.BottomLeft, FCCorner.BottomRight))

	def computeCodesOfExceptBottomLeft(self):
		return self.computeCodes((FCCorner.TopLeft, FCCorner.TopRight, FCCorner.BottomRight))

	def computeCodesOfExceptBottomRight(self):
		return self.computeCodes((FCCorner.TopLeft, FCCorner.TopRight, FCCorner.BottomLeft))

	def computeCodesOfAll(self):
		return self.computeCodes((FCCorner.TopLeft, FCCorner.TopRight, FCCorner.BottomLeft, FCCorner.BottomRight))

	def computeCodes(self, positions):
		cornerToIndex = {
			FCCorner.TopLeft: 0,
			FCCorner.TopRight: 1,
			FCCorner.BottomLeft: 2,
			FCCorner.BottomRight: 3,
			}

		cornerToBrick = {}
		bricks = []
		for pos in positions:
			index = cornerToIndex[pos]
			stroke = self.getStroke(pos)

			brick = FCBrick(pos)
			if isinstance(stroke, FCStroke):
				brick.setAsStroke(stroke)
				cornerToBrick[pos] = brick
			elif isinstance(stroke, FCCorner):
				corner = stroke
				if corner in cornerToBrick:
					wrapperBrick = cornerToBrick[corner]
					brick.setAsReference(wrapperBrick)
				else:
					stroke = self.getStroke(corner)
					brick.setAsStroke(stroke)
				cornerToBrick[corner] = brick

			bricks.append(brick)

		codes = []
		for brick in bricks:
			stroke = brick.getStrokeOrCorner()
			codes.append(stroke)
			brick.setUsedByPosition()

		return tuple(codes)

	def getStroke(self, pos):
		stroke = FCStroke.StrokeNone
		if pos == FCCorner.TopLeft:
			stroke = self.topLeft
		elif pos == FCCorner.TopRight:
			stroke = self.topRight
		elif pos == FCCorner.BottomLeft:
			stroke = self.bottomLeft
		elif pos == FCCorner.BottomRight:
			stroke = self.bottomRight
		else:
			stroke = FCStroke.StrokeNone
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

class FCBrick:
	TYPE_INVALIDATE = 0
	TYPE_STROKE = 1
	TYPE_REFERENCE = 2
	def __init__(self, position = FCCorner.CornerNone):
		self.setAsInvalidate()
		self._position = position
		self._usedByCorner = FCCorner.CornerNone

	def __str__(self):
		if self.isStroke():
			return "(1, %s)"%self.stroke
		elif self.isReference():
			return "(2, %s)"%self.wrapperBrick.getStroke()
		elif self.isInvalidate():
			return "%s"%FCStroke.StrokeNone
		else:
			return "%s"%FCStroke.StrokeNone

	@property
	def position(self):
		if self.isStroke():
			return self._position
		elif self.isReference():
			return self.wrapperBrick.position
		elif self.isInvalidate():
			return self._position
		else:
			return self._position

	def setAsInvalidate(self):
		self._type = FCBrick.TYPE_INVALIDATE

	def setAsStroke(self, stroke):
		self._type = FCBrick.TYPE_STROKE
		self.stroke = stroke

	def setAsReference(self, wrapperBrick):
		self._type = FCBrick.TYPE_REFERENCE
		self.wrapperBrick = wrapperBrick

	def isInvalidate(self):
		return self._type == FCBrick.TYPE_INVALIDATE

	def isStroke(self):
		return self._type == FCBrick.TYPE_STROKE

	def isReference(self):
		return self._type == FCBrick.TYPE_REFERENCE

	def setUsedByPosition(self):
		self.setUsedByCorner(self._position)

	def setUsedByCorner(self, corner):
		if self.isReference():
			self.wrapperBrick.setUsedByCorner(corner)
			return
		self._usedByCorner = corner

	def isUsed(self):
		if self.isReference():
			return self.wrapperBrick.isUsed()
		return self.getUsedCorner() != FCCorner.CornerNone

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

	def getStrokeOrCorner(self):
		if self.isStroke():
			return self.stroke
		elif self.isReference():
			return self.position
		elif self.isInvalidate():
			return FCStroke.StrokeNone
		else:
			return FCStroke.StrokeNone

