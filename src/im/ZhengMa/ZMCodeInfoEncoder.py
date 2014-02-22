from .ZMCodeInfo import ZMCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder
from ..base.CodeInfo import CodeInfo

class ZMCodeInfoEncoder(CodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, rtlist):
		return ZMCodeInfo.generateDefaultCodeInfo(rtlist)

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		isAllWithCode=codeInfoList and all(map(lambda x: x.getRtList(), codeInfoList))
		return isAllWithCode

	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """

		rtlist=sum(map(lambda c: c.getRtList(), codeInfoList), [])

		rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
		codeInfo=cls.generateDefaultCodeInfo([rtlist])
		return codeInfo

	@classmethod
	def encodeAsEast(cls, codeInfoList):
		"""運算 "東" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsEqual(cls, codeInfoList):
		"""運算 "爲" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo


	@classmethod
	def encodeAsHan(cls, codeInfoList):
		"""運算 "爲" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		codeInfo=cls.encodeAsLoong(newCodeInfoList)
		return codeInfo


	@classmethod
	def encodeAsTong(cls, codeInfoList):
		"""運算 "同" """
		newCodeInfoList=cls.getMergedCodeInfoListAsForGe(codeInfoList)
		codeInfo=cls.encodeAsLoong(newCodeInfoList)
		return codeInfo


	@classmethod
	def encodeAsYou(cls, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		newCodeInfoList=[secondCodeInfo, thirdCodeInfo, firstCodeInfo]
		codeInfo=cls.encodeAsLoong(newCodeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLiang(cls, codeInfoList):
		"""運算 "㒳" """

		rtlist=sum(map(lambda c: c.getRtList(), codeInfoList), [])

		rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
		codeInfo=cls.generateDefaultCodeInfo([rtlist[:1]])
		return codeInfo

	@classmethod
	def getMergedCodeInfoListAsForGe(cls, codeInfoList):
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
				frontCodeInfo=cls.generateDefaultCodeInfo([frontMainCode])
				rearCodeInfo=cls.generateDefaultCodeInfo([rearMainCode])
				return [frontCodeInfo]+codeInfoList[1:]+[rearCodeInfo]
			else:
				return codeInfoList

