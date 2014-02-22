import sys
from gear.CodeInfo import CodeInfo

class ARCodeInfo(CodeInfo):
	radixToCodeDict={
		'a':'a',
		'b':'b',
		'c':'c',
		'd':'d',
		'e':'e',
		'f':'f',
		'g':'g',
		'h':'h',
		'i':'i',
		'j':'j',
		'k':'k',
		'l':'l',
		'm':'m',
		'n':'n',
		'o':'o',
		'p':'p',
		'q':'q',
		'r':'r',
		's':'s',
		't':'t',
		'u':'u',
		'v':'v',
		'w':'w',
		'x':'x',
		'y':'y',
		'z':'z',
		'.':'.',
		',':',',
		'/':'/',
		';':';',
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

