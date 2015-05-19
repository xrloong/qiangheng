from . import quadratic
from .stroke import StrokeInfo
from .stroke import StrokeInfoMap

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

	def __str__(self):
		return "%s"%((self.left, self.top, self.right, self.bottom), )

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

	def containsPoint(self, point):
		x, y = point
		return (self.left<=x<=self.right) and (self.top<=y<=self.bottom)

	def containsPane(self, pane):
		return self.containsPoint(pane.getLeftTop()) and self.containsPoint(pane.getRightBottom())

	def limitedToPane(self, pane):
		left=max(self.left, pane.left)
		top=max(self.top, pane.top)
		right=min(self.right, pane.right)
		bottom=min(self.bottom, pane.bottom)

		self.left=left
		self.top=top
		self.right=right
		self.bottom=bottom

		self.setup()

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

	def getLeftTop(self):
		return (self.left, self.top)

	def getRightBottom(self):
		return (self.right, self.bottom)

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

	def transformRelativePointByTargetPane(self, point, targetPane):
		(x, y)=point

		newX=int((x-self.getLeft())*targetPane.getWidth()/self.getWidth())+targetPane.getLeft()
		newY=int((y-self.getTop())*targetPane.getHeight()/self.getHeight())+targetPane.getTop()

		assert newX==max(targetPane.left, min(targetPane.right, newX))
		assert newY==max(targetPane.top, min(targetPane.bottom, newY))

		return (newX, newY)

	def transformRelativePaneByTargetPane(self, relativePane, targetPane):
		(left, top)=self.transformRelativePointByTargetPane(relativePane.getLeftTop(), targetPane)
		(right, bottom)=self.transformRelativePointByTargetPane(relativePane.getRightBottom(), targetPane)

		return Pane((left, top, right, bottom))


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
	def __init__(self, strokeInfo, state=None):
		self.strokeInfo=strokeInfo
		if state:
			self.state=state
		else:
			self.state=StrokeState(strokeInfo.getBBoxPane())

	def clone(self):
		return Stroke(self.strokeInfo, self.state.clone())

	@staticmethod
	def generateStrokeInfo(name, startPoint, parameterList, bBox):
		clsStrokeInfo = StrokeInfoMap.get(name, None)
		assert clsStrokeInfo!=None

		parameterList = clsStrokeInfo.parseExpression(parameterList)
		strokeInfo = clsStrokeInfo(name, startPoint, parameterList, Pane(bBox))
		return strokeInfo

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

	def transformBy(self, sgTargetPane, newSgTargetPane):
		sTargetPane=self.state.targetPane
		newSTargetPane=sgTargetPane.transformRelativePaneByTargetPane(sTargetPane, newSgTargetPane)
		self.state.targetPane=newSTargetPane

	def getPointsOnPane(self, pane):
		startPoint=self.strokeInfo.getStartPoint()
		points=self.strokeInfo.computePoints(startPoint)
		bBoxPane=self.getInfoPane()
		newPoints = [(isCurve, bBoxPane.transformRelativePointByTargetPane(point, pane)) for (isCurve, point) in points]
		return newPoints

	def getPoints(self):
		strokeState=self.getState()
		pane=strokeState.getTargetPane()
		return self.getPointsOnPane(pane)

	def getInfoPane(self):
		return self.strokeInfo.getBBoxPane()

	def getStatePane(self):
		return self.state.getTargetPane()

class StrokeGroupInfo:
	def __init__(self, strokeList, bBox):
		self.strokeList=strokeList
		self.bBoxPane=Pane(bBox)

	def getStrokeList(self):
		return self.strokeList

	def getBBoxPane(self):
		return self.bBoxPane

	def setBBoxPane(self, bBoxPane):
		self.bBoxPane=bBoxPane

class StrokeGroupState:
	def __init__(self, targetPane=Pane()):
		self.targetPane=targetPane

	def clone(self):
		return StrokeState(self.targetPane.clone())

	def getTargetPane(self):
		return self.targetPane

class StrokeGroup:
	def __init__(self, strokeGroupInfo, state=None):
		self.strokeGroupInfo=strokeGroupInfo
		if state:
			self.state=state
		else:
			self.state=StrokeGroupState(strokeGroupInfo.getBBoxPane())

	def clone(self):
		strokeList=[s.clone() for s in self.getStrokeList()]
		strokeGroupInfo=StrokeGroupInfo(strokeList, self.getInfoPane().getAsList())
		return StrokeGroup(strokeGroupInfo, self.state.clone())

	def getInfoPane(self):
		return self.strokeGroupInfo.getBBoxPane()

	def getStatePane(self):
		return self.state.getTargetPane()

	def setInfoPane(self, pane):
		self.strokeGroupInfo.setBBoxPane(pane)

	def setStatePane(self, pane):
		self.state.targetPane=pane

	def getStrokeList(self):
		return self.strokeGroupInfo.getStrokeList()

	def getCount(self):
		return len(self.getStrokeList())

	def isValid(self):
		return all([stroke.isValid() for stroke in self.getStrokeList()])

	# 多型
	def transform(self, newSgTargetPane):
		sgTargetPane=self.getStatePane()
		sgInfoPane=self.getInfoPane()
		for stroke in self.getStrokeList():
			sTargetPane=stroke.getStatePane()
			sInfoPane=stroke.getInfoPane()
			stroke.transformBy(sgInfoPane, newSgTargetPane)

		self.setStatePane(newSgTargetPane)
		self.setInfoPane(newSgTargetPane)

	def generateStrokeGroup(self, pane):
		strokeGroup=self.clone()
		strokeGroup.transform(pane)
		return strokeGroup

	@staticmethod
	def generateStrokeGroupInfo(strokeGroupPanePair):
		def computeBBox(paneList):
			left=min(map(lambda pane: pane.getLeft(), paneList))
			top=min(map(lambda pane: pane.getTop(), paneList))
			right=max(map(lambda pane: pane.getRight(), paneList))
			bottom=max(map(lambda pane: pane.getBottom(), paneList))
			return Pane((left, top, right, bottom))

		resultStrokeList=[]
		paneList=[]
		for strokeGroup, pane in strokeGroupPanePair:
			strokeGroup=strokeGroup.generateStrokeGroup(pane)
			resultStrokeList.extend(strokeGroup.getStrokeList())
			paneList.append(strokeGroup.getInfoPane())

		pane=computeBBox(paneList)
		strokeGroupInfo=StrokeGroupInfo(resultStrokeList, pane.getAsList())

		return strokeGroupInfo

