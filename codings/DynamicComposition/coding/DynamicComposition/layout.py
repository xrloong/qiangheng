from enum import Enum

from xie.graphics.shape import Pane

class JointOperator(Enum):
	Silkworm = '蚕'
	Goose = '鴻'
	Loop = '回'

	Qi = '起'
	Liao = '廖'
	Zai = '載'
	Dou = '斗'

	Mu = '畞'
	Zuo = '㘴'
	You = '幽'
	Liang = '㒳'
	Jia = '夾'

class LayoutSpec:
	def __init__(self, operator, weights = [int],
			containerPane = None, subPanes = []):
		self.operator = operator
		self.weights = weights

		self.containerPane = containerPane
		self.subPanes = subPanes

def _splitLengthToList(length, weightList):
	totalWeight=sum(weightList)
	unitLength=length*1./totalWeight

	pointList=[]
	newComponentList=[]
	base=0
	for weight in weightList:
		pointList.append(int(base))
		base=base+unitLength*weight
	pointList.append(int(base))
	return pointList

def genVerticalPanes(weights, containerPane):
	pane = containerPane
	points=_splitLengthToList(pane.height, weights)
	paneList=[]
	offset=pane.top
	for [pointStart, pointEnd] in zip(points[:-1], points[1:]):
		height=pointEnd-pointStart
		targetHeight=int(height*0.90)
		offset=int(height-targetHeight)//2
		tmpPane=Pane(pane.left, pointStart+offset, pane.right, pointEnd-offset)
		tmpPane._offsetTopAndBottom(offset)
		paneList.append(tmpPane)
	return paneList

def genHorizontalPanes(weights, containerPane):
	pane = containerPane
	points=_splitLengthToList(pane.width, weights)
	paneList=[]
	offset=pane.left
	for [pointStart, pointEnd] in zip(points[:-1], points[1:]):
		width=pointEnd-pointStart
		targetWidth=int(width*0.90)
		offset=int(width-targetWidth)//2
		tmpPane=Pane(pointStart+offset, pane.top, pointEnd-offset, pane.bottom)
		tmpPane._offsetLeftAndRight(offset)
		paneList.append(tmpPane)
	return paneList

class LayoutFactory:
	# 字面框（Bounding Box）
	BBOX_X_MIN = 0x08
	BBOX_Y_MIN = 0x08
	BBOX_X_MAX = 0xF7
	BBOX_Y_MAX = 0xF7

	DefaultBox = Pane(
		BBOX_X_MIN,
		BBOX_Y_MIN,
		BBOX_X_MAX,
		BBOX_Y_MAX,
	)

	def __init__(self):
		pass

	def generateLayouts(self, spec: LayoutSpec) -> [Pane]:
		containerPane = spec.containerPane if spec.containerPane else LayoutFactory.DefaultBox

		operator = spec.operator
		if operator == JointOperator.Goose:
			return genHorizontalPanes(spec.weights, containerPane)
		if operator == JointOperator.Silkworm:
			return genVerticalPanes(spec.weights, containerPane)

		if spec.subPanes:
			subPanes = spec.subPanes
		else:
			subPanes = []

		return [containerPane] + subPanes

