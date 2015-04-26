from .BSCodeInfo import BSCodeInfo
from model.base.CodeInfoEncoder import CodeInfoEncoder

import sys

class BSCodeInfoEncoder(CodeInfoEncoder):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	@classmethod
	def generateDefaultCodeInfo(cls, codeList, supplementCode):
		return BSCodeInfo.generateDefaultCodeInfo(codeList, supplementCode)

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getBSCodeList(), codeInfoList))
		return isAllWithCode


	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """

		bslist=list(map(lambda c: c.getBSCodeList(), codeInfoList))
		bs_code_list=BSCodeInfoEncoder.computeBoshiamyCode(bslist)
		bs_spcode=codeInfoList[-1].getBSSupplement()

		codeInfo=cls.generateDefaultCodeInfo([bs_code_list], bs_spcode)
		return codeInfo

	@classmethod
	def encodeAsSparrow(cls, codeInfoList):
		"""運算 "雀" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsEqual(cls, codeInfoList):
		"""運算 "爲" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo


	@classmethod
	def encodeAsHan(cls, codeInfoList):
		"""運算 "函" """
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
	def encodeAsZhe(cls, codeInfoList):
		"""運算 "這" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		codeInfo=cls.encodeAsLoong([secondCodeInfo, firstCodeInfo])
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

				bs_spcode=firstCodeInfo.getBSSupplement()

				# 第一個的補碼不影響結果
				frontCodeInfo=cls.generateDefaultCodeInfo([frontMainCode], bs_spcode)
				rearCodeInfo=cls.generateDefaultCodeInfo([rearMainCode], bs_spcode)
				return [frontCodeInfo]+codeInfoList[1:]+[rearCodeInfo]
			else:
				return codeInfoList

	@staticmethod
	def computeBoshiamyCode(bsCodeList):
		bslist=list(sum(bsCodeList, []))
		bs_code_list=(bslist[:3]+bslist[-1:]) if len(bslist)>4 else bslist
		return bs_code_list

