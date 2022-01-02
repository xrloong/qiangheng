from enum import Enum

from xie.graphics.shape import Pane

from xrsolver import Problem
from xrsolver import CompoundConstraint
from xrsolver import Objective
from xrsolver import Optimization
from xrsolver.solver.cassowary import Solver

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

class Box(CompoundConstraint):
	def __init__(self, name):
		super().__init__(name)

		self.left = self.generateVariable("left")
		self.top = self.generateVariable("top")
		self.right = self.generateVariable("right")
		self.bottom = self.generateVariable("bottom")

	@property
	def width(self):
		return self.right - self.left

	@property
	def height(self):
		return self.bottom - self.top

	@property
	def boundary(self):
		return [
				self.left.getValue(),
				self.top.getValue(),
				self.right.getValue(),
				self.bottom.getValue(),
				]

	def getVariables(self):
		return [
				self.left,
				self.top,
				self.right,
				self.bottom,
				]

	def getConstraints(self):
		return [
				self.width >= 0,
				self.height >= 0,
				]

	def getObjectives(self):
		return [ Objective(self.width + self.height) ]

class GuideBox(Box):
	def __init__(self, name, hNum = 0, vNum = 0, hWeights = None, vWeights = None):
		super().__init__(name)

		self.hLines = [self.generateVariable("hL%s"%i) for i in range(hNum)]
		self.vLines = [self.generateVariable("vL%s"%i) for i in range(vNum)]
		self.hUnit = self.generateVariable("hUnit")
		self.vUnit = self.generateVariable("vUnit")

		self.hGuidelines = [self.left] + self.hLines + [self.right]
		self.vGuidelines = [self.top] + self.vLines + [self.bottom]

		self.hWeights = [1 for i in range(hNum + 1)]
		self.vWeights = [1 for i in range(vNum + 1)]

		self.setupWeights(hWeights = hWeights, vWeights = vWeights)

	def getHGuideline(self, index):
		return self.hGuidelines[index]

	def getVGuideline(self, index):
		return self.vGuidelines[index]

	def setupWeights(self, hWeights = None, vWeights = None):
		if hWeights != None:
			self.hWeights = hWeights
		if vWeights != None:
			self.vWeights = vWeights

	def getVariables(self):
		return super().getVariables() + self.hLines + self.vLines + [self.hUnit, self.vUnit]

	def getConstraints(self):
		constraints = []

		constraints.append(self.hUnit >= 0)
		constraints.append(self.vUnit >= 0)

		lines = self.hGuidelines
		for s, e, w in zip(lines[:-1], lines[1:], self.hWeights):
			constraints.append((e - s) == w * self.hUnit)
		lines = self.vGuidelines
		for s, e, w in zip(lines[:-1], lines[1:], self.vWeights):
			constraints.append((e - s) == w * self.vUnit)

		return super().getConstraints() + constraints

	def getObjectives(self):
		return super().getObjectives()

class LayoutProblem(Problem):
	def __init__(self):
		super().__init__()

		self.guideBox = None
		self.boxes = []

	def bindContainer(self, containerPaine):
		self.appendConstraint(self.guideBox.left == containerPaine.left)
		self.appendConstraint(self.guideBox.top == containerPaine.top)
		self.appendConstraint(self.guideBox.right == containerPaine.right)
		self.appendConstraint(self.guideBox.bottom == containerPaine.bottom)

	def setup(self, spec: LayoutSpec):
		operator = spec.operator
		if operator == JointOperator.Goose:
			numBoxes = len(spec.weights)
			self.setupCommonBox(numBoxes, hNum = numBoxes - 1, hWeights = spec.weights)

			self.setupForGoose()
		elif operator == JointOperator.Silkworm:
			numBoxes = len(spec.weights)
			self.setupCommonBox(numBoxes, vNum = numBoxes - 1, vWeights = spec.weights)

			self.setupForSilkworm()
		elif operator == JointOperator.Loop:
			self.setupCommonBox(2, hNum = 2, vNum = 2)

			self.setupForLoop()
		elif operator == JointOperator.Qi:
			self.setupCommonBox(2, hNum = 1, vNum = 1)

			self.setupForQi()
		elif operator == JointOperator.Liao:
			self.setupCommonBox(2, hNum = 1, vNum = 1)

			self.setupForLiao()
		elif operator == JointOperator.Zai:
			self.setupCommonBox(2, hNum = 1, vNum = 1)

			self.setupForZai()
		elif operator == JointOperator.Dou:
			self.setupCommonBox(2, hNum = 1, vNum = 1)

			self.setupForDou()
		elif operator == JointOperator.Mu:
			self.setupCommonBox(3, hNum = 1, vNum = 1)

			self.setupForMu()
		elif operator == JointOperator.Zuo:
			self.setupCommonBox(3, hNum = 1, vNum = 1)

			self.setupForZuo()
		elif operator == JointOperator.You:
			self.setupCommonBox(3, hNum = 4, vNum = 1, hWeights = [1, 3, 2, 3, 1], vWeights = [4, 1])

			self.setupForYou()
		elif operator == JointOperator.Liang:
			self.setupCommonBox(3, hNum = 4, vNum = 1, hWeights = [1, 3, 2, 3, 1], vWeights = [1, 4])

			self.setupForLiang()
		elif operator == JointOperator.Jia:
			self.setupCommonBox(3, hNum = 2, vNum = 2, hWeights = [4, 2, 4], vWeights = [2, 6, 2])

			self.setupForJia()
		else:
			pass

	def setupCommonBox(self, numBoxes, hNum = 0, vNum = 0, hWeights = None, vWeights = None):
		guideBox = GuideBox("guideBox", hNum = hNum, vNum = vNum, hWeights = hWeights, vWeights = vWeights)
		boxes = [Box("box%s"%i) for i in range(numBoxes)]

		self.appendCompoundConstraint(guideBox)
		for box in boxes:
			self.appendCompoundConstraint(box)

		self.guideBox = guideBox
		self.boxes = boxes

	def setAsGuideBox(self, box):
		guideBox = self.guideBox

		self.appendConstraint(box.left == guideBox.left)
		self.appendConstraint(box.top == guideBox.top)
		self.appendConstraint(box.right == guideBox.right)
		self.appendConstraint(box.bottom == guideBox.bottom)

	def setupForGoose(self):
		guideBox = self.guideBox
		for index, box in enumerate(self.boxes):
			self.appendConstraint(box.left == guideBox.getHGuideline(index))
			self.appendConstraint(box.right == guideBox.getHGuideline(index + 1))

			self.appendConstraint(box.top == guideBox.top)
			self.appendConstraint(box.bottom == guideBox.bottom)

	def setupForSilkworm(self):
		guideBox = self.guideBox
		for index, box in enumerate(self.boxes):
			self.appendConstraint(box.left == guideBox.left)
			self.appendConstraint(box.right == guideBox.right)

			self.appendConstraint(box.top == guideBox.getVGuideline(index))
			self.appendConstraint(box.bottom == guideBox.getVGuideline(index + 1))

	def setupForLoop(self):
		guideBox = self.guideBox
		box0, box1 = self.boxes

		self.setAsGuideBox(box0)

		self.appendConstraint(box1.left == guideBox.getHGuideline(1))
		self.appendConstraint(box1.top == guideBox.getVGuideline(1))
		self.appendConstraint(box1.right == guideBox.getHGuideline(2))
		self.appendConstraint(box1.bottom == guideBox.getVGuideline(2))

	def setupForQi(self):
		guideBox = self.guideBox
		box0, box1 = self.boxes

		self.setAsGuideBox(box0)

		self.appendConstraint(box1.left == guideBox.getHGuideline(1))
		self.appendConstraint(box1.top == guideBox.top)
		self.appendConstraint(box1.right == guideBox.right)
		self.appendConstraint(box1.bottom == guideBox.getVGuideline(1))

	def setupForLiao(self):
		guideBox = self.guideBox
		box0, box1 = self.boxes

		self.setAsGuideBox(box0)

		self.appendConstraint(box1.left == guideBox.getHGuideline(1))
		self.appendConstraint(box1.top == guideBox.getVGuideline(1))
		self.appendConstraint(box1.right == guideBox.right)
		self.appendConstraint(box1.bottom == guideBox.bottom)

	def setupForZai(self):
		guideBox = self.guideBox
		box0, box1 = self.boxes

		self.setAsGuideBox(box0)

		self.appendConstraint(box1.left == guideBox.left)
		self.appendConstraint(box1.top == guideBox.getVGuideline(1))
		self.appendConstraint(box1.right == guideBox.getHGuideline(1))
		self.appendConstraint(box1.bottom == guideBox.bottom)

	def setupForDou(self):
		guideBox = self.guideBox
		box0, box1 = self.boxes

		self.setAsGuideBox(box0)

		self.appendConstraint(box1.left == guideBox.left)
		self.appendConstraint(box1.top == guideBox.top)
		self.appendConstraint(box1.right == guideBox.getHGuideline(1))
		self.appendConstraint(box1.bottom == guideBox.getVGuideline(1))

	def setupForMu(self):
		guideBox = self.guideBox
		box0, box1, box2 = self.boxes

		self.setAsGuideBox(box0)

		self.appendConstraint(box1.left == guideBox.left)
		self.appendConstraint(box1.top == guideBox.getVGuideline(1))
		self.appendConstraint(box1.right == guideBox.getHGuideline(1))
		self.appendConstraint(box1.bottom == guideBox.bottom)

		self.appendConstraint(box2.left == guideBox.getHGuideline(1))
		self.appendConstraint(box2.top == guideBox.getVGuideline(1))
		self.appendConstraint(box2.right == guideBox.getHGuideline(2))
		self.appendConstraint(box2.bottom == guideBox.bottom)

	def setupForZuo(self):
		guideBox = self.guideBox
		box0, box1, box2 = self.boxes

		self.setAsGuideBox(box0)

		self.appendConstraint(box1.left == guideBox.left)
		self.appendConstraint(box1.top == guideBox.top)
		self.appendConstraint(box1.right == guideBox.getHGuideline(1))
		self.appendConstraint(box1.bottom == guideBox.getVGuideline(1))

		self.appendConstraint(box2.left == guideBox.getHGuideline(1))
		self.appendConstraint(box2.top == guideBox.top)
		self.appendConstraint(box2.right == guideBox.right)
		self.appendConstraint(box2.bottom == guideBox.getVGuideline(1))

	def setupForYou(self):
		guideBox = self.guideBox
		box0, box1, box2 = self.boxes

		self.setAsGuideBox(box0)

		self.appendConstraint(box1.left == guideBox.getHGuideline(1))
		self.appendConstraint(box1.top == guideBox.top)
		self.appendConstraint(box1.right == guideBox.getHGuideline(2))
		self.appendConstraint(box1.bottom == guideBox.getVGuideline(1))

		self.appendConstraint(box2.left == guideBox.getHGuideline(3))
		self.appendConstraint(box2.top == guideBox.top)
		self.appendConstraint(box2.right == guideBox.getHGuideline(4))
		self.appendConstraint(box2.bottom == guideBox.getVGuideline(1))

	def setupForLiang(self):
		guideBox = self.guideBox
		box0, box1, box2 = self.boxes

		self.setAsGuideBox(box0)

		self.appendConstraint(box1.left == guideBox.getHGuideline(1))
		self.appendConstraint(box1.top == guideBox.getVGuideline(1))
		self.appendConstraint(box1.right == guideBox.getHGuideline(2))
		self.appendConstraint(box1.bottom == guideBox.bottom)

		self.appendConstraint(box2.left == guideBox.getHGuideline(3))
		self.appendConstraint(box2.top == guideBox.getVGuideline(1))
		self.appendConstraint(box2.right == guideBox.getHGuideline(4))
		self.appendConstraint(box2.bottom == guideBox.bottom)

	def setupForJia(self):
		guideBox = self.guideBox
		box0, box1, box2 = self.boxes

		self.setAsGuideBox(box0)

		self.appendConstraint(box1.left == guideBox.left)
		self.appendConstraint(box1.top == guideBox.getVGuideline(1))
		self.appendConstraint(box1.right == guideBox.getHGuideline(1))
		self.appendConstraint(box1.bottom == guideBox.getVGuideline(2))

		self.appendConstraint(box2.left == guideBox.getHGuideline(2))
		self.appendConstraint(box2.top == guideBox.getVGuideline(1))
		self.appendConstraint(box2.right == guideBox.right)
		self.appendConstraint(box2.bottom == guideBox.getVGuideline(2))

class LayoutProblemFactory:
	def __init__(self):
		super().__init__()

	def generateLayoutProblem(self, spec: LayoutSpec):
		layoutProblem = LayoutProblem()
		layoutProblem.setup(spec)
		return layoutProblem

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
		self.layoutProblemFactory = LayoutProblemFactory()

	def generateLayouts(self, spec: LayoutSpec) -> [Pane]:
		boundaries = self._generateLayouts(spec, LayoutFactory.DefaultBox)
		return [Pane(round(left, 6), round(top, 6), round(right, 6), round(bottom, 6))
				for (left, top, right, bottom) in boundaries]

	def _generateLayouts(self, spec: LayoutSpec, containerPane) -> [(int)]:
		problem = self.layoutProblemFactory.generateLayoutProblem(spec)
		problem.bindContainer(containerPane)

		solver = Solver()
		solver.solveProblem(problem)
		return [box.boundary for box in problem.boxes]

