from . import quadratic
from .stroke import StrokeInfo
from .stroke import StrokeInfoMap

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
		return "%s"%([self.left, self.top, self.right, self.bottom])

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


class Drawing:
	def __init__(self, pane):
		self.infoPane=pane
		self.statePane=pane

	def getDrawingList(self):
		return []

	def getInfoPane(self):
		return self.infoPane

	def getStatePane(self):
		return self.statePane

	def setInfoPane(self, pane):
		self.infoPane=pane

	def setStatePane(self, pane):
		self.statePane=pane

	def transformBy(self, sgTargetPane, newSgTargetPane):
		sTargetPane=self.getStatePane()
		newSTargetPane=sgTargetPane.transformRelativePaneByTargetPane(sTargetPane, newSgTargetPane)
		self.setStatePane(newSTargetPane)

class Stroke(Drawing):
	def __init__(self, strokeInfo):
		pane=strokeInfo.getBBoxPane()
		super().__init__(pane)
		self.strokeInfo=strokeInfo

	def clone(self):
		stroke=Stroke(self.strokeInfo)
		stroke.setStatePane(self.getStatePane())
		return stroke

	@staticmethod
	def generateStroke(name, startPoint, parameterList, bBox):
		clsStrokeInfo = StrokeInfoMap.get(name, None)
		assert clsStrokeInfo!=None

		parameterList = clsStrokeInfo.parseExpression(parameterList)
		strokeInfo = clsStrokeInfo(name, startPoint, parameterList, Pane(bBox))
		return Stroke(strokeInfo)

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

	def getStrokeInfo(self):
		return self.strokeInfo

	def getPoints(self):
		pane=self.getStatePane()
		startPoint=self.strokeInfo.getStartPoint()
		points=self.strokeInfo.computePoints(startPoint)
		bBoxPane=self.getInfoPane()
		newPoints = [(isCurve, bBoxPane.transformRelativePointByTargetPane(point, pane)) for (isCurve, point) in points]
		return newPoints

class StrokeGroupInfo:
	def __init__(self, strokeList, bBoxPane):
		self.strokeList=strokeList
		self.bBoxPane=bBoxPane

	def getStrokeList(self):
		return self.strokeList

	def getBBoxPane(self):
		return self.bBoxPane

class StrokeGroup(Drawing):
	def __init__(self, strokeGroupInfo):
		pane=strokeGroupInfo.getBBoxPane()
		super().__init__(pane)
		self.strokeGroupInfo=strokeGroupInfo

	def clone(self):
		strokeList=[s.clone() for s in self.getStrokeList()]
		strokeGroupInfo=StrokeGroupInfo(strokeList, self.getInfoPane())
		strokeGroup=StrokeGroup(strokeGroupInfo)
		strokeGroup.setStatePane(self.getStatePane())
		return strokeGroup

	def getDrawingList(self):
		return self.getStrokeList()

	def getStrokeList(self):
		return self.strokeGroupInfo.getStrokeList()

	def getCount(self):
		return len(self.getStrokeList())

	@staticmethod
	def generateStrokeGroup(sg, pane):
		strokeGroup=sg.clone()

		newSgTargetPane=pane
		sgTargetPane=strokeGroup.getStatePane()
		sgInfoPane=strokeGroup.getInfoPane()
		for drawing in strokeGroup.getDrawingList():
			sTargetPane=drawing.getStatePane()
			sInfoPane=drawing.getInfoPane()
			drawing.transformBy(sgInfoPane, newSgTargetPane)

		strokeGroup.setStatePane(newSgTargetPane)
		strokeGroup.setInfoPane(newSgTargetPane)

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
			strokeGroup=StrokeGroup.generateStrokeGroup(strokeGroup, pane)
			resultStrokeList.extend(strokeGroup.getStrokeList())
			paneList.append(strokeGroup.getInfoPane())

		pane=computeBBox(paneList)
		strokeGroupInfo=StrokeGroupInfo(resultStrokeList, pane)

		return strokeGroupInfo

