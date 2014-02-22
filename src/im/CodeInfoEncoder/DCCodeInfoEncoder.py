import sys
from ..CodeInfo.DCCodeInfo import DCCodeInfo
from ..CodeInfo.DCCodeInfo import StrokeAction
from gear.CodeInfoEncoder import CodeInfoEncoder
from gear import Operator
import copy

class DCCodeInfoEncoder(CodeInfoEncoder):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	WIDTH=256
	HEIGHT=256
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, actionList):
		codeInfo=DCCodeInfo(actionList)
		return codeInfo

	def generateCodeInfo(self, propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfoEncoder.computeSupportingFromProperty(propDict)
		actionList=[]

		description=propDict.get('資訊表示式', '')
		if len(description)>0 and description!='XXXX':
			descriptionList=description.split(DCCodeInfoEncoder.RADIX_SEPERATOR)
			actionList=[StrokeAction(d) for d in descriptionList]

		codeInfo=DCCodeInfo(actionList, isSupportCharacterCode, isSupportRadixCode)
		return codeInfo

	def interprettCharacterCode(self, codeInfo):
		descriptionList=[x.getCode() for x in codeInfo.getActionList()]
		return DCCodeInfoEncoder.RADIX_SEPERATOR.join(descriptionList)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: len(x.getActionList())>0, codeInfoList))
		return isAllWithCode

	def computeNewActionList(codeInfo, helper, xStart, xEnd, yStart, yEnd):
		newActionList=[]

		[left, top, right, bottom]=helper.getBlock(xStart, xEnd, yStart, yEnd)
		width=right-left
		height=bottom-top

		xScale=width*1./DCGridHelper.WIDTH
		yScale=height*1./DCGridHelper.HEIGHT

		for tmpAction in codeInfo.getActionList():
			action=copy.deepcopy(tmpAction)
			action.scale(xScale, yScale)
			action.translate(left, top)

			newActionList.append(action)
		return newActionList

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

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 0, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsLoop(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[-1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 2, 0, 2))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 1, 1, 1, 1))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(1, nCount)

		newActionList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			newActionList.extend(DCCodeInfoEncoder.computeNewActionList(tmpCodeInfo, helper, 0, 0, index, index))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(nCount, 1)

		newActionList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			newActionList.extend(DCCodeInfoEncoder.computeNewActionList(tmpCodeInfo, helper, index, index, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsQi(self, codeInfoList):
		if len(codeInfoList)<2:
			return self.encodeAsInvalidate(codeInfoList)

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 1, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 1, 1, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsLiao(self, codeInfoList):
		if len(codeInfoList)<2:
			return self.encodeAsInvalidate(codeInfoList)

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 1, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 1, 1, 1, 1))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 1, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 0, 0, 1, 1))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsDou(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 1, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 0, 0, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsMu(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 2, 0, 2))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 0, 0, 2, 2))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(thirdCodeInfo, helper, 2, 2, 2, 2))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsZuo(self, codeInfoList):
		# 以 "㘴" 來說 first: 口，second: 人，third: 土
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(thirdCodeInfo, helper, 0, 2, 0, 2))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 0, 0, 0))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 2, 2, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsYou(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(5, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(thirdCodeInfo, helper, 0, 4, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 1, 1, 0, 0))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 3, 3, 0, 0))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(5, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(thirdCodeInfo, helper, 0, 4, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 1, 1, 1, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 3, 3, 1, 1))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsJia(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(thirdCodeInfo, helper, 0, 2, 0, 2))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 0, 1, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 2, 2, 1, 1))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
		return codeInfo

	def encodeAsYin(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[-1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 2, 0, 2))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 0, 2, 0, 2))

		codeInfo=self.generateDefaultCodeInfo(newActionList)
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

