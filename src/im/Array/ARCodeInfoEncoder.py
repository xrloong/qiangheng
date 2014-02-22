from .ARCodeInfo import ARCodeInfo
from ..base.CodeInfoEncoder import CodeInfoEncoder

import sys

class ARCodeInfoEncoder(CodeInfoEncoder):
	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, codeList):
		return ARCodeInfo.generateDefaultCodeInfo(codeList)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getMainCodeList(), codeInfoList))
		return isAllWithCode


	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """

		arCodeList=list(map(lambda c: c.getMainCodeList(), codeInfoList))
		tmpArCodeList=arCodeList
		arCode=ARCodeInfoEncoder.computeArrayCodeByCodeList(tmpArCodeList)
		codeInfo=self.generateDefaultCodeInfo([arCode])

		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo


	def encodeAsTong(self, codeInfoList):
		"""運算 "同" """
		newCodeInfoList=self.getMergedCodeInfoListAsForGe(codeInfoList)
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo

	def encodeAsHan(self, codeInfoList):
		"""運算 "函" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsZhe(self, codeInfoList):
		"""運算 "這" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		codeInfo=self.encodeAsLoong([secondCodeInfo, firstCodeInfo])
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		"""運算 "載" """
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


	def encodeAsLuan(self, codeInfoList):
		"""運算 "䜌" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		codeInfo=self.encodeAsLoong([firstCodeInfo, secondCodeInfo, secondCodeInfo])
		return codeInfo


	@staticmethod
	def computeArrayCodeByCodeList(arCodeList):
		cat=sum(arCodeList, [])
		arCode=cat[:3]+cat[-1:] if len(cat)>4 else cat
		return arCode

	def getCodeInfoExceptLast(self, codeInfo):
		mainCodeList=codeInfo.getMainCodeList()

		if len(mainCodeList)>1:
			tmpCodeInfo=self.generateDefaultCodeInfo([mainCodeList[:-1]])
		else:
			tmpCodeInfo=None

		return tmpCodeInfo

	def getCodeInfoExceptFirst(self, codeInfo):
		mainCodeList=codeInfo.getMainCodeList()

		if len(mainCodeList)>1:
			tmpCodeInfo=self.generateDefaultCodeInfo([mainCodeList[1:]])
		else:
			tmpCodeInfo=None

		return tmpCodeInfo

	def convertMergedCode(self, firstCodeInfo, secondCodeInfo, firstRadix, secondRadix, targetRadix):
		firstMainCodeList=firstCodeInfo.getMainCodeList()
		secondMainCodeList=secondCodeInfo.getMainCodeList()

		if firstMainCodeList[-1]==firstRadix and secondMainCodeList[0]==secondRadix:
			newFirstCodeInfo=self.getCodeInfoExceptLast(firstCodeInfo)
			targetCodeInfo=self.generateDefaultCodeInfo([[targetRadix]])
			newSecondCodeInfo=self.getCodeInfoExceptFirst(secondCodeInfo)
		else:
			newFirstCodeInfo=firstCodeInfo
			targetCodeInfo=None
			newSecondCodeInfo=secondCodeInfo
		return [newFirstCodeInfo, targetCodeInfo, newSecondCodeInfo]

	def getMergedCodeInfoList(self, codeInfoList, mergeCodeInfoList):
		firstCodeInfo=None
		secondCodeInfo=None

		newCodeInfoList=[]
		for xCodeInfo in codeInfoList:
			firstCodeInfo=secondCodeInfo
			secondCodeInfo=xCodeInfo

			if firstCodeInfo==None:
				continue

			for [firstRadix, secondRadix, targetRadix] in mergeCodeInfoList:
				[newFirstCodeInfo, targetCodeInfo, newSecondCodeInfo,]=self.convertMergedCode(firstCodeInfo, secondCodeInfo, firstRadix, secondRadix, targetRadix)
				if targetCodeInfo:
					if newFirstCodeInfo:
						newCodeInfoList.append(newFirstCodeInfo)
					newCodeInfoList.append(targetCodeInfo)
					secondCodeInfo=newSecondCodeInfo
					break;
			else:
				newCodeInfoList.append(firstCodeInfo)

		if secondCodeInfo!=None:
			newCodeInfoList.append(secondCodeInfo)

		return newCodeInfoList

	def getMergedCodeInfoListAsForGe(self, codeInfoList):
		# 如 咸、戎
		if len(codeInfoList)<=1:
			print("錯誤：", file=sys.stderr)
			return codeInfoList
		else:
			firstCodeInfo=codeInfoList[0]
			if firstCodeInfo.isInstallmentEncoded():
				frontMainCode=firstCodeInfo.getInstallmentCode(0)
				rearMainCode=firstCodeInfo.getInstallmentCode(1)

				frontCodeInfo=self.generateDefaultCodeInfo([frontMainCode])
				rearCodeInfo=self.generateDefaultCodeInfo([rearMainCode])
				return [frontCodeInfo]+codeInfoList[1:]+[rearCodeInfo]
			else:
				return codeInfoList

