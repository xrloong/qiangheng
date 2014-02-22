import sys
import copy

from ..CodeInfo.ARCodeInfo import ARCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class ARCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=ARCodeInfo(propDict, codeVariance)
		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getMainCodeList(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfo, codeInfoList):
		"""運算 "龜" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsLoong(self, codeInfo, codeInfoList):
		"""運算 "龍" """

		arCode=ARCodeInfoEncoder.computeArrayCodeForGenerality(codeInfoList)
		codeInfo.setCodeList([arCode])

	def encodeAsEast(self, codeInfo, codeInfoList):
		"""運算 "東" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsEqual(self, codeInfo, codeInfoList):
		"""運算 "爲" """
		self.encodeAsLoong(codeInfo, codeInfoList)


	def encodeAsSilkworm(self, codeInfo, codeInfoList):
		"""運算 "蚕" """
		arCode=ARCodeInfoEncoder.computeArrayCodeForGenerality(codeInfoList, True)
		codeInfo.setCodeList([arCode])


	def encodeAsLoop(self, codeInfo, codeInfoList):
		"""運算 "回" """
		arCode=ARCodeInfoEncoder.computeArrayCodeForGe(codeInfoList)
		codeInfo.setCodeList([arCode])

	def encodeAsTong(self, codeInfo, codeInfoList):
		"""運算 "同" """
		arCode=ARCodeInfoEncoder.computeArrayCodeForGe(codeInfoList)
		codeInfo.setCodeList([arCode])

	def encodeAsHan(self, codeInfo, codeInfoList):
		"""運算 "函" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		arCode=ARCodeInfoEncoder.computeArrayCodeForGe(newCodeInfoList)
		codeInfo.setCodeList([arCode])


	def encodeAsQi(self, codeInfo, codeInfoList):
		"""運算 "起" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		firstMainCodeList=firstCodeInfo.getMainCodeList()
		if len(firstMainCodeList)==1 and (firstMainCodeList[0]==ARCodeInfo.RADIX_EXTEND_5_BOTTOM or firstMainCodeList[0]==ARCodeInfo.RADIX_EXTEND_6_BOTTOM or firstMainCodeList[0]==ARCodeInfo.RADIX_EXTEND_2_CENTER):
			arCode=ARCodeInfoEncoder.computeArrayCodeForGe([secondCodeInfo, firstCodeInfo])
		else:
			arCode=ARCodeInfoEncoder.computeArrayCodeForGe(codeInfoList)

		codeInfo.setCodeList([arCode])

	def encodeAsZai(self, codeInfo, codeInfoList):
		"""運算 "載" """
		arCode=ARCodeInfoEncoder.computeArrayCodeForGe(codeInfoList)
		codeInfo.setCodeList([arCode])

	def encodeAsYou(self, codeInfo, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		newCodeInfoList=[secondCodeInfo, thirdCodeInfo, firstCodeInfo]
		self.encodeAsLoong(codeInfo, newCodeInfoList)

	@staticmethod
	def computeArrayCodeForGenerality(codeInfoList, isWithMergeRadix=False):
		arCodeList=list(map(lambda c: c.getMainCodeList(), codeInfoList))
		return ARCodeInfoEncoder.computeArrayCodeByCodeList(arCodeList, isWithMergeRadix)

	@staticmethod
	def computeArrayCodeForGe(codeInfoList):
		# 如 咸、戎
		if len(codeInfoList)<=1:
			print("錯誤：", file=sys.stderr)
			arCode=ARCodeInfoEncoder.computeArrayCodeForGenerality(codeInfoList)
		else:
			firstCodeInfo=codeInfoList[0]
			if firstCodeInfo.isInstallmentEncoded():
				frontMainCode=firstCodeInfo.getInstallmentCode(0)
				rearMainCode=firstCodeInfo.getInstallmentCode(1)

				restMainCode=ARCodeInfoEncoder.computeArrayCodeForGenerality(codeInfoList[1:])

				arCodeList=[frontMainCode, restMainCode, rearMainCode]
				arCode=ARCodeInfoEncoder.computeArrayCodeByCodeList(arCodeList, True)
			else:
				arCode=ARCodeInfoEncoder.computeArrayCodeForGenerality(codeInfoList)
		return arCode

	@staticmethod
	def computeArrayCodeByCodeList(arCodeList, isWithMergeRadix=False):
		tmpArCodeList=copy.copy(arCodeList)

		if isWithMergeRadix:
			numArCode=len(tmpArCodeList)
			for i in range(numArCode-1):
				arCodePrev=tmpArCodeList[i]
				arCodeNext=tmpArCodeList[i+1]
				if len(arCodePrev)>0 and len(arCodeNext)>0 and arCodePrev[-1]==ARCodeInfo.RADIX_EXTEND_1_CENTER and arCodeNext[0]==ARCodeInfo.RADIX_EXTEND_0_CENTER:
					tmpArCodeList[i]=arCodePrev[:-1]+[ARCodeInfo.RADIX_EXTEND_1_UP]
					tmpArCodeList[i+1]=arCodeNext[1:]

			# 合併字根後，有些字根列可能為空，如：戓
			tmpArCodeList=filter(lambda x: len(x)>0, tmpArCodeList)

		cat=sum(tmpArCodeList, [])
		arCode=cat[:3]+cat[-1:] if len(cat)>4 else cat
		return arCode

