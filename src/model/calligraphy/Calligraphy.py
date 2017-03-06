from . import quadratic
from .stroke import StrokeInfo
from .stroke import StrokeInfoMap
from xie.graphics.shape import Pane


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

