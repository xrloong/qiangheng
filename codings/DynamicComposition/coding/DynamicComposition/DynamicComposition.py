import abc

from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser
from coding.Base import CodeMappingInfoInterpreter

from parser.GlyphParser import GlyphTags
from parser.GlyphParser import GlyphParser
from parser.GlyphParser import IfGlyphDescriptionInterpreter
from parser.GlyphParser import GlyphElementDescription
from parser.GlyphParser import GlyphStrokeDescription, GlyphComponentDescription
from parser.GlyphParser import GlyphDataSetDescription

try:
	import xie
except ImportError as e:
	import sys
	message = """
	動態組字使用 Xie 來描繪字形。
	可到 https://github.com/xrloong/Xie 下載最新版本，並以 pip 安裝，或使可使用以下指令：
	$ pip3 install https://github.com/xrloong/Xie/releases/download/v0.1.4/Xie-0.1.4-py3-none-any.whl
"""
	print(message, file=sys.stderr)
	sys.exit(1)

from xie.graphics import Pane
from xie.graphics import BaseTextCanvasController
from xie.graphics import DrawingSystem
from xie.graphics import Component
from xie.graphics import Character

from xie.graphics import StrokeSpec

from xie.graphics import StrokeFactory
from xie.graphics import ComponentFactory

from .layout import JointOperator
from .layout import LayoutFactory
from .layout import LayoutSpec

class DCComponent:
	componentFactory = ComponentFactory()

	def __init__(self, component):
		self.component=component
		self.extraPaneDB={DCCodeInfo.PANE_NAME_DEFAULT : component.getStatePane()}

	def getCount(self):
		return self.component.getCount()

	def getComponent(self):
		return self.component

	def generateComponent(self, pane):
		componentFactory = DCComponent.componentFactory
		return componentFactory.generateComponentByComponentPane(self.component, pane)

	def setExtraPaneDB(self, extranPaneDB):
		self.extraPaneDB=extranPaneDB
		self.extraPaneDB[DCCodeInfo.PANE_NAME_DEFAULT]=self.component.getStatePane()

	def setExtraPane(self, paneName, extraPane):
		self.extraPaneDB[paneName]=extraPane

	def getExtraPane(self, paneName):
		return self.extraPaneDB.get(paneName, None)

	def getComponentPane(self):
		return self.component.getStatePane()

	@staticmethod
	def generateDefaultComponent(components, panes):
		assert len(components) == len(panes)
		dcComponentPanePairList = zip(components, panes)

		componentFactory = DCComponent.componentFactory
		componentPanePairs = [(dcComponent.getComponent(), pane) for dcComponent, pane in dcComponentPanePairList]
		component = componentFactory.generateComponentByComponentPanePairs(componentPanePairs)
		dcComponent = DCComponent(component)
		return dcComponent

	@staticmethod
	def generateComponentByStrokes(strokeList):
		componentFactory = DCComponent.componentFactory
		component = componentFactory.generateComponentByStrokes(strokeList)
		return DCComponent(component)

class DCCodeInfo(CodeInfo):
	PANE_NAME_DEFAULT="瑲珩預設範圍名稱"

	PANE_NAME_LOOP="回"
	PANE_NAME_QI="起"
	PANE_NAME_LIAO="廖"
	PANE_NAME_DAO="斗"
	PANE_NAME_ZAI="載"

	PANE_NAME_MU_1="畞:1"
	PANE_NAME_MU_2="畞:2"

	PANE_NAME_YOU_1="幽:1"
	PANE_NAME_YOU_2="幽:2"

	PANE_NAME_LIANG_1="㒳:1"
	PANE_NAME_LIANG_2="㒳:2"

	PANE_NAME_JIA_1="夾:1"
	PANE_NAME_JIA_2="夾:2"

	PANE_NAME_ZUO_1="㘴:1"
	PANE_NAME_ZUO_2="㘴:2"

	def __init__(self, component):
		super().__init__()

		self.component = component

	@staticmethod
	def generateDefaultCodeInfo(components, panes):
		component = DCComponent.generateDefaultComponent(components, panes)
		codeInfo = DCCodeInfo(component)
		return codeInfo

	def toCode(self):
		component=self.getComponent()
		return component

	def setExtraPane(self, paneName, extraPane):
		component = self.getComponent()
		component.setExtraPane(paneName, extraPane)

	def getExtraPane(self, paneName):
		component = self.getComponent()
		return component.getExtraPane(paneName)

	def getComponent(self):
		return self.component

	def getComponentPane(self):
		return self.component.getComponentPane()

	def getStrokeCount(self):
		return self.getComponent().getCount()

class DCCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		super().__init__()
		self.layoutFactory = LayoutFactory()

	def generateDefaultCodeInfo(self, codeInfos, layoutSpec: LayoutSpec):
		panes = self.layoutFactory.generateLayouts(layoutSpec)
		components = [codeInfo.getComponent() for codeInfo in codeInfos]

		return DCCodeInfo.generateDefaultCodeInfo(components, panes)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getStrokeCount()>0, codeInfoList))
		return isAllWithCode

	def generateEmbedLayoutSpec(self, operator, codeInfos, paneNames):
		containerCodeInfo = codeInfos[0]

		containerPane = containerCodeInfo.getComponentPane()
		layoutSpec = LayoutSpec(operator, containerPane = containerPane)
		return layoutSpec

	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		print("不合法的運算：龜", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """
		print("不合法的運算：龍", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsSparrow(self, codeInfoList):
		"""運算 "雀" """
		print("不合法的運算：雀", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		firstCodeInfo=codeInfoList[0]
		return firstCodeInfo


	def encodeAsLoop(self, codeInfos):
		layoutSpec = self.generateEmbedLayoutSpec(JointOperator.Loop,
				codeInfos, [DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_LOOP])
		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)

		# 颱=(起 風台), 是=(回 [風外]䖝)
		firstCodeInfo = codeInfos[0]
		if firstCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, firstCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI))
		return codeInfo

	def encodeAsSilkworm(self, codeInfos):
		weights = list(map(lambda x: x.getStrokeCount()+1, codeInfos))
		layoutSpec = LayoutSpec(JointOperator.Silkworm, weights = weights)

		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)

		lastCodeInfo = codeInfos[-1]
		# 題=(起 是頁), 是=(志 日[是下])
		if lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI))

		return codeInfo

	def encodeAsGoose(self, codeInfos):
		weights = list(map(lambda x: x.getStrokeCount(), codeInfos))
		layoutSpec = LayoutSpec(JointOperator.Goose, weights = weights)

		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)
		return codeInfo

	def encodeAsQi(self, codeInfos):
		layoutSpec = self.generateEmbedLayoutSpec(JointOperator.Qi,
				codeInfos, [DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_QI])
		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)
		return codeInfo

	def encodeAsLiao(self, codeInfos):
		layoutSpec = self.generateEmbedLayoutSpec(JointOperator.Liao,
				codeInfos, [DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_LIAO])
		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)

		lastCodeInfo = codeInfos[-1]
		# 屗=(起 尾寸), 尾=(志 尸毛)
		if lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI))
		return codeInfo

	def encodeAsZai(self, codeInfos):
		layoutSpec = self.generateEmbedLayoutSpec(JointOperator.Zai,
				codeInfos, [DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_ZAI])
		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)
		return codeInfo

	def encodeAsDou(self, codeInfos):
		layoutSpec = self.generateEmbedLayoutSpec(JointOperator.Dou,
				codeInfos, [DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_DOU])
		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)
		return codeInfo


	def encodeAsMu(self, codeInfos):
		layoutSpec = self.generateEmbedLayoutSpec(JointOperator.Mu,
				codeInfos, [DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_MU_1, DCCodeInfo.PANE_NAME_MU_2])
		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)
		return codeInfo

	def encodeAsZuo(self, codeInfos):
		layoutSpec = self.generateEmbedLayoutSpec(JointOperator.Zuo,
				codeInfos, [DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_ZUO_1, DCCodeInfo.PANE_NAME_ZUO_2])
		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)
		return codeInfo

	def encodeAsYou(self, codeInfos):
		layoutSpec = self.generateEmbedLayoutSpec(JointOperator.You,
				codeInfos, [DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_YOU_1, DCCodeInfo.PANE_NAME_YOU_2])
		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)
		return codeInfo

	def encodeAsLiang(self, codeInfos):
		layoutSpec = self.generateEmbedLayoutSpec(JointOperator.Liang,
				codeInfos, [DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_LIANG_1, DCCodeInfo.PANE_NAME_LIANG_2])
		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)
		return codeInfo

	def encodeAsJia(self, codeInfos):
		layoutSpec = self.generateEmbedLayoutSpec(JointOperator.Jia,
				codeInfos, [DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_JIA_1, DCCodeInfo.PANE_NAME_JIA_2])
		codeInfo = self.generateDefaultCodeInfo(codeInfos, layoutSpec)
		return codeInfo

class DCRadixParser(CodingRadixParser):
	TAG_STROKE_GROUP='筆劃組'
	TAG_STROKE='筆劃'
	TAG_GEOMETRY='幾何'
	TAG_SCOPE='範圍'
	TAG_STROKE='筆劃'
	TAG_NAME='名稱'
	TAG_EXTRA_SCOPE='補充範圍'
	TAG_TYPE='類型'
	TAG_START_POINT='起始點'
	TAG_PARAMETER='參數'
	TAG_BBOX='字面框'

	TAG_CODE_INFORMATION='編碼資訊'
	ATTRIB_CODE_EXPRESSION='資訊表示式'

	TAG_CHARACTER_SET='字符集'
	TAG_CHARACTER='字符'

	TAG_NAME='名稱'

	def __init__(self):
		self.glyphParser = GlyphParser()
		self.templateManager = TemplateManager()

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		componentNodeList=elementCodeInfo.get(DCRadixParser.ATTRIB_CODE_EXPRESSION)
		lastComponentNode = componentNodeList[0]

		component = self.parseComponent(lastComponentNode)

		codeInfo = DCCodeInfo(component)
		return codeInfo

	def parseRadixInfo(self, rootNode):
		characterSetNode=rootNode.get(DCRadixParser.TAG_CHARACTER_SET)
		for characterNode in characterSetNode:
			charName=characterNode.get(DCRadixParser.TAG_NAME)
			radixDescription=self.parseRadixDescription(characterNode)

			self.radixDescriptionManager.addDescription(charName, radixDescription)

	def parseExtraScopeDB(self, elementCodeInfo):
		extraPaneDB={}

		extraScopeNodeList=elementCodeInfo.get(DCRadixParser.TAG_EXTRA_SCOPE)
		if extraScopeNodeList != None:
			for extraScopeNode in extraScopeNodeList:
				paneName=extraScopeNode.get(DCRadixParser.TAG_NAME)
				pane=self.parseExtraScope(extraScopeNode)

				extraPaneDB[paneName]=pane

		return extraPaneDB

	def parseExtraScope(self, extraScopeNode):
		descriptionRegion=extraScopeNode.get(DCRadixParser.TAG_SCOPE)
		pane=self.parsePane(descriptionRegion)
		return pane

	def parseGeometry(self, geometryNode):
		descriptionRegion=geometryNode.get(DCRadixParser.TAG_SCOPE)
		pane=self.parsePane(descriptionRegion)
		return pane

	def parseComponent(self, componentNode):
		extraPaneDB = self.parseExtraScopeDB(componentNode)
		strokeNode = componentNode.get(DCRadixParser.TAG_STROKE)
		strokes = self.parseStrokes(strokeNode)

		component = DCComponent.generateComponentByStrokes(strokes)
		component.setExtraPaneDB(extraPaneDB)
		return component

	def parseStrokes(self, strokeNode):
		strokes=[]
		for strokeNode in strokeNode:
			element = self.glyphParser.parseElement(strokeNode)
			assert element.isReference

			tempStrokes = self.templateManager.interpretStrokeByReference(element)
			strokes.extend(tempStrokes)
		return strokes

	def parsePane(self, descriptionRegion):
		left=int(descriptionRegion[0:2], 16)
		top=int(descriptionRegion[2:4], 16)
		right=int(descriptionRegion[4:6], 16)
		bottom=int(descriptionRegion[6:8], 16)
		return Pane(left, top, right, bottom)

class GlyphDescriptionInterpreter(IfGlyphDescriptionInterpreter):
	def __init__(self):
		super().__init__()
		self.componentFactory = ComponentFactory()
		self.strokeFactory = StrokeFactory()

		self.anchors = {}
		self.templates = {}

	def getStroke(self, name, index):
		component=self.templates.get(name)
		return component.getStrokeList()[index]

	def applyComponentWithTransformation(self, component, position):
		if position != None:
			pane = Pane(*position)
			component = self.componentFactory.generateComponentByComponentPane(component, pane)
		return component

	def getComponent(self, name):
		component = self.anchors.get(name)
		if not component:
			component = self.templates.get(name)
		return component

	def interpretStrokeByDefinition(self, element):
		strokeType = element.strokeType
		params = element.params
		startPoint = element.startPoint
		position = element.position
		pane = Pane(*position)
		splinePointsList = element.splinePointsList

		if splinePointsList:
			strokeSpec = StrokeSpec(strokeType, splinePointsList = splinePointsList)
		else:
			strokeSpec = StrokeSpec(strokeType, params)
		stroke = self.strokeFactory.generateStrokeBySpec(strokeSpec, strokeBoundPane = pane)
		return stroke

	def interpretStrokeByReference(self, element: GlyphElementDescription):
		referenceName = element.referenceName
		order = element.order
		position = element.position

		referencedComponent = self.getComponent(referenceName)
		strokes = self.retrieveStrokesOfComponentIntoPosition(referencedComponent, order, position)
		return strokes

	def retrieveStrokesOfComponentIntoPosition(self, referencedComponent: Component, order: [int], position):
		strokes = list((referencedComponent.getStroke(index) for index in order))
		component = self.componentFactory.generateComponentByStrokes(strokes)

		component = self.applyComponentWithTransformation(component, position)
		return component.getStrokeList()

	def interpretElement(self, element: GlyphElementDescription):
		strokes = []

		if element.isReference:
			strokes = self.interpretStrokeByReference(element)
		elif element.isAnchor:
			anchorName = element.name
			referenceName = element.referenceName
			position = element.position

			referencedComponent = self.getComponent(referenceName)
			component = self.applyComponentWithTransformation(referencedComponent, position)

			self.anchors[anchorName] = component
		elif element.isDefinition:
			stroke = self.interpretStrokeByDefinition(element)
			strokes = [stroke]
		else:
			assert False
		return strokes

	def interpretStroke(self, stroke: GlyphStrokeDescription):
		element = stroke.element
		strokes = self.interpretElement(element)

		component = self.componentFactory.generateComponentByStrokes(strokes)
		return component

	def interpretComponent(self, component: GlyphComponentDescription):
		self.anchors.clear()

		strokes = []
		for element in component.elements:
			subStrokes = self.interpretElement(element)
			strokes.extend(subStrokes)

		component = self.componentFactory.generateComponentByStrokes(strokes)
		return component

	def interpretDataSet(self, glyphDataSet: GlyphDataSetDescription):
		for strokeDesc in glyphDataSet.strokes:
			name = strokeDesc.name
			stroke = self.interpretStroke(strokeDesc)

			self.templates[name] = stroke

		for partDesc in glyphDataSet.parts:
			name = partDesc.name
			part = self.interpretComponent(partDesc)

			self.templates[name] = part

		for componentDesc in glyphDataSet.components:
			name = componentDesc.name
			component = self.interpretComponent(componentDesc)

			self.templates[name] = component
		return self.templates

class TemplateManager:
	def __init__(self):
		super().__init__()
		self.interpreter = GlyphDescriptionInterpreter()
		self.templates = {}
		self.load()

	def put(self, name, template):
		assert isinstance(template, Component)
		self.templates[name]=template

	def get(self, name):
		return self.templates.get(name)

	def load(self):
		from . import CodingTemplateFile
		filename = CodingTemplateFile

		glyphParser = GlyphParser()
		glyphDataSet = glyphParser.load(filename)

		dataSet = self.interpreter.interpretDataSet(glyphDataSet)
		self.templates.update(dataSet)

	def interpretStrokeByReference(self, element: GlyphElementDescription):
		referenceName = element.referenceName
		order = element.order
		position = element.position

		referencedComponent = self.get(referenceName)
		strokes = self.interpreter.retrieveStrokesOfComponentIntoPosition(referencedComponent, order, position)
		return strokes

class YamlCanvasController(BaseTextCanvasController):
	def __init__(self):
		super().__init__()
		self.strokes = []

	def getStrokes(self):
		return self.strokes

	def onPreDrawCharacter(self, character):
		self.strokes=[]

	def onPreDrawStroke(self, stroke):
		self.clearStrokeExpression()

	def onPostDrawStroke(self, stroke):
		e=self.getStrokeExpression()
		if e:
			attrib={
				"名稱": stroke.getName(),
				"描繪": e,
				}
			self.strokes.append(attrib)


# YAML writer for drawing methods
class DmCodeMappingInfoInterpreter(CodeMappingInfoInterpreter):
	def __init__(self, codingType):
		super().__init__(codingType)

	def interpreteCodeMappingInfo(self, codeMappingInfo):
		charName = codeMappingInfo.getName()
		dcComponent = codeMappingInfo.getCode()
		variance = codeMappingInfo.getVariance()

		component = dcComponent.getComponent()
		character = Character(charName, component)

		controller = YamlCanvasController()
		ds = DrawingSystem(controller)

		ds.draw(character)

		code = controller.getStrokes()

		return {"字符": charName, "類型":variance, "字圖":code}

