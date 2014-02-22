from ..CodeInfo.ZMCodeInfo import ZMCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder
from gear.CodeInfo import CodeInfo
from gear import Operator

class ZMCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, rtlist):
		return ZMCodeInfo.generateDefaultCodeInfo(rtlist)

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=ZMCodeInfo.generateCodeInfo(propDict)
		codeInfo.multiplyCodeVarianceType(codeVariance)
		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=codeInfoList and all(map(lambda x: x.getRtList(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """

		rtlist=sum(map(lambda c: c.getRtList(), codeInfoList), [])

		rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
		codeInfo=self.generateDefaultCodeInfo([rtlist])
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo


	def encodeAsHan(self, codeInfoList):
		"""運算 "爲" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsGoose(self, codeInfoList):
		"""運算 "鴻" """

		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		newCodeInfoList=codeInfoList
		if firstCodeInfo.getRtList()[0]==ZMCodeInfo.RADIX_彳 and lastCodeInfo.getRtList()[0]==ZMCodeInfo.RADIX_亍:
			newCodeInfo=self.generateDefaultCodeInfo([[ZMCodeInfo.RADIX_行]])
			newCodeInfoList=[newCodeInfo]+codeInfoList[1:-1]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsTong(self, codeInfoList):
		"""運算 "同" """
		newCodeInfoList=self.getMergedCodeInfoListAsForGe(codeInfoList)
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsYou(self, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		newCodeInfoList=[secondCodeInfo, thirdCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		"""運算 "㒳" """

		rtlist=sum(map(lambda c: c.getRtList(), codeInfoList), [])

		rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
		codeInfo=self.generateDefaultCodeInfo([rtlist[:1]])
		return codeInfo

	def getMergedCodeInfoListAsForGe(self, codeInfoList):
		# 贏
		if len(codeInfoList)<=1:
			print("錯誤：", file=sys.stderr)
			return codeInfoList
		else:
			firstCodeInfo=codeInfoList[0]
			if firstCodeInfo.isInstallmentEncoded():
				frontMainCode=firstCodeInfo.getInstallmentCode(0)
				rearMainCode=firstCodeInfo.getInstallmentCode(1)

				# 第一個的補碼不影響結果
				frontCodeInfo=self.generateDefaultCodeInfo([frontMainCode])
				rearCodeInfo=self.generateDefaultCodeInfo([rearMainCode])
				return [frontCodeInfo]+codeInfoList[1:]+[rearCodeInfo]
			else:
				return codeInfoList

