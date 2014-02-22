import sys
from ..CodeInfo.DCCodeInfo import DCCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder
from gear import Operator
import copy

class DCCodeInfoEncoder(CodeInfoEncoder):
	WIDTH=256
	HEIGHT=256
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=DCCodeInfo(propDict, codeVariance)
		return codeInfo

	def setByComps(self, codeInfo, operator, codeInfoList):
		isAllWithCode=all(map(lambda x: len(x.getActionList())>0, codeInfoList))
		if isAllWithCode:
			if Operator.OperatorTurtle.equals(operator):
				print("不合法的運算：%s"%operator.getName(), file=sys.stderr)
				FCCodeInfoEncoder.encodeAsInvalidate(codeInfo, operator, codeInfoList)
			elif Operator.OperatorLoong.equals(operator):
				print("不合法的運算：%s"%operator.getName(), file=sys.stderr)
				FCCodeInfoEncoder.encodeAsInvalidate(codeInfo, operator, codeInfoList)
			elif Operator.OperatorEast.equals(operator):
				print("不合法的運算：%s"%operator.getName(), file=sys.stderr)
				FCCodeInfoEncoder.encodeAsInvalidate(codeInfo, operator, codeInfoList)

#			elif Operator.OperatorEqual.equals(operator):
#				FCCodeInfoEncoder.encodeAsEqual(codeInfo, operator, codeInfoList)
#			elif Operator.OperatorLoop.equals(operator):
#				FCCodeInfoEncoder.encodeAsLoop(codeInfo, operator, codeInfoList)
			elif Operator.OperatorSilkworm.equals(operator):
				DCCodeInfoEncoder.encodeAsSilkworm(codeInfo, operator, codeInfoList)
			elif Operator.OperatorGoose.equals(operator):
				DCCodeInfoEncoder.encodeAsGoose(codeInfo, operator, codeInfoList)

			elif Operator.OperatorQi.equals(operator):
				DCCodeInfoEncoder.encodeAsQi(codeInfo, operator, codeInfoList)
			elif Operator.OperatorLiao.equals(operator):
				DCCodeInfoEncoder.encodeAsLiao(codeInfo, operator, codeInfoList)
			elif Operator.OperatorZai.equals(operator):
				DCCodeInfoEncoder.encodeAsZai(codeInfo, operator, codeInfoList)
			elif Operator.OperatorDou.equals(operator):
				DCCodeInfoEncoder.encodeAsDou(codeInfo, operator, codeInfoList)

				"""
			elif Operator.OperatorMu.equals(operator):
				FCCodeInfoEncoder.encodeAsMu(codeInfo, operator, codeInfoList)
			elif Operator.OperatorZuo.equals(operator):
				FCCodeInfoEncoder.encodeAsZuo(codeInfo, operator, codeInfoList)
			elif Operator.OperatorYou.equals(operator):
				FCCodeInfoEncoder.encodeAsYou(codeInfo, operator, codeInfoList)
			elif Operator.OperatorLiang.equals(operator):
				FCCodeInfoEncoder.encodeAsLiang(codeInfo, operator, codeInfoList)
			elif Operator.OperatorJia.equals(operator):
				FCCodeInfoEncoder.encodeAsJia(codeInfo, operator, codeInfoList)
				"""

			else:
				DCCodeInfoEncoder.encodeAsConcatenate(codeInfo, operator, codeInfoList)

	@staticmethod
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

	@staticmethod
	def encodeAsConcatenate(codeInfo, operator, codeInfoList):
		actionList=[]
		for tmpCodeInfo in codeInfoList:
			actionList.extend(copy.deepcopy(tmpCodeInfo.getActionList()))
		codeInfo.setActionList(actionList)

	@staticmethod
	def encodeAsInvalidate(codeInfo, operator, codeInfoList):
		codeInfo.setActionList([])

	@staticmethod
	def encodeAsEqual(codeInfo, operator, codeInfoList):
		targetCodeInfo=codeInfoList[0]
		codeInfo.setCode(
			targetCodeInfo.getTopLeft(),
			targetCodeInfo.getTopRight(),
			targetCodeInfo.getBottomLeft(),
			targetCodeInfo.getBottomRight())

	@staticmethod
	def encodeAsEast(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]
		codeInfo.setCode(
			firstCodeInfo.getTopLeft(),
			firstCodeInfo.getTopRight(),
			lastCodeInfo.getBottomLeft(),
			lastCodeInfo.getBottomRight())

	@staticmethod
	def encodeAsLoop(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]
		grid=FCGrid()
		grid.setAsOut_In(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		codeInfo.setCode(top_left, top_right, bottom_left, bottom_right)

	@staticmethod
	def encodeAsSilkworm(codeInfo, operator, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(1, nCount)

		newActionList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			[left, top, right, bottom]=helper.getBlock(0, 0, index, index)
			width=right-left
			height=bottom-top

			xScale=width*1./DCGridHelper.WIDTH
			yScale=height*1./DCGridHelper.HEIGHT

			for tmpAction in tmpCodeInfo.getActionList():
				action=copy.deepcopy(tmpAction)
				action.scale(xScale, yScale)
				action.translate(left, top)

				newActionList.append(action)
		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsGoose(codeInfo, operator, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(nCount, 1)

		newActionList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			[left, top, right, bottom]=helper.getBlock(index, index, 0, 0)
			width=right-left
			height=bottom-top

			xScale=width*1./DCGridHelper.WIDTH
			yScale=height*1./DCGridHelper.HEIGHT

			for tmpAction in tmpCodeInfo.getActionList():
				action=copy.deepcopy(tmpAction)
				action.scale(xScale, yScale)
				action.translate(left, top)

				newActionList.append(action)
		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsQi(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 1, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 1, 1, 0, 0))

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsLiao(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 1, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 1, 1, 1, 1))

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsZai(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 1, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 0, 0, 1, 1))

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsDou(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(2, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 1, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 0, 0, 0, 0))

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsMu(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsTop_BottomLeft_BottomRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		codeInfo.setCode(top_left, top_right, bottom_left, bottom_right)

	@staticmethod
	def encodeAsZuo(codeInfo, operator, codeInfoList):
		# 以 "㘴" 來說 first: 口，second: 人，third: 土
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_TopLeft_TopRight(thirdCodeInfo, firstCodeInfo, secondCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		codeInfo.setCode(top_left, top_right, bottom_left, bottom_right)

	@staticmethod
	def encodeAsYou(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_InTopLeft_InTopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		codeInfo.setCode(top_left, top_right, bottom_left, bottom_right)

	@staticmethod
	def encodeAsLiang(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsTop_InBottomLeft_InBottomRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		codeInfo.setCode(top_left, top_right, bottom_left, bottom_right)

	@staticmethod
	def encodeAsJia(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_InTopLeft_InTopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		codeInfo.setCode(top_left, top_right, bottom_left, bottom_right)

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

