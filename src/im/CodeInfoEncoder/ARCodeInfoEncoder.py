import sys
import copy

from ..CodeInfo.ARCodeInfo import ARCodeInfo
from gear.CodeInfoEncoder import CodeInfoEncoder
from gear.CodeInfo import CodeInfo

class ARCodeInfoEncoder(CodeInfoEncoder):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	def __init__(self):
		pass

	def generateDefaultCodeInfo(self, codeList):
		codeInfo=ARCodeInfo(codeList)
		return codeInfo

	def generateCodeInfo(self, propDict):
		return ARCodeInfo.generateCodeInfo(propDict)

	def interprettCharacterCode(self, codeInfo):
		mainRadixList=codeInfo.getMainCodeList()
		mainCodeList=list(map(lambda x: ARCodeInfo.radixToCodeDict[x], mainRadixList))
		code="".join(mainCodeList)
		return (code[:3]+code[-1] if len(code)>4 else code)


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


	def encodeAsSilkworm(self, codeInfoList):
		"""運算 "蚕" """
		newCodeInfoList=self.getMergedCodeInfoListAsSilkworm(codeInfoList)
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		"""運算 "鴻" """
		newCodeInfoList=self.getMergedCodeInfoListAsGoose(codeInfoList)
		codeInfo=self.encodeAsLoong(newCodeInfoList)
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


	def encodeAsYin(self, codeInfoList):
		"""運算 "胤" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		if firstCodeInfo.getMainCodeList()[0]==ARCodeInfo.RADIX_儿:
			radix_丨=self.generateDefaultCodeInfo([[ARCodeInfo.RADIX_丨]])
			radix_乚=self.generateDefaultCodeInfo([[ARCodeInfo.RADIX_乚]])
			codeInfo=self.encodeAsGoose([radix_丨, secondCodeInfo, radix_乚])
			return codeInfo
		elif firstCodeInfo.getMainCodeList()[0]==ARCodeInfo.RADIX_丨丨:
			radix_丨=self.generateDefaultCodeInfo([[ARCodeInfo.RADIX_丨]])
			codeInfo=self.encodeAsGoose([radix_丨, secondCodeInfo, radix_丨])
			return codeInfo
		else:
			return self.encodeAsInvalidate()

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

	def getMergedCodeInfoListAsSilkworm(self, codeInfoList):
		firstCodeInfo=None
		secondCodeInfo=None

		mergeCodeInfoList=[
			[ARCodeInfo.RADIX_一, ARCodeInfo.RADIX_口, ARCodeInfo.RADIX_一口],
			[ARCodeInfo.RADIX_士, ARCodeInfo.RADIX_冖, ARCodeInfo.RADIX_士冖],
			[ARCodeInfo.RADIX_山, ARCodeInfo.RADIX_一, ARCodeInfo.RADIX_山一],
			[ARCodeInfo.RADIX_文, ARCodeInfo.RADIX_厂, ARCodeInfo.RADIX_文厂],
		]

		return self.getMergedCodeInfoList(codeInfoList, mergeCodeInfoList)

	def getMergedCodeInfoListAsGoose(self, codeInfoList):
		firstCodeInfo=None
		secondCodeInfo=None

		mergeCodeInfoList=[
			[ARCodeInfo.RADIX_彳, ARCodeInfo.RADIX_山一, ARCodeInfo.RADIX_彳山一],
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

