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

	def generateDefaultCodeInfo(self, strokeGroup):
		return DCCodeInfo.generateDefaultCodeInfo(strokeGroup)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: len(x.getStrokeList())>0, codeInfoList))
		return isAllWithCode

	def mergeStrokeGroupList(self, strokeGroupList):
		resultStrokeList=[]
		for strokeGroup in strokeGroupList:
			resultStrokeList.extend(strokeGroup.getStrokeList())
		pane=Pane.DEFAULT_PANE
		return StrokeGroup(pane, resultStrokeList)

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

	def encodeByEmbed(self, codeInfoList, paneNameList):
		if len(codeInfoList)<2:
			return self.encodeAsInvalidate(codeInfoList)

		containerCodeInfo=codeInfoList[0]

		newStrokeGroupList=[]
		paneNameList=[DCCodeInfo.PANE_NAME_DEFAULT]+paneNameList
		for [paneName, codeInfo] in zip(paneNameList, codeInfoList):
			extraPane=containerCodeInfo.getExtraPane(paneName)
			assert extraPane!=None, "extraPane 不應為 None 。%s: %s"%(paneName, str(containerCodeInfo))

			strokeGroup=copy.deepcopy(codeInfo.getStrokeGroup())
			strokeGroup.transform(extraPane)
			newStrokeGroupList.append(strokeGroup)

		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
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

		newStrokeGroupList=[copy.deepcopy(firstCodeInfo.getStrokeGroup())]
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		return copy.deepcopy(firstCodeInfo)

	def encodeAsLoop(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		codeInfo=self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_LOOP])
		if firstCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, copy.deepcopy(firstCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI)))
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		weightList=list(map(lambda x: x.getStrokeCount()+1, codeInfoList))
		pointList=self.splitLengthToList(Pane.HEIGHT, weightList)

		newStrokeGroupList=[]
		for [pointStart, pointEnd, codeInfo] in zip(pointList[:-1], pointList[1:], codeInfoList):
			pane=Pane([0, pointStart, Pane.X_MAX, pointEnd])

			newStrokeGroup=copy.deepcopy(codeInfo.getStrokeGroup())
			newStrokeGroup.transform(pane)
			newStrokeGroupList.append(newStrokeGroup)
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)

		lastCodeInfo=codeInfoList[-1]
		if lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, copy.deepcopy(lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI)))

		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		weightList=list(map(lambda x: x.getStrokeCount(), codeInfoList))
		pointList=self.splitLengthToList(Pane.WIDTH, weightList)

		newStrokeGroupList=[]
		for [pointStart, pointEnd, codeInfo] in zip(pointList[:-1], pointList[1:], codeInfoList):
			pane=Pane([pointStart, 0, pointEnd, Pane.Y_MAX])

			newStrokeGroup=copy.deepcopy(codeInfo.getStrokeGroup())
			newStrokeGroup.transform(pane)
			newStrokeGroupList.append(newStrokeGroup)

		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsQi(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_QI])

	def encodeAsLiao(self, codeInfoList):
		codeInfo=self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_LIAO])

		lastCodeInfo=codeInfoList[-1]
		if lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI):
			codeInfo.setExtraPane(DCCodeInfo.PANE_NAME_QI, copy.deepcopy(lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI)))
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_ZAI])

	def encodeAsDou(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_DOU])


	def encodeAsMu(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_MU_1, DCCodeInfo.PANE_NAME_MU_2])

	def encodeAsZuo(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_ZUO_1, DCCodeInfo.PANE_NAME_ZUO_2])

	def encodeAsYou(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_YOU_1, DCCodeInfo.PANE_NAME_YOU_2])

	def encodeAsLiang(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_LIANG_1, DCCodeInfo.PANE_NAME_LIANG_2])

	def encodeAsJia(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_JIA_1, DCCodeInfo.PANE_NAME_JIA_2])

