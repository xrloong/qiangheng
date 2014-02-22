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

		dyCode=DYCodeInfoEncoder.computeDaYiCode(codeInfoList)
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
		dyCode=DYCodeInfoEncoder.computeDaYiCodeForGe(codeInfoList)
		codeInfo=self.generateDefaultCodeInfo([dyCode])
		return codeInfo

	def encodeAsTong(self, codeInfoList):
		"""運算 "同" """
		dyCode=DYCodeInfoEncoder.computeDaYiCodeForGe(codeInfoList)
		codeInfo=self.generateDefaultCodeInfo([dyCode])
		return codeInfo

	def encodeAsHan(self, codeInfoList):
		"""運算 "函" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		dyCode=DYCodeInfoEncoder.computeDaYiCodeForGe(newCodeInfoList)
		codeInfo=self.generateDefaultCodeInfo([dyCode])
		return codeInfo


	def encodeAsZhe(self, codeInfoList):
		"""運算 "這" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		codeInfo=self.encodeAsLoong([secondCodeInfo, firstCodeInfo])
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		"""運算 "載" """
		dyCode=DYCodeInfoEncoder.computeDaYiCodeForGe(codeInfoList)
		codeInfo=self.generateDefaultCodeInfo([dyCode])
		return codeInfo


	def encodeAsLuan(self, codeInfoList):
		"""運算 "䜌" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		codeInfo=self.encodeAsLoong([firstCodeInfo, secondCodeInfo, secondCodeInfo])
		return codeInfo

	@staticmethod
	def computeDaYiCode(codeInfoList):
		dyCodeList=list(map(lambda c: c.getMainCodeList(), codeInfoList))
		return DYCodeInfoEncoder.computeDaYiCodeByCodeList(dyCodeList)

	def computeDaYiCodeByCodeList(dyCodeList):
		cat=sum(dyCodeList, [])
		dyCode=cat[:3]+cat[-1:] if len(cat)>4 else cat
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

				tmpDyCodeList=DYCodeInfoEncoder.mergeRadixAsSilkworm(dyCodeList)
				dyCode=DYCodeInfoEncoder.computeDaYiCodeByCodeList(tmpDyCodeList)
			else:
				dyCode=DYCodeInfoEncoder.computeDaYiCode(codeInfoList)
		return dyCode

	@staticmethod
	def mergeRadixAsSilkworm(dyCodeList):
		tmpDyCodeList=copy.copy(dyCodeList)

		numDyCode=len(tmpDyCodeList)
		for i in range(numDyCode-1):
			dyCodePrev=tmpDyCodeList[i]
			dyCodeNext=tmpDyCodeList[i+1]
			if len(dyCodePrev)>0 and len(dyCodeNext)>0:
				if dyCodePrev[-1]==DYCodeInfo.RADIX_厂 and dyCodeNext[0]==DYCodeInfo.RADIX_一:
					tmpDyCodeList[i]=dyCodePrev[:-1]+[DYCodeInfo.RADIX_厂一]
					tmpDyCodeList[i+1]=dyCodeNext[1:]

		# 合併字根後，有些字根列可能為空，如：戓
		tmpDyCodeList=filter(lambda x: len(x)>0, tmpDyCodeList)

		return tmpDyCodeList
