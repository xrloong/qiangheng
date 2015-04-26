from model.base.CodeInfo import CodeInfo

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

