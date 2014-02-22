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

			elif Operator.OperatorEqual.equals(operator):
				DCCodeInfoEncoder.encodeAsEqual(codeInfo, operator, codeInfoList)
			elif Operator.OperatorLoop.equals(operator):
				DCCodeInfoEncoder.encodeAsLoop(codeInfo, operator, codeInfoList)
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

			elif Operator.OperatorMu.equals(operator):
				DCCodeInfoEncoder.encodeAsMu(codeInfo, operator, codeInfoList)
			elif Operator.OperatorZuo.equals(operator):
				DCCodeInfoEncoder.encodeAsZuo(codeInfo, operator, codeInfoList)
			elif Operator.OperatorYou.equals(operator):
				DCCodeInfoEncoder.encodeAsYou(codeInfo, operator, codeInfoList)
			elif Operator.OperatorLiang.equals(operator):
				DCCodeInfoEncoder.encodeAsLiang(codeInfo, operator, codeInfoList)
			elif Operator.OperatorJia.equals(operator):
				DCCodeInfoEncoder.encodeAsJia(codeInfo, operator, codeInfoList)

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
		firstCodeInfo=codeInfoList[0]

		nCount=len(codeInfoList)
		helper=DCGridHelper(1, 1)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 0, 0, 0))

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsLoop(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[-1]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 2, 0, 2))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 1, 1, 1, 1))

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsSilkworm(codeInfo, operator, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(1, nCount)

		newActionList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			newActionList.extend(DCCodeInfoEncoder.computeNewActionList(tmpCodeInfo, helper, 0, 0, index, index))

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsGoose(codeInfo, operator, codeInfoList):
		nCount=len(codeInfoList)
		helper=DCGridHelper(nCount, 1)

		newActionList=[]
		for (index, tmpCodeInfo) in enumerate(codeInfoList):
			newActionList.extend(DCCodeInfoEncoder.computeNewActionList(tmpCodeInfo, helper, index, index, 0, 0))

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

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 2, 0, 2))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 0, 0, 2, 2))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(thirdCodeInfo, helper, 2, 2, 2, 2))

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsZuo(codeInfo, operator, codeInfoList):
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

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsYou(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(5, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(thirdCodeInfo, helper, 0, 4, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 1, 1, 0, 0))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 3, 3, 0, 0))

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsLiang(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(5, 2)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(thirdCodeInfo, helper, 0, 4, 0, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 1, 1, 1, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 3, 3, 1, 1))

		codeInfo.setActionList(newActionList)

	@staticmethod
	def encodeAsJia(codeInfo, operator, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		nCount=len(codeInfoList)
		helper=DCGridHelper(3, 3)

		newActionList=[]
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(thirdCodeInfo, helper, 0, 2, 0, 2))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(firstCodeInfo, helper, 0, 0, 1, 1))
		newActionList.extend(DCCodeInfoEncoder.computeNewActionList(secondCodeInfo, helper, 2, 2, 1, 1))

		codeInfo.setActionList(newActionList)

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

