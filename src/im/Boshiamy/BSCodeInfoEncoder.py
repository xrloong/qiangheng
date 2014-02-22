from .BSCodeInfo import BSCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder

import sys
import copy

class BSCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, codeList, supplementCode):
		return BSCodeInfo.generateDefaultCodeInfo(codeList, supplementCode)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getBSCodeList(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """

		bslist=list(map(lambda c: c.getBSCodeList(), codeInfoList))
		bs_code_list=BSCodeInfoEncoder.computeBoshiamyCode(bslist)
		bs_spcode=codeInfoList[-1].getBSSupplement()

		codeInfo=self.generateDefaultCodeInfo([bs_code_list], bs_spcode)
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		"""運算 "蚕" """
		bsCodeList=list(map(lambda c: c.getBSCodeList(), codeInfoList))
		tmpBsCodeList=BSCodeInfoEncoder.mergeRadixAsSilkworm(bsCodeList)

		bs_code_list=BSCodeInfoEncoder.computeBoshiamyCode(tmpBsCodeList)
		bs_spcode=codeInfoList[-1].getBSSupplement()

		codeInfo=self.generateDefaultCodeInfo([bs_code_list], bs_spcode)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		"""運算 "鴻" """
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		if firstCodeInfo.getMainCodeList()[0]==BSCodeInfo.RADIX_丿 and lastCodeInfo.getMainCodeList()[0]==BSCodeInfo.RADIX_乚:
			newCodeInfo=self.generateDefaultCodeInfo([[BSCodeInfo.RADIX_儿]], "l")
			codeInfo=self.encodeAsGoose([newCodeInfo]+codeInfoList[1:-1])
			return codeInfo
		if firstCodeInfo.getMainCodeList()[0]==BSCodeInfo.RADIX_丨 and lastCodeInfo.getMainCodeList()[0]==BSCodeInfo.RADIX_丨:
			newCodeInfo=self.generateDefaultCodeInfo([[BSCodeInfo.RADIX_丨丨]], "i")
			codeInfo=self.encodeAsGoose([newCodeInfo]+codeInfoList[1:-1])
			return codeInfo
		if firstCodeInfo.getMainCodeList()[0]==BSCodeInfo.RADIX_丨 and lastCodeInfo.getMainCodeList()[0]==BSCodeInfo.RADIX_丿:
			newCodeInfo=self.generateDefaultCodeInfo([[BSCodeInfo.RADIX_丨丿]], "i")
			codeInfo=self.encodeAsGoose([newCodeInfo]+codeInfoList[1:-1])
			return codeInfo
		if firstCodeInfo.getMainCodeList()[0]==BSCodeInfo.RADIX_丿 and lastCodeInfo.getMainCodeList()[0]==BSCodeInfo.RADIX_丨:
			newCodeInfo=self.generateDefaultCodeInfo([[BSCodeInfo.RADIX_丿丨]], "i")
			codeInfo=self.encodeAsGoose([newCodeInfo]+codeInfoList[1:-1])
			return codeInfo

		bsCodeList=list(map(lambda c: c.getBSCodeList(), codeInfoList))
		tmpBsCodeList=BSCodeInfoEncoder.mergeRadixAsGoose(bsCodeList)

		bs_code_list=BSCodeInfoEncoder.computeBoshiamyCode(tmpBsCodeList)
		bs_spcode=codeInfoList[-1].getBSSupplement()

		codeInfo=self.generateDefaultCodeInfo([bs_code_list], bs_spcode)
		return codeInfo

	def encodeAsHan(self, codeInfoList):
		"""運算 "函" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo

	def encodeAsTong(self, codeInfoList):
		"""運算 "同" """
		newCodeInfoList=self.getMergedCodeInfoListAsForGe(codeInfoList)
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsZhe(self, codeInfoList):
		"""運算 "這" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		codeInfo=self.encodeAsLoong([secondCodeInfo, firstCodeInfo])
		return codeInfo

	def encodeAsYou(self, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		newCodeInfoList=[secondCodeInfo, thirdCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
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

				bs_spcode=firstCodeInfo.getBSSupplement()

				# 第一個的補碼不影響結果
				frontCodeInfo=self.generateDefaultCodeInfo([frontMainCode], bs_spcode)
				rearCodeInfo=self.generateDefaultCodeInfo([rearMainCode], bs_spcode)
				return [frontCodeInfo]+codeInfoList[1:]+[rearCodeInfo]
			else:
				return codeInfoList

	@staticmethod
	def computeBoshiamyCode(bsCodeList):
		bslist=list(sum(bsCodeList, []))
		bs_code_list=(bslist[:3]+bslist[-1:]) if len(bslist)>4 else bslist
		return bs_code_list

	@staticmethod
	def mergeRadixAsSilkworm(bsCodeList):
		tmpBsCodeList=copy.copy(bsCodeList)

		numBsCode=len(tmpBsCodeList)
		for i in range(numBsCode-1):
			bsCodePrev=tmpBsCodeList[i]
			bsCodeNext=tmpBsCodeList[i+1]
			if len(bsCodePrev)>0 and len(bsCodeNext)>0:
				if bsCodePrev[-1]==BSCodeInfo.RADIX_山 and bsCodeNext[0]==BSCodeInfo.RADIX_一:
					tmpBsCodeList[i]=bsCodePrev[:-1]+[BSCodeInfo.RADIX_山一]
					tmpBsCodeList[i+1]=bsCodeNext[1:]

		# 合併字根後，有些字根列可能為空，如：戓
		tmpBsCodeList=filter(lambda x: len(x)>0, tmpBsCodeList)

		return tmpBsCodeList

	@staticmethod
	def mergeRadixAsGoose(bsCodeList):
		tmpBsCodeList=copy.copy(bsCodeList)

		numBsCode=len(tmpBsCodeList)
		for i in range(numBsCode-1):
			bsCodePrev=tmpBsCodeList[i]
			bsCodeNext=tmpBsCodeList[i+1]
			if len(bsCodePrev)>0 and len(bsCodeNext)>0:
				if bsCodePrev[0]==BSCodeInfo.RADIX_丿丿 and bsCodeNext[0]==BSCodeInfo.RADIX_山一:
					tmpBsCodeList[i]=[BSCodeInfo.RADIX_丿丿_山一]+bsCodePrev[1:]
					tmpBsCodeList[i+1]=bsCodeNext[1:]

		# 合併字根後，有些字根列可能為空，如：戓
		tmpBsCodeList=filter(lambda x: len(x)>0, tmpBsCodeList)

		return tmpBsCodeList

