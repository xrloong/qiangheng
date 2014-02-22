from .DCCodeInfo import DCCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder
from ..base.CodeInfo import CodeInfo

import sys
import copy

class DCCodeInfoEncoder(CodeInfoEncoder):
	WIDTH=256
	HEIGHT=256
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, strokeList, region=[0, 0, 0xFF, 0xFF]):
		return DCCodeInfo.generateDefaultCodeInfo(strokeList, region)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: len(x.getStrokeList())>0, codeInfoList))
		return isAllWithCode

	def computeNewStrokeList(codeInfo, helper, xStart, xEnd, yStart, yEnd):
		newStrokeList=[]

		[left, top, right, bottom]=helper.getBlock(xStart, xEnd, yStart, yEnd)
		width=right-left
		height=bottom-top

		xScale=width*1./DCGridHelper.WIDTH
		yScale=height*1./DCGridHelper.HEIGHT

		for tmpStroke in codeInfo.getStrokeList():
			stroke=copy.deepcopy(tmpStroke)
			stroke.scale(xScale, yScale)
			stroke.translate(left, top)

			newStrokeList.append(stroke)
		return newStrokeList

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

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 0, 0, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsLoop(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[-1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 0, 2, 0, 2))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(secondCodeInfo, helper, 1, 1, 1, 1))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(1, nCount)

		newStrokeList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(tmpCodeInfo, helper, 0, 0, index, index))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(nCount, 1)

		newStrokeList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(tmpCodeInfo, helper, index, index, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsQi(self, codeInfoList):
		if len(codeInfoList)<2:
			return self.encodeAsInvalidate(codeInfoList)

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 0, 1, 0, 1))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(secondCodeInfo, helper, 1, 1, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsLiao(self, codeInfoList):
		if len(codeInfoList)<2:
			return self.encodeAsInvalidate(codeInfoList)

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 0, 1, 0, 1))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(secondCodeInfo, helper, 1, 1, 1, 1))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 0, 1, 0, 1))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(secondCodeInfo, helper, 0, 0, 1, 1))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsDou(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 0, 1, 0, 1))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(secondCodeInfo, helper, 0, 0, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsMu(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 0, 2, 0, 2))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(secondCodeInfo, helper, 0, 0, 2, 2))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(thirdCodeInfo, helper, 2, 2, 2, 2))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsZuo(self, codeInfoList):
		# 以 "㘴" 來說 first: 口，second: 人，third: 土
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(thirdCodeInfo, helper, 0, 2, 0, 2))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 0, 0, 0, 0))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(secondCodeInfo, helper, 2, 2, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsYou(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(5, 2)

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(thirdCodeInfo, helper, 0, 4, 0, 1))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 1, 1, 0, 0))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(secondCodeInfo, helper, 3, 3, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(5, 2)

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(thirdCodeInfo, helper, 0, 4, 0, 1))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 1, 1, 1, 1))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(secondCodeInfo, helper, 3, 3, 1, 1))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
		return codeInfo

	def encodeAsJia(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newStrokeList=[]
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(thirdCodeInfo, helper, 0, 2, 0, 2))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(firstCodeInfo, helper, 0, 0, 1, 1))
		newStrokeList.extend(DCCodeInfoEncoder.computeNewStrokeList(secondCodeInfo, helper, 2, 2, 1, 1))

		codeInfo=self.generateDefaultCodeInfo(newStrokeList)
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

