from .ARCodeInfo import ARCodeInfo
from model.base.CodeInfoEncoder import CodeInfoEncoder

import sys

class ARCodeInfoEncoder(CodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, codeList):
		return ARCodeInfo.generateDefaultCodeInfo(codeList)

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getMainCodeList(), codeInfoList))
		return isAllWithCode


	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """

		arCodeList=list(map(lambda c: c.getMainCodeList(), codeInfoList))
		tmpArCodeList=arCodeList
		arCode=ARCodeInfoEncoder.computeArrayCodeByCodeList(tmpArCodeList)
		codeInfo=cls.generateDefaultCodeInfo([arCode])

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
	def encodeAsTong(cls, codeInfoList):
		"""運算 "同" """
		newCodeInfoList=cls.getMergedCodeInfoListAsForGe(codeInfoList)
		codeInfo=cls.encodeAsLoong(newCodeInfoList)
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
	def encodeAsZhe(cls, codeInfoList):
		"""運算 "這" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		codeInfo=cls.encodeAsLoong([secondCodeInfo, firstCodeInfo])
		return codeInfo

	@classmethod
	def encodeAsZai(cls, codeInfoList):
		"""運算 "載" """
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
	def encodeAsLuan(cls, codeInfoList):
		"""運算 "䜌" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		codeInfo=cls.encodeAsLoong([firstCodeInfo, secondCodeInfo, secondCodeInfo])
		return codeInfo


	@classmethod
	def getCodeInfoExceptLast(cls, codeInfo):
		mainCodeList=codeInfo.getMainCodeList()

		if len(mainCodeList)>1:
			tmpCodeInfo=cls.generateDefaultCodeInfo([mainCodeList[:-1]])
		else:
			tmpCodeInfo=None

		return tmpCodeInfo

	@classmethod
	def getCodeInfoExceptFirst(cls, codeInfo):
		mainCodeList=codeInfo.getMainCodeList()

		if len(mainCodeList)>1:
			tmpCodeInfo=cls.generateDefaultCodeInfo([mainCodeList[1:]])
		else:
			tmpCodeInfo=None

		return tmpCodeInfo

	@classmethod
	def convertMergedCode(cls, firstCodeInfo, secondCodeInfo, firstRadix, secondRadix, targetRadix):
		firstMainCodeList=firstCodeInfo.getMainCodeList()
		secondMainCodeList=secondCodeInfo.getMainCodeList()

		if firstMainCodeList[-1]==firstRadix and secondMainCodeList[0]==secondRadix:
			newFirstCodeInfo=cls.getCodeInfoExceptLast(firstCodeInfo)
			targetCodeInfo=cls.generateDefaultCodeInfo([[targetRadix]])
			newSecondCodeInfo=cls.getCodeInfoExceptFirst(secondCodeInfo)
		else:
			newFirstCodeInfo=firstCodeInfo
			targetCodeInfo=None
			newSecondCodeInfo=secondCodeInfo
		return [newFirstCodeInfo, targetCodeInfo, newSecondCodeInfo]

	@classmethod
	def getMergedCodeInfoList(cls, codeInfoList, mergeCodeInfoList):
		firstCodeInfo=None
		secondCodeInfo=None

		newCodeInfoList=[]
		for xCodeInfo in codeInfoList:
			firstCodeInfo=secondCodeInfo
			secondCodeInfo=xCodeInfo

			if firstCodeInfo==None:
				continue

			for [firstRadix, secondRadix, targetRadix] in mergeCodeInfoList:
				[newFirstCodeInfo, targetCodeInfo, newSecondCodeInfo,]=cls.convertMergedCode(firstCodeInfo, secondCodeInfo, firstRadix, secondRadix, targetRadix)
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

	@classmethod
	def getMergedCodeInfoListAsForGe(cls, codeInfoList):
		# 如 咸、戎
		if len(codeInfoList)<=1:
			print("錯誤：", file=sys.stderr)
			return codeInfoList
		else:
			firstCodeInfo=codeInfoList[0]
			if firstCodeInfo.isInstallmentEncoded():
				frontMainCode=firstCodeInfo.getInstallmentCode(0)
				rearMainCode=firstCodeInfo.getInstallmentCode(1)

				frontCodeInfo=cls.generateDefaultCodeInfo([frontMainCode])
				rearCodeInfo=cls.generateDefaultCodeInfo([rearMainCode])
				return [frontCodeInfo]+codeInfoList[1:]+[rearCodeInfo]
			else:
				return codeInfoList

	@staticmethod
	def computeArrayCodeByCodeList(arCodeList):
		cat=sum(arCodeList, [])
		arCode=cat[:3]+cat[-1:] if len(cat)>4 else cat
		return arCode

