from .DCCodeInfo import DCCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder
from ..base.CodeInfo import CodeInfo
from .Calligraphy import Pane
from .Calligraphy import StrokeGroup

import sys
import copy

class DCCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, strokeGroupDB):
		return DCCodeInfo.generateDefaultCodeInfo(strokeGroupDB)

	def generateStrokeGroupDB(self, strokeGroup):
		return strokeGroupDB

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getStrokeCount()>0, codeInfoList))
		return isAllWithCode

	def mergeStrokeGroupListToDB(self, strokeGroupList):
		resultStrokeList=[]
		for strokeGroup in strokeGroupList:
			resultStrokeList.extend(strokeGroup.getStrokeList())
		pane=Pane.DEFAULT_PANE
		strokeGroup=StrokeGroup(pane, resultStrokeList)
		strokeGroupDB={DCCodeInfo.STROKE_GROUP_NAME_DEFAULT : strokeGroup}
		return strokeGroupDB

	def extendStrokeGroupNameList(self, strokeGroupNameList, codeInfoList):
		lenNameList=len(strokeGroupNameList)
		lenCodeInfoList=len(codeInfoList)
		extendingList=[]
		if lenCodeInfoList>lenNameList:
			diff=lenCodeInfoList-lenNameList
			extendingList=[DCCodeInfo.STROKE_GROUP_NAME_DEFAULT for i in range(diff)]
		return strokeGroupNameList+extendingList

	def splitLengthToList(self, length, weightList):
		totalWeight=sum(weightList)
		unitLength=length*1./totalWeight

		pointList=[]
		newStrokeGroupList=[]
		base=0
		for weight in weightList:
			pointList.append(int(base))
			base=base+unitLength*weight
		pointList.append(base)
		return pointList

	def encodeByEmbed(self, codeInfoList, strokeGroupNameList, paneNameList):
		if len(codeInfoList)<2:
			return self.encodeAsInvalidate(codeInfoList)

		containerCodeInfo=codeInfoList[0]

		strokeGroupNameList=self.extendStrokeGroupNameList(strokeGroupNameList, codeInfoList)

		newStrokeGroupList=[]
		paneNameList=[DCCodeInfo.PANE_NAME_DEFAULT]+paneNameList
		for [paneName, strokeGroupName, codeInfo] in zip(paneNameList, strokeGroupNameList, codeInfoList):
			extraPane=containerCodeInfo.getExtraPane(paneName)
			assert extraPane!=None, "extraPane 不應為 None 。%s: %s"%(paneName, str(containerCodeInfo))

			strokeGroup=codeInfo.getCopyOfStrokeGroup(strokeGroupName)
			strokeGroup.transform(extraPane)
			newStrokeGroupList.append(strokeGroup)

		strokeGroupDB=self.mergeStrokeGroupListToDB(newStrokeGroupList)
		codeInfo=self.generateDefaultCodeInfo(strokeGroupDB)
		return codeInfo

	def encodeAsTurtle(self, codeInfoList):
		print("不合法的運算：龜", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		print("不合法的運算：龍", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		print("不合法的運算：東", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		return copy.deepcopy(firstCodeInfo)

	def encodeAsLoop(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		codeInfo=self.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_LOOP], [DCCodeInfo.PANE_NAME_LOOP])
		if firstCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, copy.deepcopy(firstCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI)))
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		weightList=list(map(lambda x: x.getStrokeCount()+1, codeInfoList))
		pointList=self.splitLengthToList(Pane.HEIGHT, weightList)

		strokeGroupNameList=self.extendStrokeGroupNameList(['蚕'], codeInfoList)

		newStrokeGroupList=[]
		for [pointStart, pointEnd, strokeGroupName, codeInfo] in zip(pointList[:-1], pointList[1:], strokeGroupNameList, codeInfoList):
			pane=Pane([0, pointStart, Pane.X_MAX, pointEnd])

			newStrokeGroup=codeInfo.getCopyOfStrokeGroup(strokeGroupName)
			newStrokeGroup.transform(pane)
			newStrokeGroupList.append(newStrokeGroup)
		strokeGroupDB=self.mergeStrokeGroupListToDB(newStrokeGroupList)
		codeInfo=self.generateDefaultCodeInfo(strokeGroupDB)

		lastCodeInfo=codeInfoList[-1]
		if lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, copy.deepcopy(lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI)))

		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		weightList=list(map(lambda x: x.getStrokeCount(), codeInfoList))
		pointList=self.splitLengthToList(Pane.WIDTH, weightList)

		strokeGroupNameList=self.extendStrokeGroupNameList(['鴻'], codeInfoList)

		newStrokeGroupList=[]
		for [pointStart, pointEnd, strokeGroupName, codeInfo] in zip(pointList[:-1], pointList[1:], strokeGroupNameList, codeInfoList):
			pane=Pane([pointStart, 0, pointEnd, Pane.Y_MAX])

			newStrokeGroup=codeInfo.getCopyOfStrokeGroup(strokeGroupName)
			newStrokeGroup.transform(pane)
			newStrokeGroupList.append(newStrokeGroup)

		strokeGroupDB=self.mergeStrokeGroupListToDB(newStrokeGroupList)
		codeInfo=self.generateDefaultCodeInfo(strokeGroupDB)
		return codeInfo

	def encodeAsQi(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_QI], [DCCodeInfo.PANE_NAME_QI])

	def encodeAsLiao(self, codeInfoList):
		codeInfo=self.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_LIAO], [DCCodeInfo.PANE_NAME_LIAO])

		lastCodeInfo=codeInfoList[-1]
		if lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, copy.deepcopy(lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI)))
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_ZAI], [DCCodeInfo.PANE_NAME_ZAI])

	def encodeAsDou(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_DOU], [DCCodeInfo.PANE_NAME_DOU])


	def encodeAsMu(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_MU], [DCCodeInfo.PANE_NAME_MU_1, DCCodeInfo.PANE_NAME_MU_2])

	def encodeAsZuo(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_ZUO], [DCCodeInfo.PANE_NAME_ZUO_1, DCCodeInfo.PANE_NAME_ZUO_2])

	def encodeAsYou(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_YOU], [DCCodeInfo.PANE_NAME_YOU_1, DCCodeInfo.PANE_NAME_YOU_2])

	def encodeAsLiang(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_LIANG], [DCCodeInfo.PANE_NAME_LIANG_1, DCCodeInfo.PANE_NAME_LIANG_2])

	def encodeAsJia(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.STROKE_GROUP_NAME_JIA], [DCCodeInfo.PANE_NAME_JIA_1, DCCodeInfo.PANE_NAME_JIA_2])

