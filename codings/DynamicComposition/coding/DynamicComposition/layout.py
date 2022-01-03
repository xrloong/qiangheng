import copy

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
	def __init__(self, name, hNum = 0, vNum = 0):
		super().__init__(name)

		self.hLines = [self.generateVariable("hL%s"%i) for i in range(hNum)]
		self.vLines = [self.generateVariable("vL%s"%i) for i in range(vNum)]
		self.hUnit = self.generateVariable("hUnit")
		self.vUnit = self.generateVariable("vUnit")

		self.hGuidelines = [self.left] + self.hLines + [self.right]
		self.vGuidelines = [self.top] + self.vLines + [self.bottom]

		self.hWeights = [1 for i in range(hNum + 1)]
		self.vWeights = [1 for i in range(vNum + 1)]

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

	def initCommonBoxes(self, numBoxes, hNum = 0, vNum = 0):
		self.guideBox = GuideBox("guideBox", hNum = hNum, vNum = vNum)
		self.boxes = [Box("box%s"%i) for i in range(numBoxes)]

	def bindContainer(self, containerPaine):
		self.appendConstraint(self.guideBox.left == containerPaine.left)
		self.appendConstraint(self.guideBox.top == containerPaine.top)
		self.appendConstraint(self.guideBox.right == containerPaine.right)
		self.appendConstraint(self.guideBox.bottom == containerPaine.bottom)

	def setAsGuideBox(self, box):
		guideBox = self.guideBox

		self.appendConstraint(box.left == guideBox.left)
		self.appendConstraint(box.top == guideBox.top)
		self.appendConstraint(box.right == guideBox.right)
		self.appendConstraint(box.bottom == guideBox.bottom)

	def setupCommonBoxes(self):
		self.appendCompoundConstraint(self.guideBox)
		for box in self.boxes:
			self.appendCompoundConstraint(box)

	def setupGuideWeights(self, hWeights = None, vWeights = None):
		self.guideBox.setupWeights(hWeights, vWeights)

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

		self.problemPrototype = {
				(JointOperator.Silkworm, 2): self.generateBaseLayoutProblem(JointOperator.Silkworm, numWeights=2),
				(JointOperator.Silkworm, 3): self.generateBaseLayoutProblem(JointOperator.Silkworm, numWeights=3),
				(JointOperator.Silkworm, 4): self.generateBaseLayoutProblem(JointOperator.Silkworm, numWeights=4),
				(JointOperator.Silkworm, 5): self.generateBaseLayoutProblem(JointOperator.Silkworm, numWeights=5),
				(JointOperator.Goose, 2): self.generateBaseLayoutProblem(JointOperator.Goose, numWeights=2),
				(JointOperator.Goose, 3): self.generateBaseLayoutProblem(JointOperator.Goose, numWeights=3),
				(JointOperator.Goose, 4): self.generateBaseLayoutProblem(JointOperator.Goose, numWeights=4),
				(JointOperator.Goose, 5): self.generateBaseLayoutProblem(JointOperator.Goose, numWeights=5),

				JointOperator.Loop: self.generateBaseLayoutProblem(JointOperator.Loop),
				JointOperator.Qi: self.generateBaseLayoutProblem(JointOperator.Qi),
				JointOperator.Liao: self.generateBaseLayoutProblem(JointOperator.Liao),
				JointOperator.Zai: self.generateBaseLayoutProblem(JointOperator.Zai),
				JointOperator.Dou: self.generateBaseLayoutProblem(JointOperator.Dou),

				JointOperator.Mu: self.generateBaseLayoutProblem(JointOperator.Mu),
				JointOperator.Zuo: self.generateBaseLayoutProblem(JointOperator.Zuo),
				JointOperator.You: self.generateBaseLayoutProblem(JointOperator.You),
				JointOperator.Liang: self.generateBaseLayoutProblem(JointOperator.Liang),
				JointOperator.Jia: self.generateBaseLayoutProblem(JointOperator.Jia),
				}

	def generateBaseLayoutProblem(self, operator, numWeights = None):
		layoutProblem = LayoutProblem()
		if operator == JointOperator.Goose:
			layoutProblem.initCommonBoxes(numWeights, hNum = numWeights - 1)
			layoutProblem.setupForGoose()
		elif operator == JointOperator.Silkworm:
			layoutProblem.initCommonBoxes(numWeights, vNum = numWeights - 1)
			layoutProblem.setupForSilkworm()
		elif operator == JointOperator.Loop:
			layoutProblem.initCommonBoxes(2, hNum = 2, vNum = 2)
			layoutProblem.setupForLoop()
		elif operator == JointOperator.Qi:
			layoutProblem.initCommonBoxes(2, hNum = 1, vNum = 1)
			layoutProblem.setupForQi()
		elif operator == JointOperator.Liao:
			layoutProblem.initCommonBoxes(2, hNum = 1, vNum = 1)
			layoutProblem.setupForLiao()
		elif operator == JointOperator.Zai:
			layoutProblem.initCommonBoxes(2, hNum = 1, vNum = 1)
			layoutProblem.setupForZai()
		elif operator == JointOperator.Dou:
			layoutProblem.initCommonBoxes(2, hNum = 1, vNum = 1)
			layoutProblem.setupForDou()
		elif operator == JointOperator.Mu:
			layoutProblem.initCommonBoxes(3, hNum = 1, vNum = 1)
			layoutProblem.setupForMu()
		elif operator == JointOperator.Zuo:
			layoutProblem.initCommonBoxes(3, hNum = 1, vNum = 1)
			layoutProblem.setupForZuo()
		elif operator == JointOperator.You:
			layoutProblem.initCommonBoxes(3, hNum = 4, vNum = 1)
			layoutProblem.setupForYou()
		elif operator == JointOperator.Liang:
			layoutProblem.initCommonBoxes(3, hNum = 4, vNum = 1)
			layoutProblem.setupForLiang()
		elif operator == JointOperator.Jia:
			layoutProblem.initCommonBoxes(3, hNum = 2, vNum = 2)
			layoutProblem.setupForJia()
		else:
			pass
		return layoutProblem

	def extractWeights(self, spec: LayoutSpec):
		operator = spec.operator

		hWeights = []
		vWeights = []
		if operator == JointOperator.Goose:
			hWeights = spec.weights
			vWeights = None
		elif operator == JointOperator.Silkworm:
			hWeights = None
			vWeights = spec.weights
		elif operator == JointOperator.Loop:
			hWeights = None
			vWeights = None
		elif operator == JointOperator.Qi:
			hWeights = None
			vWeights = None
		elif operator == JointOperator.Liao:
			hWeights = None
			vWeights = None
		elif operator == JointOperator.Zai:
			hWeights = None
			vWeights = None
		elif operator == JointOperator.Dou:
			hWeights = None
			vWeights = None
		elif operator == JointOperator.Mu:
			hWeights = None
			vWeights = None
		elif operator == JointOperator.Zuo:
			hWeights = None
			vWeights = None
		elif operator == JointOperator.You:
			hWeights = [1, 3, 2, 3, 1]
			vWeights = [4, 1]
		elif operator == JointOperator.Liang:
			hWeights = [1, 3, 2, 3, 1]
			vWeights = [1, 4]
		elif operator == JointOperator.Jia:
			hWeights = [4, 2, 4]
			vWeights = [2, 6, 2]
		else:
			pass
		return (hWeights, vWeights)

	def getCopyFromProtopty(self, spec: LayoutSpec):
		operator = spec.operator

		if operator in [JointOperator.Goose, JointOperator.Silkworm]:
			key = (operator, len(spec.weights))
		else:
			key = operator

		prototype = self.problemPrototype.get(key)
		if not prototype:
			numWeights = len(spec.weights) if spec.weights != None else None
			prototype = self.generateBaseLayoutProblem(spec.operator, numWeights)
			self.problemPrototype[key] = prototype

		layoutProblem = copy.deepcopy(prototype)
		return layoutProblem

	def generateLayoutProblem(self, spec: LayoutSpec):
		layoutProblem = self.getCopyFromProtopty(spec)
		(hWeights, vWeights) = self.extractWeights(spec)
		layoutProblem.setupGuideWeights(hWeights = hWeights, vWeights = vWeights)
		layoutProblem.setupCommonBoxes()
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

