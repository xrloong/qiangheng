import abc

from model.base.IMInfo import IMInfo
from model.base.CodeInfo import CodeInfo
from model.base.CodeInfoEncoder import CodeInfoEncoder

from xie.graphics.shape import Pane
from xie.graphics.stroke import StrokeGroup
from xie.graphics.stroke import StrokeGroupInfo
from xie.graphics.factory import ShapeFactory

class DynamicCompositionInfo(IMInfo):
	"動態組字"

	IMName="動態組字"
	def __init__(self):
		self.keyMaps=[
			['0', '0',],
			['1', '1',],
			['2', '2',],
			['3', '3',],
			['4', '4',],
			['5', '5',],
			['6', '6',],
			['7', '7',],
			['8', '8',],
			['9', '9',],
			]
		self.nameDict={
				'cn':'動態組字',
				'tw':'動態組字',
				'hk':'動態組字',
				'en':'DynamicComposition',
				}
		self.iconfile="qhdc.svg"
		self.maxkeylength=4

class DCStrokeGroup:
	shapeFactory = ShapeFactory()

	def __init__(self, strokeGroup):
		self.strokeGroup=strokeGroup
		self.extraPaneDB={DCCodeInfo.PANE_NAME_DEFAULT : strokeGroup.getStatePane()}

	def getCount(self):
		return self.strokeGroup.getCount()

	def getStrokeGroup(self):
		return self.strokeGroup

	def generateStrokeGroup(self, pane):
		shapeFactory=DCStrokeGroup.shapeFactory
		return shapeFactory.generateStrokeGroupByStrokeGroupPane(self.strokeGroup, pane)

	def setExtraPaneDB(self, extranPaneDB):
		self.extraPaneDB=extranPaneDB
		self.extraPaneDB[DCCodeInfo.PANE_NAME_DEFAULT]=self.strokeGroup.getStatePane()

	def setExtraPane(self, paneName, extraPane):
		self.extraPaneDB[paneName]=extraPane

	def getExtraPane(self, paneName):
		return self.extraPaneDB.get(paneName, None)

	@staticmethod
	def generateDefaultStrokeGroup(dcStrokeGroupPanePairList):
		shapeFactory=DCStrokeGroup.shapeFactory
		strokeGroupPanePair=[(dcStrokeGroup.getStrokeGroup(), pane) for dcStrokeGroup, pane in dcStrokeGroupPanePairList]
		strokeGroup=shapeFactory.generateStrokeGroupByStrokeGroupPanePairList(strokeGroupPanePair)
		dcStrokeGroup=DCStrokeGroup(strokeGroup)
		return dcStrokeGroup

	@staticmethod
	def generateStrokeGroupByStrokeList(strokeList):
		shapeFactory=DCStrokeGroup.shapeFactory
		strokeGroup = shapeFactory.generateStrokeGroupByStrokeList(strokeList)
		return DCStrokeGroup(strokeGroup)

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

	def __init__(self, strokeGroupDB):
		super().__init__()

		self.strokeGroupDB=strokeGroupDB

	@staticmethod
	def generateDefaultCodeInfo(strokeGroupPanePair):
		strokeGroup=DCStrokeGroup.generateDefaultStrokeGroup(strokeGroupPanePair)
		strokeGroupDB={DCCodeInfo.STROKE_GROUP_NAME_DEFAULT : strokeGroup}

		codeInfo=DCCodeInfo(strokeGroupDB)
		return codeInfo

	def toCode(self):
		strokeGroup=self.getStrokeGroup()
		return strokeGroup

	def setExtraPane(self, strokeGroupName, paneName, extraPane):
		strokeGroup=self.getStrokeGroup(strokeGroupName)

		if strokeGroup==None:
			strokeGroup=self.getStrokeGroup()

		strokeGroup.setExtraPane(paneName, extraPane)

	def getExtraPane(self, strokeGroupName, paneName):
		strokeGroup=self.getStrokeGroup(strokeGroupName)

		if strokeGroup==None:
			strokeGroup=self.getStrokeGroup()

		return strokeGroup.getExtraPane(paneName)

	def getStrokeGroup(self, strokeGroupName=STROKE_GROUP_NAME_DEFAULT):
		strokeGroup=self.strokeGroupDB.get(strokeGroupName)
		if strokeGroupName!=DCCodeInfo.STROKE_GROUP_NAME_DEFAULT and strokeGroup==None:
			strokeGroup=self.getStrokeGroup(DCCodeInfo.STROKE_GROUP_NAME_DEFAULT)
		return strokeGroup

	def getStrokeCount(self):
		return self.getStrokeGroup().getCount()

class DCCodeInfoEncoder(CodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, strokeGroupPanePair):
		return DCCodeInfo.generateDefaultCodeInfo(strokeGroupPanePair)

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getStrokeCount()>0, codeInfoList))
		return isAllWithCode

	@classmethod
	def extendStrokeGroupNameList(cls, strokeGroupNameList, codeInfoList):
		lenNameList=len(strokeGroupNameList)
		lenCodeInfoList=len(codeInfoList)
		extendingList=[]
		if lenCodeInfoList>lenNameList:
			diff=lenCodeInfoList-lenNameList
			extendingList=[DCCodeInfo.STROKE_GROUP_NAME_DEFAULT for i in range(diff)]
		return strokeGroupNameList+extendingList

	@classmethod
	def splitLengthToList(cls, length, weightList):
		totalWeight=sum(weightList)
		unitLength=length*1./totalWeight

		pointList=[]
		newStrokeGroupList=[]
		base=0
		for weight in weightList:
			pointList.append(int(base))
			base=base+unitLength*weight
		pointList.append(int(base))
		return pointList

	@classmethod
	def encodeByEmbed(cls, codeInfoList, strokeGroupNameList, paneNameList):
		if len(codeInfoList)<2:
			return cls.encodeAsInvalidate(codeInfoList)

		containerCodeInfo=codeInfoList[0]

		newStrokeGroupList=[]
		for [strokeGroupName, paneName, codeInfo] in zip(strokeGroupNameList, paneNameList, codeInfoList):
			extraPane=containerCodeInfo.getExtraPane(strokeGroupName, paneName)
			assert extraPane!=None, "extraPane 不應為 None 。%s: %s"%(paneName, str(containerCodeInfo))

			strokeGroup=codeInfo.getStrokeGroup(strokeGroupName).generateStrokeGroup(extraPane)
			newStrokeGroupList.append(strokeGroup)

		paneList=[]
		for [strokeGroupName, paneName] in zip(strokeGroupNameList, paneNameList):
			extraPane=containerCodeInfo.getExtraPane(strokeGroupName, paneName)
			assert extraPane!=None, "extraPane 不應為 None 。%s: %s"%(paneName, str(containerCodeInfo))
			paneList.append(extraPane)

		strokeGroupList=[]
		for [strokeGroupName, codeInfo] in zip(strokeGroupNameList, codeInfoList):
			strokeGroup=codeInfo.getStrokeGroup(strokeGroupName)
			strokeGroupList.append(strokeGroup)

		strokeGroupPanePair=zip(strokeGroupList, paneList)
		codeInfo=cls.generateDefaultCodeInfo(strokeGroupPanePair)
		return codeInfo


	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		print("不合法的運算：龜", file=sys.stderr)
		codeInfo=cls.encodeAsInvalidate(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """
		print("不合法的運算：龍", file=sys.stderr)
		codeInfo=cls.encodeAsInvalidate(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsSparrow(cls, codeInfoList):
		"""運算 "雀" """
		print("不合法的運算：雀", file=sys.stderr)
		codeInfo=cls.encodeAsInvalidate(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsEqual(cls, codeInfoList):
		"""運算 "爲" """
		firstCodeInfo=codeInfoList[0]
		return firstCodeInfo


	@classmethod
	def encodeAsLoop(cls, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		codeInfo=cls.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_LOOP, DCCodeInfo.STROKE_GROUP_NAME_LOOP],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_LOOP])
		# 颱=(起 風台), 是=(回 [風外]䖝)
		if firstCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI, firstCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI))
		return codeInfo

	@classmethod
	def encodeAsSilkworm(cls, codeInfoList):
		def genPaneList(weightList):
			pane=Pane.BBOX
			pointList=cls.splitLengthToList(pane.getHeight(), weightList)
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

		strokeGroupNameList=cls.extendStrokeGroupNameList(['蚕'], codeInfoList)

		strokeGroupList=[]
		for [strokeGroupName, codeInfo] in zip(strokeGroupNameList, codeInfoList):
			strokeGroup=codeInfo.getStrokeGroup(strokeGroupName)
			strokeGroupList.append(strokeGroup)

		strokeGroupPanePair=zip(strokeGroupList, paneList)
		codeInfo=cls.generateDefaultCodeInfo(strokeGroupPanePair)

		lastCodeInfo=codeInfoList[-1]
		# 題=(起 是頁), 是=(志 日[是下])
		if lastCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI, lastCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI))

		return codeInfo

	@classmethod
	def encodeAsGoose(cls, codeInfoList):
		def genPaneList(weightList):
			pane=Pane.BBOX
			pointList=cls.splitLengthToList(pane.getWidth(), weightList)
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

		strokeGroupNameList=cls.extendStrokeGroupNameList(['鴻'], codeInfoList)

		strokeGroupList=[]
		for [strokeGroupName, codeInfo] in zip(strokeGroupNameList, codeInfoList):
			strokeGroup=codeInfo.getStrokeGroup(strokeGroupName)
			strokeGroupList.append(strokeGroup)

		strokeGroupPanePair=zip(strokeGroupList, paneList)
		codeInfo=cls.generateDefaultCodeInfo(strokeGroupPanePair)
		return codeInfo

	@classmethod
	def encodeAsQi(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.STROKE_GROUP_NAME_QI],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_QI])

	@classmethod
	def encodeAsLiao(cls, codeInfoList):
		codeInfo=cls.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_LIAO, DCCodeInfo.STROKE_GROUP_NAME_LIAO],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_LIAO])

		lastCodeInfo=codeInfoList[-1]
		# 屗=(起 尾寸), 尾=(志 尸毛)
		if lastCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI, lastCodeInfo.getExtraPane(DCCodeInfo.STROKE_GROUP_NAME_QI, DCCodeInfo.PANE_NAME_QI))
		return codeInfo

	@classmethod
	def encodeAsZai(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_ZAI, DCCodeInfo.STROKE_GROUP_NAME_ZAI],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_ZAI])

	@classmethod
	def encodeAsDou(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_DOU, DCCodeInfo.STROKE_GROUP_NAME_DOU],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_DOU])


	@classmethod
	def encodeAsMu(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_MU, DCCodeInfo.STROKE_GROUP_NAME_MU, DCCodeInfo.STROKE_GROUP_NAME_MU],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_MU_1, DCCodeInfo.PANE_NAME_MU_2])

	@classmethod
	def encodeAsZuo(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_ZUO, DCCodeInfo.STROKE_GROUP_NAME_ZUO, DCCodeInfo.STROKE_GROUP_NAME_ZUO],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_ZUO_1, DCCodeInfo.PANE_NAME_ZUO_2])

	@classmethod
	def encodeAsYou(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_YOU, DCCodeInfo.STROKE_GROUP_NAME_YOU, DCCodeInfo.STROKE_GROUP_NAME_YOU],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_YOU_1, DCCodeInfo.PANE_NAME_YOU_2])

	@classmethod
	def encodeAsLiang(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_LIANG, DCCodeInfo.STROKE_GROUP_NAME_LIANG, DCCodeInfo.STROKE_GROUP_NAME_LIANG],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_LIANG_1, DCCodeInfo.PANE_NAME_LIANG_2])

	@classmethod
	def encodeAsJia(cls, codeInfoList):
		return cls.encodeByEmbed(codeInfoList,
			[DCCodeInfo.STROKE_GROUP_NAME_JIA, DCCodeInfo.STROKE_GROUP_NAME_JIA, DCCodeInfo.STROKE_GROUP_NAME_JIA, ],
			[DCCodeInfo.PANE_NAME_DEFAULT, DCCodeInfo.PANE_NAME_JIA_1, DCCodeInfo.PANE_NAME_JIA_2])

class DCRadixParser():
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

		strokeGroupDB={}

		strokeGroupNodeList=elementCodeInfo.get(DCRadixParser.ATTRIB_CODE_EXPRESSION)
		for strokeGroupNode in strokeGroupNodeList:
			[strokeGroupName, strokeGroup]=self.parseStrokeGroup(strokeGroupNode)

			extraPaneDB=self.parseExtraScopeDB(strokeGroupNode)
			strokeGroup.setExtraPaneDB(extraPaneDB)

			if strokeGroupName==None:
				strokeGroupName=DCCodeInfo.STROKE_GROUP_NAME_DEFAULT
			strokeGroupDB[strokeGroupName]=strokeGroup

		codeInfo=DCCodeInfo(strokeGroupDB)
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

	def parseStrokeGroup(self, strokeGroupNode):
		strokeGroupName=strokeGroupNode.get(DCRadixParser.TAG_NAME)

		t=strokeGroupNode.get(DCRadixParser.TAG_STROKE_GROUP)
		strokeList=self.parseStrokeList(t)

		strokeGroup=DCStrokeGroup.generateStrokeGroupByStrokeList(strokeList)
		return [strokeGroupName, strokeGroup]

	def parseStrokeList(self, strokeGroupNode):
		strokeList=[]
		strokeNodeList=strokeGroupNode.get(DCRadixParser.TAG_STROKE)
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

		return shapeFactory.generateStroke(name, startPoint, parameterList)

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
		assert isinstance(template, StrokeGroup)
		self.anchors[name]=template

	def get(self, name):
		return self.anchors.get(name)

class CompositionTemplateManager(AbsTemplateManager):
	def __init__(self, templateManagers):
		super().__init__()
		self.templateManagers=templateManagers

	"""
	def put(self, name, template):
		assert isinstance(template, StrokeGroup)
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
		assert isinstance(template, StrokeGroup)
		self.templates[name]=template

	def get(self, name):
		return self.templates.get(name)

	def getStroke(self, name, index):
		strokeGroup=self.templates.get(name)
		return strokeGroup.getStrokeList()[index]

	def getStrokes(self, name, start, end):
		strokeGroup=self.templates.get(name)
		return strokeGroup.getStrokeList()[start, end+1]

	def load(self):
		template_file="gen/qhdata/dc/radix/template.yaml"
		self.parseTemplateFromYAML(template_file)

	def parseTemplateFromYAML(self, filename):
		import yaml
		rootNode=yaml.load(open(filename), Loader=yaml.SafeLoader)
		self.parseTemplateSet(rootNode)

	def parseTemplateSet(self, rootNode):
		templateSetNode=rootNode.get(TemplateManager.TAG_TEMPLATE_SET)
		for templateNode in templateSetNode:
			templateName=templateNode.get(TemplateManager.TAG_NAME)
			strokeGroupNode=templateNode.get(TemplateManager.TAG_STROKE_GROUP)
			strokeGroup=self.parseStrokeGroup(strokeGroupNode)
			self.put(templateName, strokeGroup)

	def parseStrokeGroup(self, strokeGroupNode):
		strokes=[]
		anchorTemplateManager = AnchorTemplateManager()
		compositionTemplateManager = CompositionTemplateManager((anchorTemplateManager, self,))
		for strokeNode in strokeGroupNode.get(TemplateManager.TAG_STROKE):
			method=strokeNode.get(TemplateManager.TAG_METHOD, TemplateManager.TAG_METHOD__DEFINITION)
			if method==TemplateManager.TAG_METHOD__REFERENCE:
				tempStrokes=self.parseStrokeByReference(strokeNode, compositionTemplateManager)
				strokes.extend(tempStrokes)
			elif method==TemplateManager.TAG_METHOD__ANCHOR:
				anchorName=strokeNode.get(TemplateManager.TAG_NAME)
				strokeGroup=self.parseStrokeByAnchor(strokeNode, anchorTemplateManager)
				anchorTemplateManager.put(anchorName, strokeGroup)
			elif method==TemplateManager.TAG_METHOD__DEFINITION:
				stroke=self.parseStroke(strokeNode)
				strokes.append(stroke)
			else:
				assert False
		strokeGroup=self.shapeFactory.generateStrokeGroupByStrokeList(strokes)
		return strokeGroup

	def parseStroke(self, strokeNode):
		strokeType=strokeNode.get(TemplateManager.TAG_TYPE)
		startPoint=strokeNode.get(TemplateManager.TAG_START_POINT)
		params=strokeNode.get(TemplateManager.TAG_PARAMETER)
		stroke=self.shapeFactory.generateStroke(strokeType, startPoint, params)
		return stroke

	def parseStrokeByReference(self, strokeNode, templateManager):
		strokeType=strokeNode.get(TemplateManager.TAG_TYPE)
		templateName=strokeNode.get(TemplateManager.TAG_REFRENCE_NAME)
		orders=strokeNode.get(TemplateManager.TAG_ORDER)

		strokeGroup=templateManager.get(templateName)
		strokes=list((strokeGroup.getStroke(index) for index in orders))

		transformationNode=strokeNode.get(TemplateManager.TAG_TRANSFORMATION)
		if transformationNode != None:
			strokeGroupInfo = StrokeGroupInfo(strokes)
			statePane = strokeGroupInfo.getInfoPane().clone()
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

			strokes=list((stroke.generateCopyToApplyNewPane(strokeGroupInfo.getInfoPane(), statePane) for stroke in strokes))

		return strokes

	def parseStrokeByAnchor(self, strokeNode, anchromTemplateName):
		referenceName=strokeNode.get(TemplateManager.TAG_REFRENCE_NAME)
		strokeGroup=self.get(referenceName)

		transformationNode=strokeNode.get(TemplateManager.TAG_TRANSFORMATION)
		if transformationNode != None:
			strokes=list(strokeGroup.getStrokeList())

			strokeGroupInfo = StrokeGroupInfo(strokes)
			statePane = strokeGroupInfo.getInfoPane().clone()
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

			strokes=list((stroke.generateCopyToApplyNewPane(strokeGroupInfo.getInfoPane(), statePane) for stroke in strokes))
			strokeGroup=strokeGroup.generateCopyToApplyNewPane(statePane)

		return strokeGroup

IMInfo = DynamicCompositionInfo
CodeInfoEncoder = DCCodeInfoEncoder
RadixParser = DCRadixParser

