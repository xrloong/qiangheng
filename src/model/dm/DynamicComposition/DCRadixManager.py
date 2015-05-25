from .DCCodeInfo import DCCodeInfo
from .DCCodeInfo import DCStrokeGroup
from .DCCodeInfoEncoder import DCCodeInfoEncoder
from model.base.RadixManager import RadixParser
from model.calligraphy import stroke
from model.calligraphy.Calligraphy import Pane
from model.calligraphy.Calligraphy import Stroke
from model.calligraphy.Calligraphy import StrokeGroupInfo

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
		bBox=t.get(DCRadixParser.TAG_BBOX)
		strokeList=self.parseStrokeList(t)

		strokeGroup=DCStrokeGroup.generateStrokeGroupByParameter(strokeList, bBox)
		return [strokeGroupName, strokeGroup]

	def parseStrokeList(self, strokeGroupNode):
		strokeList=[]
		strokeNodeList=strokeGroupNode.get(DCRadixParser.TAG_STROKE)
		for strokeNode in strokeNodeList:
			stroke=DCRadixParser.fromStrokeNode(strokeNode)
			strokeList.append(stroke)
		return strokeList

	@staticmethod
	def fromStrokeNode(strokeNode):
		name=strokeNode.get(DCRadixParser.TAG_TYPE)

		startPoint=strokeNode.get(DCRadixParser.TAG_START_POINT)

		parameterList = strokeNode.get(DCRadixParser.TAG_PARAMETER)
		bBox = strokeNode.get(DCRadixParser.TAG_BBOX)

		return Stroke.generateStroke(name, startPoint, parameterList, bBox)

	def parsePane(self, descriptionRegion):
		left=int(descriptionRegion[0:2], 16)
		top=int(descriptionRegion[2:4], 16)
		right=int(descriptionRegion[4:6], 16)
		bottom=int(descriptionRegion[6:8], 16)
		return Pane([left, top, right, bottom])

