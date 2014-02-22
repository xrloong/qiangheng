from .DCCodeInfo import DCCodeInfo
from .DCCodeInfoEncoder import DCCodeInfoEncoder
from ..base.RadixManager import RadixParser
from calligraphy import Calligraphy
from calligraphy.Calligraphy import Pane
from calligraphy.Calligraphy import Stroke
from calligraphy.Calligraphy import StrokeGroup
import re

class DCRadixParser(RadixParser):
	TAG_STROKE_GROUP='筆劃組'
	TAG_GEOMETRY='幾何'
	TAG_SCOPE='範圍'
	TAG_STROKE='筆劃'
	TAG_NAME='名稱'
	TAG_EXTRA_SCOPE='補充範圍'

	TAG_CODE_INFORMATION='編碼資訊'
	ATTRIB_STROKE_EXPRESSION='筆劃資訊'

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

		strokeGroupNodeList=elementCodeInfo.findall(DCRadixParser.TAG_STROKE_GROUP)
		for strokeGroupNode in strokeGroupNodeList:
			[strokeGroupName, strokeGroup]=self.parseStrokeGroup(strokeGroupNode)
			if strokeGroupName==None:
				strokeGroupName=DCCodeInfo.STROKE_GROUP_NAME_DEFAULT
			strokeGroupDB[strokeGroupName]=strokeGroup

		codeInfo=self.getEncoder().generateDefaultCodeInfo(strokeGroupDB)

		extraPaneDB=self.parseExtraScopeDB(elementCodeInfo)
		codeInfo.setExtraPaneDB(extraPaneDB)
		return codeInfo

	def parseRadixInfo(self, rootNode):
		characterSetNode=rootNode.find(DCRadixParser.TAG_CHARACTER_SET)
		characterNodeList=characterSetNode.findall(DCRadixParser.TAG_CHARACTER)
		for characterNode in characterNodeList:
			charName=characterNode.get(DCRadixParser.TAG_NAME)
			radixDescription=self.parseRadixDescription(characterNode)

			self.radixDescriptionManager.addDescription(charName, radixDescription)

	def parseExtraScopeDB(self, elementCodeInfo):
		extraPaneDB={}

		extraScopeNodeList=elementCodeInfo.findall(DCRadixParser.TAG_EXTRA_SCOPE)
		for extraScopeNode in extraScopeNodeList:
			paneName=extraScopeNode.attrib.get(DCRadixParser.TAG_NAME)
			pane=self.parseExtraScope(extraScopeNode)

			extraPaneDB[paneName]=pane

		return extraPaneDB

	def parseExtraScope(self, extraScopeNode):
		geometryNode=extraScopeNode.find(DCRadixParser.TAG_GEOMETRY)
		pane=self.parseGeometry(geometryNode)
		return pane

	def parseGeometry(self, geometryNode):
		descriptionRegion=geometryNode.get(DCRadixParser.TAG_SCOPE)
		pane=self.parsePane(descriptionRegion)
		return pane

	def parseStrokeGroup(self, strokeGroupNode):
		strokeGroupName=strokeGroupNode.get(DCRadixParser.TAG_NAME)

		geometryNode=strokeGroupNode.find(DCRadixParser.TAG_GEOMETRY)
		pane=self.parseGeometry(geometryNode)

		strokeGroup=self.parseStroke(pane, strokeGroupNode)
		return [strokeGroupName, strokeGroup]

	def parseStroke(self, pane, strokeGroupNode):
		strokeList=[]
		strokeNodeList=strokeGroupNode.findall(DCRadixParser.TAG_STROKE)
		for strokeNode in strokeNodeList:
			descriptionRegion=strokeNode.get(DCRadixParser.TAG_SCOPE)
			countourPane=self.parsePane(descriptionRegion)

			strokeExpression=strokeNode.attrib.get(DCRadixParser.ATTRIB_STROKE_EXPRESSION, '')
			stroke=DCRadixParser.fromStrokeExpression(pane, strokeExpression)

			stroke.transform(countourPane)

			strokeList.append(stroke)
		strokeGroup=StrokeGroup(pane, strokeList)
		return strokeGroup

	@staticmethod
	def fromStrokeExpression(contourPane, strokeExpression):
		l=strokeExpression.split(';')
		name=l[0]
		scopeDesc=l[1]

		left=int(scopeDesc[0:2], 16)
		top=int(scopeDesc[2:4], 16)
		right=int(scopeDesc[4:6], 16)
		bottom=int(scopeDesc[6:8], 16)
		scope=(left, top, right, bottom)

		strokeDesc=l[2]
		parameterExpression = strokeDesc[1:-1]
		parameterExpressionList = parameterExpression.split(',')

		clsStrokeInfo = Calligraphy.StrokeInfoMap.get(name, None)
		assert clsStrokeInfo!=None

		parameterList = clsStrokeInfo.parseExpression(parameterExpressionList)
		strokeInfo = clsStrokeInfo(name, scope, parameterList)

		return Stroke(strokeInfo)

	def parsePane(self, descriptionRegion):
		left=int(descriptionRegion[0:2], 16)
		top=int(descriptionRegion[2:4], 16)
		right=int(descriptionRegion[4:6], 16)
		bottom=int(descriptionRegion[6:8], 16)
		return Pane([left, top, right, bottom])

