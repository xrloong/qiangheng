from . import quadratic
from .stroke import StrokeInfo

class StrokeDrawing:
	def __init__(self, points):
		self.points = points

	def computeLeft(self):
		return StrokeInfo.computeExtreme(self.points, min, quadratic.solveMin, lambda p: p[0])

	def computeRight(self):
		return StrokeInfo.computeExtreme(self.points, max, quadratic.solveMax, lambda p: p[0])

	def computeTop(self):
		return StrokeInfo.computeExtreme(self.points, min, quadratic.solveMin, lambda p: p[1])

	def computeBottom(self):
		return StrokeInfo.computeExtreme(self.points, max, quadratic.solveMax, lambda p: p[1])

	def computeScope(self):
		return (
			self.computeLeft(), self.computeTop(),
			self.computeRight(), self.computeBottom(),
			)

class Pane:
	EMBOX_X_MIN=0x00
	EMBOX_Y_MIN=0x00
	EMBOX_X_MAX=0xFF
	EMBOX_Y_MAX=0xFF
	EMBOX_WIDTH=EMBOX_X_MAX-EMBOX_X_MIN+1
	EMBOX_HEIGHT=EMBOX_Y_MAX-EMBOX_Y_MIN+1

	BBOX_X_MIN=0x08
	BBOX_Y_MIN=0x08
	BBOX_X_MAX=0xF7
	BBOX_Y_MAX=0xF7


	EMBOX_REGION=[EMBOX_X_MIN, EMBOX_Y_MIN, EMBOX_X_MAX, EMBOX_Y_MAX]

	def __init__(self, region=EMBOX_REGION):
		[left, top, right, bottom]=region
		self.left=left
		self.top=top
		self.right=right
		self.bottom=bottom

		self.setup()

	def clone(self):
		return Pane(self.getAsList())

	def setup(self):
		self.hScale=self.width*1./Pane.EMBOX_WIDTH
		self.vScale=self.height*1./Pane.EMBOX_HEIGHT

	def offsetLeftAndRight(self, offset):
		self.left += offset
		self.right += offset

	def offsetTopAndBottom(self, offset):
		self.top += offset
		self.bottom += offset

	@property
	def width(self):
		return self.right-self.left+1

	@property
	def height(self):
		return self.bottom-self.top+1

	def getAsList(self):
		return [self.left, self.top, self.right, self.bottom]

	def getLeft(self):
		return self.left

	def getTop(self):
		return self.top

	def getRight(self):
		return self.right

	def getBottom(self):
		return self.bottom

	def getWidth(self):
		return self.width

	def getHeight(self):
		return self.height

	def getHScale(self):
		return self.hScale

	def getVScale(self):
		return self.vScale

	def transformPoint(self, point):
		[x, y]=point
		left=self.getLeft()
		top=self.getTop()

		hScale=self.getHScale()
		vScale=self.getVScale()

		newX=int(x*hScale)+left
		newY=int(y*vScale)+top

		return (newX, newY)

	def transformPane(self, pane):
		(left, top)=self.transformPoint((pane.left, pane.top))
		(right, bottom)=self.transformPoint((pane.right, pane.bottom))

		pane.left=left
		pane.top=top
		pane.right=right
		pane.bottom=bottom

		pane.setup()

# 字身框（Em Box）
Pane.EMBOX=Pane()

# 字面框（Bounding Box）
Pane.BBOX=Pane([
	Pane.BBOX_X_MIN,
	Pane.BBOX_Y_MIN,
	Pane.BBOX_X_MAX,
	Pane.BBOX_Y_MAX,
	])


class Writing:
	def __init__(self, contourPane):
		self.boundaryPane=Pane.EMBOX
		self.contourPane=contourPane

	def getBoundaryPane(self):
		return self.boundaryPane

	def getContourPane(self):
		return self.contourPane

	# 多型
	def transform(self, pane):
		pass

class StrokeState:
	def __init__(self, targetPane=Pane()):
		self.targetPane=targetPane

	def clone(self):
		return StrokeState(self.targetPane.clone())

	def getTargetPane(self):
		return self.targetPane

class Stroke(Writing):
	def __init__(self, startPoint, strokeInfo, state=StrokeState()):
		super().__init__(Pane())

		self.startPoint=startPoint
		self.strokeInfo=strokeInfo
		self.state=state

	def clone(self):
		return Stroke(self.startPoint, self.strokeInfo, self.state.clone())

	def getExpression(self):
		def encodeStroke(stroke):
			points=stroke.getPoints()
			point = points[0]
			isCurve = point[0]
			assert isCurve is False
			pointExpressionList = ["0000{0[0]:02X}{0[1]:02X}".format(point[1]), ]

			for point in points[1:]:
				isCurve = point[0]
				if isCurve:
					pointExpressionList.append("0002{0[0]:02X}{0[1]:02X}".format(point[1]))
				else:
					pointExpressionList.append("0001{0[0]:02X}{0[1]:02X}".format(point[1]))
			return ",".join(pointExpressionList)
		return encodeStroke(self)


	def getName(self):
		return self.getStrokeInfo().getName()

	def getState(self):
		return self.state

	def getStrokeInfo(self):
		return self.strokeInfo

	def isValid(self):
		return self.strokeInfo.isValid()

	# 多型
	def transform(self, pane):
		pane.transformPane(self.state.getTargetPane())

	def getPoints(self):
		strokeState=self.getState()
		pane=strokeState.getTargetPane()

		startPoint=self.startPoint
		points=self.strokeInfo.computePoints(startPoint)
		newPoints = [(isCurve, pane.transformPoint(point)) for (isCurve, point) in points]
		return newPoints

	def computeScope(self):
		return StrokeDrawing(self.getPoints()).computeScope()

class StrokeGroup(Writing):
	def __init__(self, contourPane, strokeList):
		super().__init__(contourPane)

		self.strokeList=strokeList

	def clone(self):
		strokeList=[s.clone() for s in self.strokeList]
		return StrokeGroup(self.contourPane, strokeList)

	def getStrokeList(self):
		return self.strokeList

	def getCount(self):
		return len(self.strokeList)

	def isValid(self):
		return all([stroke.isValid() for stroke in self.strokeList])

	# 多型
	def transform(self, pane):
		for stroke in self.strokeList:
			stroke.transform(pane)

	def computeScope(self):
		scopes=[s.computeScope() for s in self.strokeList]
		left=min(list(zip(*scopes))[0])
		top=min(list(zip(*scopes))[1])
		right=min(list(zip(*scopes))[2])
		bottom=min(list(zip(*scopes))[3])
		return (left, top, right, bottom)

