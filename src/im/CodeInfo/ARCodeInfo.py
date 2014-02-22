import sys
from gear.CodeInfo import CodeInfo

class ARCodeInfo(CodeInfo):
	radixToCodeDict={
		'1-':'a',
		'5v':'b',
		'3v':'c',
		'3-':'d',
		'3^':'e',
		'4-':'f',
		'5-':'g',
		'6-':'h',
		'8^':'i',
		'7-':'j',
		'8-':'k',
		'9-':'l',
		'7v':'m',
		'6v':'n',
		'9^':'o',
		'0^':'p',
		'1^':'q',
		'4^':'r',
		'2-':'s',
		'5^':'t',
		'7^':'u',
		'4v':'v',
		'2^':'w',
		'2v':'x',
		'6^':'y',
		'1v':'z',
		'9v':'.',
		'8v':',',
		'0v':'/',
		'0-':';',
	}
	def setRadixCodeProperties(self, propDict):
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			codeList=str_rtlist.split('|')
			codeList=list(map(lambda x: x.split(':'), codeList))
			self.setCodeList(codeList)

	@property
	def characterCode(self):
		mainRadixList=self.getMainCode()
		mainCodeList=list(map(lambda x: ARCodeInfo.radixToCodeDict[x], mainRadixList))
		return "".join(mainCodeList)

	def setDataEmpty(self):
		self._codeList=None

	def setSingleDataEmpty(self):
		pass

	def isInstallmentEncoded(self):
		return len(self._codeList)>1

	def setCodeList(self, codeList):
		self._codeList=codeList

	def getMainCode(self):
		if self._codeList != None:
#			return "".join(self._codeList)
			return sum(self._codeList, [])
		return None

	def getInstallmentCode(self, index):
		return self._codeList[index]

