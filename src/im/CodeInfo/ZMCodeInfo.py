from gear.CodeInfo import CodeInfo

class ZMCodeInfo(CodeInfo):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	RADIX_彳='$彳'
	RADIX_亍='$亍'
	RADIX_行='$行'

	radixToCodeDict={
		RADIX_彳:["oi"],
		RADIX_亍:["bd","i"],
		RADIX_行:["oi"],
	}

	def __init__(self, singleCode, rtList, extraCode, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

		self._zm_code=''
		self._codeList=rtList

		self._zm_extra=extraCode
		self._zm_single=singleCode

	@staticmethod
	def generateCodeInfo(propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupportingFromProperty(propDict)
		extra_code=propDict.get('補充資訊')
		strCodeList=propDict.get('資訊表示式')

		zm_code=''
		zm_extra=extra_code
		zm_single=propDict.get('獨體編碼')
		codeList=[]
		if strCodeList!=None:
			codeList=strCodeList.split(ZMCodeInfo.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(ZMCodeInfo.RADIX_SEPERATOR), codeList))

		codeInfo=ZMCodeInfo(zm_single, codeList, zm_extra, isSupportCharacterCode, isSupportRadixCode)
		return codeInfo

	def getSingletonCode(self):
		return self._zm_single

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

