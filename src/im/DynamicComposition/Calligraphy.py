import re
import sys
import copy

class Point:
	def __init__(self, x, y):
		self.x=x
		self.y=y

	def __deepcopy__(self, memo):
		copy.deepcopy(None, memo)
		return Point(self.x, self.y)

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def scale(self, xScale, yScale):
		self.x=int(self.x*xScale)
		self.y=int(self.y*yScale)

	def translate(self, xOffset, yOffset):
		self.x=int(self.x+xOffset)
		self.y=int(self.y+yOffset)

	def transform(self, pane):
		width=pane.getWidth()
		height=pane.getHeight()
		xScale=width*1./Pane.WIDTH
		yScale=height*1./Pane.HEIGHT
		left=pane.getLeft()
		top=pane.getTop()

		self.scale(xScale, yScale)
		self.translate(left, top)

class Pane:
	WIDTH=0x100
	HEIGHT=0x100
	X_MAX=0xFF
	Y_MAX=0xFF

	DEFAULT_REGION=[0, 0, X_MAX, Y_MAX]

	def __init__(self, region=DEFAULT_REGION):
		[left, top, right, bottom]=region
		self.left=left
		self.top=top
		self.right=right
		self.bottom=bottom

		self.name="預設範圍"

	def __deepcopy__(self, memo):
		copy.deepcopy(None, memo)
		return self

	@property
	def width(self):
		return self.right-self.left+1

	@property
	def height(self):
		return self.bottom-self.top+1

	def setName(self, name):
		self.name=name

	def getName(self):
		return self.name

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

Pane.DEFAULT_PANE=Pane()

class Writing:
	def __init__(self, contourPane):
		self.boundaryPane=Pane.DEFAULT_PANE
		self.contourPane=contourPane

	def getBoundaryPane(self):
		return self.boundaryPane

	def getContourPane(self):
		return self.contourPane

	# 多型
	def transform(self, pane):
		pass

class Stroke(Writing):
	STROKE_NAMES=[
#		"XXXX",

		"點", "長頓點",

		"橫", "橫鉤", "橫折", "橫折橫",
		"橫折鉤", "橫撇", "橫曲鉤",
		"橫撇橫折鉤", "橫斜鉤",
		"橫折橫折",

		"豎", "豎折", "豎挑", "豎橫折",
		"豎橫折鉤", "豎曲鉤", "豎鉤",
		"臥鉤", "斜鉤", "彎鉤",

		"撇", "撇頓點", "撇橫", "撇挑",
		"撇折", "豎撇", "挑", "挑折",
		"捺",

		"挑捺",	# 例子：乀
		"橫捺",	# 例子：乁
		"圓",	# 例子：㔔
	]

	DEFAULT_INSTANCE_NAME='瑲珩預設筆劃名'

	def __init__(self, contourPane, strokeName, actionList, pointList):
		super().__init__(contourPane)

		assert (strokeName in Stroke.STROKE_NAMES), "不認得的筆畫名稱: %s"%strokeName

		self.setInstanceName(Stroke.DEFAULT_INSTANCE_NAME)

		self.typeName=strokeName

		self.actionList=actionList
		self.pointList=pointList

	def __deepcopy__(self, memo):
		pointList=copy.deepcopy(self.pointList, memo)
		return Stroke(self.contourPane, self.typeName, self.actionList, pointList)

	def getInstanceName(self):
		return self.name

	def setInstanceName(self, name):
		self.name=name

	def getTypeName(self):
		return self.typeName

	def getCode(self):
		codeList=["%4s%02X%02X"%(action, point.getX(), point.getY()) for [action, point] in zip(self.actionList, self.pointList)]
		return ','.join(codeList)

	# 多型
	def transform(self, pane):
		for point in self.pointList:
			point.transform(pane)

class StrokeGroup(Writing):
	def __init__(self, contourPane, strokeList):
		super().__init__(contourPane)

		self.strokeList=strokeList

	def __deepcopy__(self, memo):
		strokeList=copy.deepcopy(self.strokeList, memo)
		return StrokeGroup(self.contourPane, strokeList)

	def clone(self):
		return copy.deepcopy(self)

	def getStrokeList(self):
		return self.strokeList

	# 多型
	def transform(self, pane):
		for stroke in self.strokeList:
			stroke.transform(pane)

