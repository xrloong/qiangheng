import sys

from ..CodeInfo.ARCodeInfo import ARCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class ARCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=ARCodeInfo(propDict, codeVariance)
		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getMainCode(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfo, codeInfoList):
		"""運算 "龜" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsLoong(self, codeInfo, codeInfoList):
		"""運算 "龍" """

		arCode=ARCodeInfoEncoder.computeArrayCode(codeInfoList)
		codeInfo.setCodeList([arCode])

	def encodeAsEast(self, codeInfo, codeInfoList):
		"""運算 "東" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsEqual(self, codeInfo, codeInfoList):
		"""運算 "爲" """
		self.encodeAsLoong(codeInfo, codeInfoList)


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

	def encodeAsZai(self, codeInfo, codeInfoList):
		"""運算 "載" """
		arCode=ARCodeInfoEncoder.computeArrayCodeForGe(codeInfoList)
		codeInfo.setCodeList([arCode])

	@staticmethod
	def computeArrayCode(codeInfoList):
		arCodeList=list(map(lambda c: c.getMainCode(), codeInfoList))
		return ARCodeInfoEncoder.computeArrayCodeByCodeList(arCodeList)

	def computeArrayCodeByCodeList(arCodeList):
		cat="".join(arCodeList)
		arCode=cat[:3]+cat[-1] if len(cat)>4 else cat
		return arCode

	@staticmethod
	def computeArrayCodeForGe(codeInfoList):
		# 如 咸、戎
		if len(codeInfoList)<=1:
			print("錯誤：", file=sys.stderr)
			arCode=ARCodeInfoEncoder.computeArrayCode(codeInfoList)
		else:
			firstCodeInfo=codeInfoList[0]
			if firstCodeInfo.isInstallmentEncoded():
				frontMainCode=firstCodeInfo.getInstallmentCode(0)
				rearMainCode=firstCodeInfo.getInstallmentCode(1)

				restMainCode=ARCodeInfoEncoder.computeArrayCode(codeInfoList[1:])

				arCodeList=[frontMainCode, restMainCode, rearMainCode]
				arCode=ARCodeInfoEncoder.computeArrayCodeByCodeList(arCodeList)
			else:
				arCode=ARCodeInfoEncoder.computeArrayCode(codeInfoList)
		return arCode

