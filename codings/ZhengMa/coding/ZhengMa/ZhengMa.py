from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

class ZMCodeInfo(CodeInfo):
	def __init__(self, rtList, extraCode, rtListSingleton):
		super().__init__()

		self._zm_code=''
		self._codeList=rtList
		self._codeListSingleton=rtListSingleton

		self._zm_extra=extraCode

	@staticmethod
	def generateDefaultCodeInfo(rtlist):
		codeInfo=ZMCodeInfo(rtlist, None, None)
		return codeInfo

	def toCode(self):
		if self._codeListSingleton:
			rtlist=sum(self._codeListSingleton, [])
			codeList=self.convertRadixListToCodeList(rtlist)
			ans=self.computeCharacterCode(codeList)
			return ans
		else:
			rtlist=self.getRtList()
			codeList=self.convertRadixListToCodeList(rtlist)
			ans=self.computeCharacterCode(codeList)
			extraCode=self.getExtraCode()
			if extraCode:
				ans+=extraCode
			return ans

	def convertRadixListToCodeList(self, radixList):
		return radixList

	def computeCharacterCode(self, rtlist):
		ans=''
		tmp_rtlist=rtlist
		if len(tmp_rtlist)==0:
			return None
		elif len(tmp_rtlist)==1:
			ans=rtlist[0]
		elif len(tmp_rtlist)==2:
			if len(tmp_rtlist[0])==1 and len(tmp_rtlist[1])==1:
				ans=''.join(rtlist[0:2])
				ans=rtlist[0][0]+rtlist[-1][0]+'vv'
			else:
				ans=(rtlist[0]+rtlist[-1])[:4]
		elif len(tmp_rtlist)==3:
			if len(tmp_rtlist[0])==1:
				ans=rtlist[0][0]+rtlist[1][0]+rtlist[-1][0:2]
			elif len(tmp_rtlist[0])==2:
				ans=rtlist[0][0:2]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0])==3:
				ans=rtlist[0][0:3]+rtlist[-1][0]
			else:
				# 錯誤處理
				ans=rtlist[0][0:4]
		elif len(tmp_rtlist)>=4:
			if len(tmp_rtlist[0])==1:
				ans=rtlist[0][0]+rtlist[1][0]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0])==2:
				ans=rtlist[0][0:2]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0])==3:
				ans=rtlist[0][0:3]+rtlist[-1][0]
			else:
				# 錯誤處理
				ans=rtlist[0][0:4]
		else:
			ans=''
		return ans

	def getExtraCode(self):
		return self._zm_extra

	def getRtList(self):
		return self.getMainCodeList()


	def isInstallmentEncoded(self):
		return len(self._codeList)>1

	def getMainCodeList(self):
		if self._codeList != None:
			return sum(self._codeList, [])
		return None

	def getInstallmentCode(self, index):
		return self._codeList[index]

class ZMCodeInfoEncoder(CodeInfoEncoder):
	def generateDefaultCodeInfo(self, rtlist):
		return ZMCodeInfo.generateDefaultCodeInfo(rtlist)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=codeInfoList and all(map(lambda x: x.getRtList(), codeInfoList))
		return isAllWithCode


	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """

		rtlist=sum(map(lambda c: c.getRtList(), codeInfoList), [])

		rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
		codeInfo=self.generateDefaultCodeInfo([rtlist])
		return codeInfo


	def encodeAsHan(self, codeInfoList):
		"""運算 "爲" """
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


	def encodeAsYou(self, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		newCodeInfoList=[secondCodeInfo, thirdCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		"""運算 "㒳" """

		rtlist=sum(map(lambda c: c.getRtList(), codeInfoList), [])

		rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
		codeInfo=self.generateDefaultCodeInfo([rtlist[:1]])
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

				# 第一個的補碼不影響結果
				frontCodeInfo=self.generateDefaultCodeInfo([frontMainCode])
				rearCodeInfo=self.generateDefaultCodeInfo([rearMainCode])
				return [frontCodeInfo]+codeInfoList[1:]+[rearCodeInfo]
			else:
				return codeInfoList

class ZMRadixParser(CodingRadixParser):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	ATTRIB_CODE_EXPRESSION='編碼表示式'
	ATTRIB_SUPPLEMENTARY_CODE='補充資訊'
	ATTRIB_SINGLETON_EXPRESSION='獨體表示式'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict=elementCodeInfo

		extra_code=infoDict.get(ZMRadixParser.ATTRIB_SUPPLEMENTARY_CODE)
		strCodeList=infoDict.get(ZMRadixParser.ATTRIB_CODE_EXPRESSION)
		strCodeListSingleton=infoDict.get(ZMRadixParser.ATTRIB_SINGLETON_EXPRESSION)

		zm_code=''
		zm_extra=extra_code
		codeList=[]
		if strCodeList!=None:
			codeList=strCodeList.split(ZMRadixParser.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(ZMRadixParser.RADIX_SEPERATOR), codeList))

		codeListSingleton=[]
		if strCodeListSingleton!=None:
			codeListSingleton=strCodeListSingleton.split(ZMRadixParser.INSTALLMENT_SEPERATOR)
			codeListSingleton=list(map(lambda x: x.split(ZMRadixParser.RADIX_SEPERATOR), codeListSingleton))

		codeInfo=ZMCodeInfo(codeList, zm_extra, codeListSingleton)
		return codeInfo

