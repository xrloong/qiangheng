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

	def generateDefaultStrokeGroup(self, strokeList):
		pane=Pane.DEFAULT_PANE
		strokeGroup=StrokeGroup(pane, strokeList)
		return self.generateDefaultCodeInfo(strokeGroup)

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
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(1, nCount)

		newStrokeGroupList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(tmpCodeInfo, helper, 0, 0, index, index))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
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

	def encodeAsQi(self, codeInfoList):
		if len(codeInfoList)<2:
			return self.encodeAsInvalidate(codeInfoList)

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 0, 1, 0, 1))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(secondCodeInfo, helper, 1, 1, 0, 0))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsLiao(self, codeInfoList):
		if len(codeInfoList)<2:
			return self.encodeAsInvalidate(codeInfoList)

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 0, 1, 0, 1))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(secondCodeInfo, helper, 1, 1, 1, 1))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 0, 1, 0, 1))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(secondCodeInfo, helper, 0, 0, 1, 1))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsDou(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 0, 1, 0, 1))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(secondCodeInfo, helper, 0, 0, 0, 0))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsMu(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 0, 2, 0, 2))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(secondCodeInfo, helper, 0, 0, 2, 2))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(thirdCodeInfo, helper, 2, 2, 2, 2))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsZuo(self, codeInfoList):
		# 以 "㘴" 來說 first: 口，second: 人，third: 土
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(thirdCodeInfo, helper, 0, 2, 0, 2))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 0, 0, 0, 0))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(secondCodeInfo, helper, 2, 2, 0, 0))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsYou(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(5, 2)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(thirdCodeInfo, helper, 0, 4, 0, 1))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 1, 1, 0, 0))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(secondCodeInfo, helper, 3, 3, 0, 0))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(5, 2)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(thirdCodeInfo, helper, 0, 4, 0, 1))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 1, 1, 1, 1))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(secondCodeInfo, helper, 3, 3, 1, 1))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

	def encodeAsJia(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newStrokeGroupList=[]
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(thirdCodeInfo, helper, 0, 2, 0, 2))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(firstCodeInfo, helper, 0, 0, 1, 1))
		newStrokeGroupList.append(DCCodeInfoEncoder.computeNewStrokeGroup(secondCodeInfo, helper, 2, 2, 1, 1))
		newStrokeGroup=self.mergeStrokeGroupList(newStrokeGroupList)

		codeInfo=self.generateDefaultCodeInfo(newStrokeGroup)
		return codeInfo

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

