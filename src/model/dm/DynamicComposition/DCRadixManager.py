from .DCCodeInfo import DCCodeInfo
from .DCCodeInfo import DCStrokeGroup
from .DCCodeInfoEncoder import DCCodeInfoEncoder
from model.base.RadixManager import RadixParser
from xie.graphics.shape import Pane
from xie.graphics.stroke import StrokeGroup
from xie.graphics.stroke import StrokeGroupInfo
from xie.graphics.factory import ShapeFactory

class DCRadixParser(RadixParser):
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

	def __init__(self, nameInputMethod, codeInfoEncoder):
		super().__init__(nameInputMethod, codeInfoEncoder)
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
				tempStrokes=self.templateManager.parseStrokeByReference(strokeNode)
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

class TemplateManager:
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

	TAG_REFRENCE_NAME='引用名稱'
	TAG_ORDER='順序'
	TAG_TRANSFORMATION='變換'

	TAG_POSITION='定位'
	TAG_TRANSLATION='平移'
	TAG_SCALING='縮放'

	TAG_PIVOT='樞軸點'
	TAG_RATIO='比例'

	def __init__(self, shapeFactory):
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
		rootNode=yaml.load(open(filename))
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
		for strokeNode in strokeGroupNode.get(TemplateManager.TAG_STROKE):
			method=strokeNode.get(TemplateManager.TAG_METHOD, TemplateManager.TAG_METHOD__DEFINITION)
			if method==TemplateManager.TAG_METHOD__REFERENCE:
				tempStrokes=self.parseStrokeByReference(strokeNode)
				strokes.extend(tempStrokes)
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

	def parseStrokeByReference(self, strokeNode):
		strokeType=strokeNode.get(TemplateManager.TAG_TYPE)
		templateName=strokeNode.get(TemplateManager.TAG_REFRENCE_NAME)
		orders=strokeNode.get(TemplateManager.TAG_ORDER)

		strokeGroup=self.get(templateName)
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

