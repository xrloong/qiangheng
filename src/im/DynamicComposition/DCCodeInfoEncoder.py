from .DCCodeInfo import DCCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder
from ..base.CodeInfo import CodeInfo
from .Calligraphy import Pane
from .Calligraphy import StrokeGroup

import sys
import copy

class DCCodeInfoEncoder(CodeInfoEncoder):
	WIDTH=256
	HEIGHT=256
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

	@staticmethod
	def computeNewStrokeGroup(codeInfo, helper, xStart, xEnd, yStart, yEnd):

		region=helper.getBlock(xStart, xEnd, yStart, yEnd)
		pane=Pane(region)

		newStrokeGroup=copy.deepcopy(codeInfo.getStrokeGroup())
		newStrokeGroup.transform(pane)
		return newStrokeGroup

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

		nCount=len(codeInfoList)
		helper=DCGridHelper(1, 1)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 0, 0, 0, 0))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		return copy.deepcopy(firstCodeInfo)

	def encodeAsLoop(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[-1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 0, 2, 0, 2))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(secondCodeInfo, helper, 1, 1, 1, 1))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)

		codeInfo.setExtraPane(copy.deepcopy(firstCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI)), DCCodeInfo.PANE_NAME_QI)
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(1, nCount)

		newStrokeGroupList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(tmpCodeInfo, helper, 0, 0, index, index))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)

		lastCodeInfo=codeInfoList[-1]
		codeInfo.setExtraPane(copy.deepcopy(lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI)), DCCodeInfo.PANE_NAME_QI)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(nCount, 1)

		newStrokeGroupList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(tmpCodeInfo, helper, index, index, 0, 0))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

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

	def encodeAsQi(self, codeInfoList):
		return self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_QI])

	def encodeAsLiao(self, codeInfoList):
		codeInfo=self.encodeByEmbed(codeInfoList, [DCCodeInfo.PANE_NAME_LIAO])

		lastCodeInfo=codeInfoList[-1]
		codeInfo.setExtraPane(copy.deepcopy(lastCodeInfo.getExtraPane(DCCodeInfo.PANE_NAME_QI)), DCCodeInfo.PANE_NAME_QI)
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

class DCGridHelper:
	WIDTH=256
	HEIGHT=256

	def __init__(self, xCount, yCount):
		self.xCoordinate=[ int(DCGridHelper.WIDTH*i*1./xCount) for i in range(xCount+1)]
		self.yCoordinate=[ int(DCGridHelper.HEIGHT*i*1./yCount) for i in range(yCount+1)]

	def getBlock(self, xStart, xEnd, yStart, yEnd):
		left=self.xCoordinate[xStart]
		top=self.yCoordinate[yStart]
		right=self.xCoordinate[xEnd+1]
		bottom=self.yCoordinate[yEnd+1]
		return [left, top, right, bottom]

