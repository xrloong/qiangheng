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
			containerPane = None):
		self.operator = operator
		self.weights = weights

		self.containerPane = containerPane

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
		def compute(fromValue: int, toValue: int, frac: float) -> int:
			return round(fromValue*(1-frac) + toValue*frac)
		containerPane = spec.containerPane if spec.containerPane else LayoutFactory.DefaultBox

		operator = spec.operator
		# Silkworm = '蚕'
		# Goose = '鴻'
		if operator == JointOperator.Goose:
			return genHorizontalPanes(spec.weights, containerPane)
		if operator == JointOperator.Silkworm:
			return genVerticalPanes(spec.weights, containerPane)

		(centerX, centerY) = containerPane.center
		(left, top, right, bottom) = containerPane.boundary
		if operator == JointOperator.Qi:
			subPanes = [Pane(centerX, top, right, centerY)]
		elif operator == JointOperator.Liao:
			subPanes = [Pane(centerX, centerY, right, bottom)]
		elif operator == JointOperator.Zai:
			subPanes = [Pane(left, centerY, centerX, bottom)]
		elif operator == JointOperator.Dou:
			subPanes = [Pane(left, top, centerX, centerY)]
		elif operator == JointOperator.Loop:
			subPanes = [
						Pane(compute(left, right, 0.33), compute(top, bottom, 0.33),
							compute(left, right, 0.66), compute(top, bottom, 0.66)),
						]
		elif operator == JointOperator.Mu:
			subPanes = [
						Pane(left, centerY, centerX, bottom),
						Pane(centerX, centerY, right, bottom),
						]
		elif operator == JointOperator.Zuo:
			subPanes = [
						Pane(left, top, centerX, centerY),
						Pane(centerX, top, right, centerY),
						]
		elif operator == JointOperator.You:
			tmpBottom = compute(top, bottom, 0.8)
			subPanes = [
						Pane(compute(left, right, 0.1), top, compute(left, right, 0.4), tmpBottom),
						Pane(compute(left, right, 0.6), top, compute(left, right, 0.9), tmpBottom),
						]
		elif operator == JointOperator.Liang:
			tmpTop = compute(top, bottom, 0.2)
			subPanes = [
						Pane(compute(left, right, 0.1), tmpTop, compute(left, right, 0.4), bottom),
						Pane(compute(left, right, 0.6), tmpTop, compute(left, right, 0.9), bottom),
						]
		elif operator == JointOperator.Jia:
			tmpTop = compute(top, bottom, 0.2)
			tmpBottom = compute(top, bottom, 0.8)
			subPanes = [
						Pane(left, tmpTop, compute(left, right, 0.4), tmpBottom),
						Pane(compute(left, right, 0.6), tmpTop, right, tmpBottom),
						]
		else:
			subPanes = []

		return [containerPane] + subPanes

