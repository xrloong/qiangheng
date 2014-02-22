import sys

from ..CodeInfo.DYCodeInfo import DYCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class DYCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=DYCodeInfo(propDict, codeVariance)
		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getMainCode(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfo, codeInfoList):
		"""運算 "龜" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsLoong(self, codeInfo, codeInfoList):
		"""運算 "龍" """

		dyCode=DYCodeInfoEncoder.computeDaYiCode(codeInfoList)
		codeInfo.setCodeList([dyCode])

	def encodeAsEast(self, codeInfo, codeInfoList):
		"""運算 "東" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsEqual(self, codeInfo, codeInfoList):
		"""運算 "爲" """
		self.encodeAsLoong(codeInfo, codeInfoList)


	def encodeAsLoop(self, codeInfo, codeInfoList):
		"""運算 "回" """
		self.encodeAsZai(codeInfo, codeInfoList)

	def encodeAsTong(self, codeInfo, codeInfoList):
		"""運算 "同" """
		dyCode=DYCodeInfoEncoder.computeDaYiCodeForGe(codeInfoList)
		codeInfo.setCodeList([dyCode])

	def encodeAsZai(self, codeInfo, codeInfoList):
		"""運算 "載" """
		dyCode=DYCodeInfoEncoder.computeDaYiCodeForGe(codeInfoList)
		codeInfo.setCodeList([dyCode])

	@staticmethod
	def computeDaYiCode(codeInfoList):
		dyCodeList=list(map(lambda c: c.getMainCode(), codeInfoList))
		return DYCodeInfoEncoder.computeDaYiCodeByCodeList(dyCodeList)

	def computeDaYiCodeByCodeList(dyCodeList):
		cat="".join(dyCodeList)
		dyCode=cat[:3]+cat[-1] if len(cat)>4 else cat
		return dyCode

	@staticmethod
	def computeDaYiCodeForGe(codeInfoList):
		# 如 咸、戎
		if len(codeInfoList)<=1:
			print("錯誤：", file=sys.stderr)
			dyCode=DYCodeInfoEncoder.computeDaYiCode(codeInfoList)
		else:
			firstCodeInfo=codeInfoList[0]
			if firstCodeInfo.isInstallmentEncoded():
				frontMainCode=firstCodeInfo.getInstallmentCode(0)
				rearMainCode=firstCodeInfo.getInstallmentCode(1)

				restMainCode=DYCodeInfoEncoder.computeDaYiCode(codeInfoList[1:])

				dyCodeList=[frontMainCode, restMainCode, rearMainCode]
				dyCode=DYCodeInfoEncoder.computeDaYiCodeByCodeList(dyCodeList)
			else:
				dyCode=DYCodeInfoEncoder.computeDaYiCode(codeInfoList)
		return dyCode

