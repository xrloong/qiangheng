from gear.CodeInfo import CodeInfo

class DYCodeInfo(CodeInfo):
	def setRadixCodeProperties(self, propDict):
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			codeList=str_rtlist.split('|')
			self.setCodeList(codeList)

	@property
	def characterCode(self):
		return self.getMainCode()

	def setDataEmpty(self):
		pass

	def setSingleDataEmpty(self):
		pass

	def isInstallmentEncoded(self):
		return len(self._codeList)>1

	def setCodeList(self, codeList):
		self._codeList=codeList

	def getMainCode(self):
		if self._codeList != None:
			return "".join(self._codeList)
		return None

	def getInstallmentCode(self, index):
		return self._codeList[index]

