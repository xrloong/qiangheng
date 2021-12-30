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
	def __init__(self, operator, weights = [int]):
		self.operator = operator
		self.weights = weights

def _splitLengthToList(length, weightList):
	totalWeight = sum(weightList)
	unitLength = length / totalWeight

	pointList = []
	newComponentList = []
	base = 0
	for weight in weightList:
		pointList.append(base)
		base = base + unitLength * weight
	pointList.append(base)
	return pointList

def genVerticalPanes(weights, containerPane):
	pane = containerPane
	points = _splitLengthToList(pane.height, weights)
	paneList = []
	offset = pane.top
	for [pointStart, pointEnd] in zip(points[:-1], points[1:]):
		newPane = (pane.left, pointStart + offset, pane.right, pointEnd + offset)
		paneList.append(newPane)
	return paneList

def genHorizontalPanes(weights, containerPane):
	pane = containerPane
	points = _splitLengthToList(pane.width, weights)
	paneList = []
	offset = pane.left
	for [pointStart, pointEnd] in zip(points[:-1], points[1:]):
		newPane = (pointStart + offset, pane.top, pointEnd + offset, pane.bottom)
		paneList.append(newPane)
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
		boundaries = self._generateLayouts(spec, LayoutFactory.DefaultBox)
		return [Pane(round(left, 6), round(top, 6), round(right, 6), round(bottom, 6))
				for (left, top, right, bottom) in boundaries]

	def _generateLayouts(self, spec: LayoutSpec, containerPane) -> [(int)]:
		def compute(fromValue: int, toValue: int, frac: float) -> int:
			return fromValue*(1-frac) + toValue*frac

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
			subPanes = [(centerX, top, right, centerY)]
		elif operator == JointOperator.Liao:
			subPanes = [(centerX, centerY, right, bottom)]
		elif operator == JointOperator.Zai:
			subPanes = [(left, centerY, centerX, bottom)]
		elif operator == JointOperator.Dou:
			subPanes = [(left, top, centerX, centerY)]
		elif operator == JointOperator.Loop:
			subPanes = [
						(compute(left, right, 1/3), compute(top, bottom, 1/3),
							compute(left, right, 2/3), compute(top, bottom, 2/3)),
						]
		elif operator == JointOperator.Mu:
			subPanes = [
						(left, centerY, centerX, bottom),
						(centerX, centerY, right, bottom),
						]
		elif operator == JointOperator.Zuo:
			subPanes = [
						(left, top, centerX, centerY),
						(centerX, top, right, centerY),
						]
		elif operator == JointOperator.You:
			tmpBottom = compute(top, bottom, 0.8)
			subPanes = [
						(compute(left, right, 0.1), top, compute(left, right, 0.4), tmpBottom),
						(compute(left, right, 0.6), top, compute(left, right, 0.9), tmpBottom),
						]
		elif operator == JointOperator.Liang:
			tmpTop = compute(top, bottom, 0.2)
			subPanes = [
						(compute(left, right, 0.1), tmpTop, compute(left, right, 0.4), bottom),
						(compute(left, right, 0.6), tmpTop, compute(left, right, 0.9), bottom),
						]
		elif operator == JointOperator.Jia:
			tmpTop = compute(top, bottom, 0.2)
			tmpBottom = compute(top, bottom, 0.8)
			subPanes = [
						(left, tmpTop, compute(left, right, 0.4), tmpBottom),
						(compute(left, right, 0.6), tmpTop, right, tmpBottom),
						]
		else:
			subPanes = []

		return [containerPane.boundary] + subPanes

