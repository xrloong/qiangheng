import sys
from gear.CodeInfo import CodeInfo

class ARCodeInfo(CodeInfo):
	RADIX_1_UP='1^'
	RADIX_2_UP='2^'
	RADIX_3_UP='3^'
	RADIX_4_UP='4^'
	RADIX_5_UP='5^'
	RADIX_6_UP='6^'
	RADIX_7_UP='7^'
	RADIX_8_UP='8^'
	RADIX_9_UP='9^'
	RADIX_0_UP='0^'

	RADIX_1_CENTER='1-'
	RADIX_2_CENTER='2-'
	RADIX_3_CENTER='3-'
	RADIX_4_CENTER='4-'
	RADIX_5_CENTER='5-'
	RADIX_6_CENTER='6-'
	RADIX_7_CENTER='7-'
	RADIX_8_CENTER='8-'
	RADIX_9_CENTER='9-'
	RADIX_0_CENTER='0-'

	RADIX_1_BOTTOM='1v'
	RADIX_2_BOTTOM='2v'
	RADIX_3_BOTTOM='3v'
	RADIX_4_BOTTOM='4v'
	RADIX_5_BOTTOM='5v'
	RADIX_6_BOTTOM='6v'
	RADIX_7_BOTTOM='7v'
	RADIX_8_BOTTOM='8v'
	RADIX_9_BOTTOM='9v'
	RADIX_0_BOTTOM='0v'

	RADIX_EXTEND_1_UP='x:1^:1'	# 即[一口]，豆的上部
	RADIX_EXTEND_1_CENTER='x:1-:1'	# 即一，可用來合併字根，末的序列為 '4v,1-' ，但在 '唜' 中，不做合併用。
	RADIX_EXTEND_0_CENTER='x:0-:1'	# 即口，可用來合併字根
	RADIX_EXTEND_4_BOTTOM='x:4v:1'	# 即[士冖]，壹的上部
	RADIX_EXTEND_4_UP='x:4^:1'	# 即士，可用來合併字根
	RADIX_EXTEND_7_CENTER='x:7-:1'	# 即冖，可用來合併字根

	RADIX_EXTEND_5_BOTTOM='x:5v:1'	# 即廴
	RADIX_EXTEND_6_BOTTOM='x:6v:1'	# 即辶
	RADIX_EXTEND_2_CENTER='x:2-:1'	# 即[亾下]
	radixToCodeDict={
		RADIX_1_UP:'q',
		RADIX_2_UP:'w',
		RADIX_3_UP:'e',
		RADIX_4_UP:'r',
		RADIX_5_UP:'t',
		RADIX_6_UP:'y',
		RADIX_7_UP:'u',
		RADIX_8_UP:'i',
		RADIX_9_UP:'o',
		RADIX_0_UP:'p',

		RADIX_1_CENTER:'a',
		RADIX_2_CENTER:'s',
		RADIX_3_CENTER:'d',
		RADIX_4_CENTER:'f',
		RADIX_5_CENTER:'g',
		RADIX_6_CENTER:'h',
		RADIX_7_CENTER:'j',
		RADIX_8_CENTER:'k',
		RADIX_9_CENTER:'l',
		RADIX_0_CENTER:';',

		RADIX_1_BOTTOM:'z',
		RADIX_2_BOTTOM:'x',
		RADIX_3_BOTTOM:'c',
		RADIX_4_BOTTOM:'v',
		RADIX_5_BOTTOM:'b',
		RADIX_6_BOTTOM:'n',
		RADIX_7_BOTTOM:'m',
		RADIX_8_BOTTOM:',',
		RADIX_9_BOTTOM:'.',
		RADIX_0_BOTTOM:'/',

		RADIX_EXTEND_1_UP:'q',
		RADIX_EXTEND_1_CENTER:'a',
		RADIX_EXTEND_0_CENTER:';',

		RADIX_EXTEND_4_BOTTOM:'v',
		RADIX_EXTEND_4_UP:'r',
		RADIX_EXTEND_7_CENTER:'j',

		RADIX_EXTEND_5_BOTTOM:'b',
		RADIX_EXTEND_6_BOTTOM:'n',
		RADIX_EXTEND_2_CENTER:'s',
	}

	def setRadixCodeProperties(self, propDict):
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			codeList=str_rtlist.split('|')
			codeList=list(map(lambda x: x.split(','), codeList))
			self.setCodeList(codeList)

	@property
	def characterCode(self):
		mainRadixList=self.getMainCodeList()
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

	def getMainCodeList(self):
		if self._codeList != None:
			return sum(self._codeList, [])
		return None

	def getInstallmentCode(self, index):
		return self._codeList[index]

