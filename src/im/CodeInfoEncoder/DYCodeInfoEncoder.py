import sys
import copy

from ..CodeInfo.DYCodeInfo import DYCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder

class DYCodeInfoEncoder(CodeInfoEncoder):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, codeList):
		codeInfo=DYCodeInfo(codeList)
		return codeInfo

	def generateCodeInfo(self, propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfoEncoder.computeSupportingFromProperty(propDict)
		strCodeList=propDict.get('資訊表示式')

		codeList=None
		if strCodeList!=None:
			codeList=strCodeList.split(DYCodeInfoEncoder.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(DYCodeInfoEncoder.RADIX_SEPERATOR), codeList))

		codeInfo=DYCodeInfo(codeList, isSupportCharacterCode, isSupportRadixCode)
		return codeInfo

	def interprettCharacterCode(self, codeInfo):
		mainRadixList=codeInfo.getMainCodeList()
		mainCodeList=list(map(lambda x: DYCodeInfo.radixToCodeDict[x], mainRadixList))
		code="".join(mainCodeList)
		return (code[:3]+code[-1:] if len(code)>4 else code)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getMainCodeList(), codeInfoList))
		return isAllWithCode

	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """

		dyCodeList=list(map(lambda c: c.getMainCodeList(), codeInfoList))
		dyCode=DYCodeInfoEncoder.computeDaYiCodeByCodeList(dyCodeList)
		codeInfo=self.generateDefaultCodeInfo([dyCode])
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLoop(self, codeInfoList):
		"""運算 "回" """
		newCodeInfoList=self.getMergedCodeInfoListAsForGe(codeInfoList)
		codeInfo=self.encodeAsLoong(newCodeInfoList)
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
		newCodeInfoList=self.getMergedCodeInfoListAsForGe(newCodeInfoList)
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


	def encodeAsLuan(self, codeInfoList):
		"""運算 "䜌" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		codeInfo=self.encodeAsLoong([firstCodeInfo, secondCodeInfo, secondCodeInfo])
		return codeInfo

	@staticmethod
	def computeDaYiCodeByCodeList(dyCodeList):
		cat=sum(dyCodeList, [])
		dyCode=cat[:3]+cat[-1:] if len(cat)>4 else cat
		return dyCode

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

	def getMergedCodeInfoListAsSilkworm(self, codeInfoList):
		firstCodeInfo=None
		secondCodeInfo=None

		mergeCodeInfoList=[
			[DYCodeInfo.RADIX_厂, DYCodeInfo.RADIX_一, DYCodeInfo.RADIX_厂一],
		]

		return self.getMergedCodeInfoList(codeInfoList, mergeCodeInfoList)

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
				return self.getMergedCodeInfoListAsSilkworm([frontCodeInfo]+codeInfoList[1:]+[rearCodeInfo])
			else:
				return codeInfoList
