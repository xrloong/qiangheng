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

	def __init__(self, singleCode, rtList, extraCode):
		CodeInfo.__init__(self)

		self._zm_code=''
		self._codeList=rtList

		self._zm_extra=extraCode
		self._zm_single=singleCode

	@staticmethod
	def generateDefaultCodeInfo(rtlist):
		codeInfo=ZMCodeInfo(None, rtlist, None)
		return codeInfo

	def toCode(self):
		singletonCode=self.getSingletonCode()
		if singletonCode:
			return singletonCode

		rtlist=self.getRtList()
		codeList=self.convertRadixListToCodeList(rtlist)
		ans=self.computeCharacterCode(codeList)
		extraCode=self.getExtraCode()
		if extraCode:
			ans+=extraCode
		return ans

	def convertRadixListToCodeList(self, radixList):
		return sum([ZMCodeInfo.radixToCodeDict.get(radix, [radix]) for radix in radixList], [])

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

