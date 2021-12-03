import abc

from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser
from coding.Base import CodeMappingInfoInterpreter

try:
	import xie
except ImportError as e:
	import sys
	message = """
	動態組字使用 Xie 來描繪字形。
	可到 https://github.com/xrloong/Xie 下載最新版本，並以 pip 安裝，或使可使用以下指令：
	$ pip3 install https://github.com/xrloong/Xie/releases/download/v0.0.9/Xie-0.0.9-py3-none-any.whl
"""
	print(message, file=sys.stderr)
	sys.exit(1)

from xie.graphics import Pane
from xie.graphics import BaseTextCanvasController
from xie.graphics import DrawingSystem
from xie.graphics import Component, ComponentInfo
from xie.graphics import Character
from xie.graphics import ShapeFactory


class DCComponent:
	shapeFactory = ShapeFactory()

	def __init__(self, component):
		self.component=component
		self.extraPaneDB={DCCodeInfo.PANE_NAME_DEFAULT : component.getStatePane()}

	def getCount(self):
		return self.component.getCount()

	def getComponent(self):
		return self.component

	def generateComponent(self, pane):
		shapeFactory=DCComponent.shapeFactory
		return shapeFactory.generateComponentByComponentPane(self.component, pane)

	def setExtraPaneDB(self, extranPaneDB):
		self.extraPaneDB=extranPaneDB
		self.extraPaneDB[DCCodeInfo.PANE_NAME_DEFAULT]=self.component.getStatePane()

	def setExtraPane(self, paneName, extraPane):
		self.extraPaneDB[paneName]=extraPane

	def getExtraPane(self, paneName):
		return self.extraPaneDB.get(paneName, None)

	@staticmethod
	def generateDefaultComponent(dcComponentPanePairList):
		shapeFactory=DCComponent.shapeFactory
		componentPanePair=[(dcComponent.getComponent(), pane) for dcComponent, pane in dcComponentPanePairList]
		component=shapeFactory.generateComponentByComponentPanePairList(componentPanePair)
		dcComponent=DCComponent(component)
		return dcComponent

	@staticmethod
	def generateComponentByStrokeList(strokeList):
		shapeFactory=DCComponent.shapeFactory
		component = shapeFactory.generateComponentByStrokeList(strokeList)
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

	STROKE_GROUP_NAME_DEFAULT="瑲珩預設筆劃組名稱"

	STROKE_GROUP_NAME_LOOP="回"
	STROKE_GROUP_NAME_QI="起"
	STROKE_GROUP_NAME_LIAO="廖"
	STROKE_GROUP_NAME_DAO="斗"
	STROKE_GROUP_NAME_ZAI="載"

	STROKE_GROUP_NAME_MU="畞"
	STROKE_GROUP_NAME_YOU="幽"
	STROKE_GROUP_NAME_LIANG="㒳"
	STROKE_GROUP_NAME_JIA="夾"
	STROKE_GROUP_NAME_ZUO="㘴"

	def __init__(self, componentDB):
		super().__init__()

		self.componentDB=componentDB

	@staticmethod
	def generateDefaultCodeInfo(componentPanePair):
		component=DCComponent.generateDefaultComponent(componentPanePair)
		componentDB={DCCodeInfo.STROKE_GROUP_NAME_DEFAULT : component}

		codeInfo=DCCodeInfo(componentDB)
		return codeInfo

	def toCode(self):
		component=self.getComponent()
		return component

	def setExtraPane(self, componentName, paneName, extraPane):
		component=self.getComponent(componentName)

		if component==None:
			component=self.getComponent()

		component.setExtraPane(paneName, extraPane)

	def getExtraPane(self, componentName, paneName):
		component=self.getComponent(componentName)

		if component==None:
			component=self.getComponent()

		return component.getExtraPane(paneName)

	def getComponent(self, componentName=STROKE_GROUP_NAME_DEFAULT):
		component=self.componentDB.get(componentName)
		if componentName!=DCCodeInfo.STROKE_GROUP_NAME_DEFAULT and component==None:
			component=self.getComponent(DCCodeInfo.STROKE_GROUP_NAME_DEFAULT)
		return component

	def getStrokeCount(self):
		return self.getComponent().getCount()

class DCCodeInfoEncoder(CodeInfoEncoder):
	def generateDefaultCodeInfo(self, componentPanePair):
		return DCCodeInfo.generateDefaultCodeInfo(componentPanePair)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getStrokeCount()>0, codeInfoList))
		return isAllWithCode

	def extendComponentNameList(self, componentNameList, codeInfoList):
		lenNameList=len(componentNameList)
		lenCodeInfoList=len(codeInfoList)
		extendingList=[]
		if lenCodeInfoList>lenNameList:
			diff=lenCodeInfoList-lenNameList
			extendingList=[DCCodeInfo.STROKE_GROUP_NAME_DEFAULT for i in range(diff)]
		return componentNameList+extendingList

	def splitLengthToList(self, length, weightList):
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

	def encodeByEmbed(self, codeInfoList, componentNameList, paneNameList):
		if len(codeInfoList)<2:
			return self.encodeAsInvalidate(codeInfoList)

		containerCodeInfo=codeInfoList[0]

		newComponentList=[]
		for [componentName, paneName, codeInfo] in zip(componentNameList, paneNameList, codeInfoList):
			extraPane=containerCodeInfo.getExtraPane(componentName, paneName)
			assert extraPane!=None, "extraPane 不應為 None 。%s: %s"%(paneName, str(containerCodeInfo))

			component=codeInfo.getComponent(componentName).generateComponent(extraPane)
			newComponentList.append(component)

		paneList=[]
		for [componentName, paneName] in zip(componentNameList, paneNameList):
			extraPane=containerCodeInfo.getExtraPane(componentName, paneName)
			assert extraPane!=None, "extraPane 不應為 None 。%s: %s"%(paneName, str(containerCodeInfo))
			paneList.append(extraPane)

		componentList=[]
		for [componentName, codeInfo] in zip(componentNameList, codeInfoList):
			component=codeInfo.getComponent(componentName)
			componentList.append(component)

		componentPanePair=zip(componentList, paneList)
		codeInfo=self.generateDefaultCodeInfo(componentPanePair)
		return codeInfo


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


	def encodeAsLoop(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		codeInfo=self.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_LOOP, DCCodeInfo.STROKE_GROUP_NAME_LOOP],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_LOOP])
		# 颱=(起 風台), 是=(回 [風外]䖝)
		if firstCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI, firstCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI))
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		def genPaneList(weightList):
			pane=Pane.BBOX
			pointList=self.splitLengthToList(pane.getHeight(), weightList)
			paneList=[]
			offset=pane.getTop()
			for [pointStart, pointEnd] in zip(pointList[:-1], pointList[1:]):
				height=pointEnd-pointStart
				targetHeight=int(height*0.90)
				offset=int(height-targetHeight)//2
				tmpPane=Pane(pane.getLeft(), pointStart+offset, pane.getRight(), pointEnd-offset)
				tmpPane.offsetTopAndBottom(offset)
				paneList.append(tmpPane)
			return paneList

		weightList=list(map(lambda x: x.getStrokeCount()+1, codeInfoList))
		paneList=genPaneList(weightList)

		componentNameList=self.extendComponentNameList(['蚕'], codeInfoList)

		componentList=[]
		for [componentName, codeInfo] in zip(componentNameList, codeInfoList):
			component=codeInfo.getComponent(componentName)
			componentList.append(component)

		componentPanePair=zip(componentList, paneList)
		codeInfo=self.generateDefaultCodeInfo(componentPanePair)

		lastCodeInfo=codeInfoList[-1]
		# 題=(起 是頁), 是=(志 日[是下])
		if lastCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI, lastCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI))

		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		def genPaneList(weightList):
			pane=Pane.BBOX
			pointList=self.splitLengthToList(pane.getWidth(), weightList)
			paneList=[]
			offset=pane.getLeft()
			for [pointStart, pointEnd] in zip(pointList[:-1], pointList[1:]):
				width=pointEnd-pointStart
				targetWidth=int(width*0.90)
				offset=int(width-targetWidth)//2
				tmpPane=Pane(pointStart+offset, pane.getTop(), pointEnd-offset, pane.getBottom())
				tmpPane.offsetLeftAndRight(offset)
				paneList.append(tmpPane)
			return paneList

		weightList=list(map(lambda x: x.getStrokeCount(), codeInfoList))
		paneList=genPaneList(weightList)

		componentNameList=self.extendComponentNameList(['鴻'], codeInfoList)

		componentList=[]
		for [componentName, codeInfo] in zip(componentNameList, codeInfoList):
			component=codeInfo.getComponent(componentName)
			componentList.append(component)

		componentPanePair=zip(componentList, paneList)
		codeInfo=self.generateDefaultCodeInfo(componentPanePair)
		return codeInfo

	def encodeAsQi(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.STROKE_GROUP_NAME_QI],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_QI])

	def encodeAsLiao(self, codeInfoList):
		codeInfo=self.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_LIAO, DCCodeInfo.STROKE_GROUP_NAME_LIAO],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_LIAO])

		lastCodeInfo=codeInfoList[-1]
		# 屗=(起 尾寸), 尾=(志 尸毛)
		if lastCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI, lastCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI))
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_ZAI, DCCodeInfo.STROKE_GROUP_NAME_ZAI],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_ZAI])

	def encodeAsDou(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_DOU, DCCodeInfo.STROKE_GROUP_NAME_DOU],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_DOU])


	def encodeAsMu(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_MU, DCCodeInfo.STROKE_GROUP_NAME_MU, DCCodeInfo.STROKE_GROUP_NAME_MU],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_MU_1, DCCodeInfo.PANE_NAME_MU_2])

	def encodeAsZuo(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_ZUO, DCCodeInfo.STROKE_GROUP_NAME_ZUO, DCCodeInfo.STROKE_GROUP_NAME_ZUO],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_ZUO_1, DCCodeInfo.PANE_NAME_ZUO_2])

	def encodeAsYou(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_YOU, DCCodeInfo.STROKE_GROUP_NAME_YOU, DCCodeInfo.STROKE_GROUP_NAME_YOU],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_YOU_1, DCCodeInfo.PANE_NAME_YOU_2])

	def encodeAsLiang(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_LIANG, DCCodeInfo.STROKE_GROUP_NAME_LIANG, DCCodeInfo.STROKE_GROUP_NAME_LIANG],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_LIANG_1, DCCodeInfo.PANE_NAME_LIANG_2])

	def encodeAsJia(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_JIA, DCCodeInfo.STROKE_GROUP_NAME_JIA, DCCodeInfo.STROKE_GROUP_NAME_JIA, ],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_JIA_1, DCCodeInfo.PANE_NAME_JIA_2])

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
		self.shapeFactory=ShapeFactory()
		self.templateManager=TemplateManager(self.shapeFactory)

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		componentDB={}

		componentNodeList=elementCodeInfo.get(DCRadixParser.ATTRIB_CODE_EXPRESSION)
		for componentNode in componentNodeList:
			[componentName, component]=self.parseComponent(componentNode)

			extraPaneDB=self.parseExtraScopeDB(componentNode)
			component.setExtraPaneDB(extraPaneDB)

			if componentName==None:
				componentName=DCCodeInfo.STROKE_GROUP_NAME_DEFAULT
			componentDB[componentName]=component

		codeInfo=DCCodeInfo(componentDB)
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
		componentName=componentNode.get(DCRadixParser.TAG_NAME)

		t=componentNode.get(DCRadixParser.TAG_STROKE_GROUP)
		strokeList=self.parseStrokeList(t)

		component=DCComponent.generateComponentByStrokeList(strokeList)
		return [componentName, component]

	def parseStrokeList(self, componentNode):
		strokeList=[]
		strokeNodeList=componentNode.get(DCRadixParser.TAG_STROKE)
		for strokeNode in strokeNodeList:
			method=strokeNode.get(TemplateManager.TAG_METHOD, TemplateManager.TAG_METHOD__DEFINITION)
			if method==TemplateManager.TAG_METHOD__REFERENCE:
				tempStrokes=self.templateManager.parseStrokeByReference(strokeNode, self.templateManager)
				strokeList.extend(tempStrokes)
			elif method==TemplateManager.TAG_METHOD__DEFINITION:
				stroke=DCRadixParser.fromStrokeNode(strokeNode, self.shapeFactory)
				strokeList.append(stroke)
		return strokeList

	@staticmethod
	def fromStrokeNode(strokeNode, shapeFactory):
		name=strokeNode.get(DCRadixParser.TAG_TYPE)
		startPoint=strokeNode.get(DCRadixParser.TAG_START_POINT)
		parameterList = strokeNode.get(DCRadixParser.TAG_PARAMETER)
		return shapeFactory.generateParameterBasedStroke(name, parameterList, startPoint)

	def parsePane(self, descriptionRegion):
		left=int(descriptionRegion[0:2], 16)
		top=int(descriptionRegion[2:4], 16)
		right=int(descriptionRegion[4:6], 16)
		bottom=int(descriptionRegion[6:8], 16)
		return Pane(left, top, right, bottom)

class AbsTemplateManager(object, metaclass=abc.ABCMeta):
	def __init__(self):
		pass

	def put(self, name, template):
		raise NotImplementedError('users must define put to use this base class')

	def get(self, name):
		raise NotImplementedError('users must define get to use this base class')
		return None

class AnchorTemplateManager(AbsTemplateManager):
	def __init__(self):
		super().__init__()
		self.anchors={}

	def put(self, name, template):
		assert isinstance(template, Component)
		self.anchors[name]=template

	def get(self, name):
		return self.anchors.get(name)

class CompositionTemplateManager(AbsTemplateManager):
	def __init__(self, templateManagers):
		super().__init__()
		self.templateManagers=templateManagers

	"""
	def put(self, name, template):
		assert isinstance(template, Component)
		self.anchors[name]=template
	"""

	def get(self, name):
		for templateManager in self.templateManagers:
			sg=templateManager.get(name)
			if sg:
				return sg

class TemplateManager(AbsTemplateManager):
	TAG_TEMPLATE_SET = "樣式集"
	TAG_STROKE_GROUP='筆劃組'
	TAG_STROKE='筆劃'
	TAG_NAME='名稱'

	TAG_METHOD='方式'
	TAG_TYPE='類型'
	TAG_START_POINT='起始點'
	TAG_PARAMETER='參數'

	TAG_METHOD__DEFINITION='定義'
	TAG_METHOD__REFERENCE='引用'
	TAG_METHOD__ANCHOR='錨點'

	TAG_REFRENCE_NAME='引用名稱'
	TAG_ORDER='順序'
	TAG_TRANSFORMATION='變換'

	TAG_POSITION='定位'
	TAG_TRANSLATION='平移'
	TAG_SCALING='縮放'

	TAG_PIVOT='樞軸點'
	TAG_RATIO='比例'

	def __init__(self, shapeFactory):
		super().__init__()
		self.shapeFactory=shapeFactory
		self.templates={}
		self.load()

	def put(self, name, template):
		assert isinstance(template, Component)
		self.templates[name]=template

	def get(self, name):
		return self.templates.get(name)

	def getStroke(self, name, index):
		component=self.templates.get(name)
		return component.getStrokeList()[index]

	def getStrokes(self, name, start, end):
		component=self.templates.get(name)
		return component.getStrokeList()[start, end+1]

	def load(self):
		from . import CodingTemplateFile
		template_file = CodingTemplateFile
		self.parseTemplateFromYAML(template_file)

	def parseTemplateFromYAML(self, filename):
		import ruamel.yaml as yaml
		rootNode=yaml.load(open(filename), Loader=yaml.SafeLoader)
		self.parseTemplateSet(rootNode)

	def parseTemplateSet(self, rootNode):
		templateSetNode=rootNode.get(TemplateManager.TAG_TEMPLATE_SET)
		for templateNode in templateSetNode:
			templateName=templateNode.get(TemplateManager.TAG_NAME)
			componentNode=templateNode.get(TemplateManager.TAG_STROKE_GROUP)
			component=self.parseComponent(componentNode)
			self.put(templateName, component)

	def parseComponent(self, componentNode):
		strokes=[]
		anchorTemplateManager = AnchorTemplateManager()
		compositionTemplateManager = CompositionTemplateManager((anchorTemplateManager, self,))
		for strokeNode in componentNode.get(TemplateManager.TAG_STROKE):
			method=strokeNode.get(TemplateManager.TAG_METHOD, TemplateManager.TAG_METHOD__DEFINITION)
			if method==TemplateManager.TAG_METHOD__REFERENCE:
				tempStrokes=self.parseStrokeByReference(strokeNode, compositionTemplateManager)
				strokes.extend(tempStrokes)
			elif method==TemplateManager.TAG_METHOD__ANCHOR:
				anchorName=strokeNode.get(TemplateManager.TAG_NAME)
				component=self.parseStrokeByAnchor(strokeNode, anchorTemplateManager)
				anchorTemplateManager.put(anchorName, component)
			elif method==TemplateManager.TAG_METHOD__DEFINITION:
				stroke=self.parseStroke(strokeNode)
				strokes.append(stroke)
			else:
				assert False
		component=self.shapeFactory.generateComponentByStrokeList(strokes)
		return component

	def parseStroke(self, strokeNode):
		strokeType=strokeNode.get(TemplateManager.TAG_TYPE)
		startPoint=strokeNode.get(TemplateManager.TAG_START_POINT)
		params=strokeNode.get(TemplateManager.TAG_PARAMETER)
		stroke=self.shapeFactory.generateParameterBasedStroke(strokeType, params, startPoint)
		return stroke

	def parseStrokeByReference(self, strokeNode, templateManager):
		strokeType=strokeNode.get(TemplateManager.TAG_TYPE)
		templateName=strokeNode.get(TemplateManager.TAG_REFRENCE_NAME)
		orders=strokeNode.get(TemplateManager.TAG_ORDER)

		component=templateManager.get(templateName)
		strokes=list((component.getStroke(index) for index in orders))

		transformationNode=strokeNode.get(TemplateManager.TAG_TRANSFORMATION)
		if transformationNode != None:
			componentInfo = ComponentInfo(strokes)
			statePane = componentInfo.getInfoPane().clone()
			for node in transformationNode:
				if TemplateManager.TAG_POSITION in node:
					position = node.get(TemplateManager.TAG_POSITION)
					statePane = Pane(*position)
				elif TemplateManager.TAG_TRANSLATION in node:
					translation = node.get(TemplateManager.TAG_TRANSLATION)
					statePane.translateBy(translation)
				elif TemplateManager.TAG_SCALING in node:
					scalingNode = node.get(TemplateManager.TAG_SCALING)
					pivot = scalingNode.get(TemplateManager.TAG_PIVOT)
					ratio = scalingNode.get(TemplateManager.TAG_RATIO)
					statePane.scale(pivot, ratio)

			strokes=list((stroke.generateCopyToApplyNewPane(componentInfo.getInfoPane(), statePane) for stroke in strokes))

		return strokes

	def parseStrokeByAnchor(self, strokeNode, anchromTemplateName):
		referenceName=strokeNode.get(TemplateManager.TAG_REFRENCE_NAME)
		component=self.get(referenceName)

		transformationNode=strokeNode.get(TemplateManager.TAG_TRANSFORMATION)
		if transformationNode != None:
			strokes=list(component.getStrokeList())

			componentInfo = ComponentInfo(strokes)
			statePane = componentInfo.getInfoPane().clone()
			for node in transformationNode:
				if TemplateManager.TAG_POSITION in node:
					position = node.get(TemplateManager.TAG_POSITION)
					statePane = Pane(*position)
				elif TemplateManager.TAG_TRANSLATION in node:
					translation = node.get(TemplateManager.TAG_TRANSLATION)
					statePane.translateBy(translation)
				elif TemplateManager.TAG_SCALING in node:
					scalingNode = node.get(TemplateManager.TAG_SCALING)
					pivot = scalingNode.get(TemplateManager.TAG_PIVOT)
					ratio = scalingNode.get(TemplateManager.TAG_RATIO)
					statePane.scale(pivot, ratio)

			component=component.generateCopyToApplyNewPane(statePane)

		return component

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

