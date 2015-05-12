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


class StrokeState:
	def __init__(self, targetPane=Pane()):
		self.targetPane=targetPane

	def clone(self):
		return StrokeState(self.targetPane.clone())

	def getTargetPane(self):
		return self.targetPane

class Stroke:
	def __init__(self, strokeInfo, state=StrokeState()):
		self.strokeInfo=strokeInfo
		self.state=state

	def clone(self):
		return Stroke(self.strokeInfo, self.state.clone())

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

	def getPointsOnPane(self, pane):
		startPoint=self.strokeInfo.getStartPoint()
		points=self.strokeInfo.computePoints(startPoint)
		newPoints = [(isCurve, pane.transformPoint(point)) for (isCurve, point) in points]
		return newPoints

	def getPoints(self):
		strokeState=self.getState()
		pane=strokeState.getTargetPane()
		return self.getPointsOnPane(pane)

	def getBBox(self):
		return self.strokeInfo.getBBox()

class StrokeGroupInfo:
	def __init__(self, strokeList, bBox):
		self.strokeList=strokeList
		self.bBox=bBox

	def getStrokeList(self):
		return self.strokeList

	def getBBox(self):
		return self.bBox

	def setBBox(self, bBox):
		self.bBox=bBox

class StrokeGroupState:
	def __init__(self, targetPane=Pane()):
		self.targetPane=targetPane

	def clone(self):
		return StrokeState(self.targetPane.clone())

	def getTargetPane(self):
		return self.targetPane

class StrokeGroup:
	def __init__(self, strokeGroupInfo, state=StrokeGroupState()):
		self.strokeGroupInfo=strokeGroupInfo
		self.state=state

	def clone(self):
		strokeList=[s.clone() for s in self.getStrokeList()]
		strokeGroupInfo=StrokeGroupInfo(strokeList, self.strokeGroupInfo.getBBox())
		return StrokeGroup(strokeGroupInfo, self.state.clone())

	def getBBox(self):
		return self.bBox

	def getStrokeList(self):
		return self.strokeGroupInfo.getStrokeList()

	def getCount(self):
		return len(self.getStrokeList())

	def isValid(self):
		return all([stroke.isValid() for stroke in self.getStrokeList()])

	# 多型
	def transform(self, pane):
		for stroke in self.getStrokeList():
			stroke.transform(pane)

