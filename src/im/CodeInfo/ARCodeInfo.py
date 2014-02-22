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

	RADIX_一口='$一口'
	RADIX_一='$一'
	RADIX_口='$口'
	RADIX_士冖='$士冖'
	RADIX_士='$士'
	RADIX_冖='$冖'
	RADIX_彳山一='$彳山一'
	RADIX_彳='$彳'
	RADIX_山='$山'
	RADIX_山一='$山一'

	RADIX_文='$文'
	RADIX_厂='$厂'
	RADIX_文厂='$文厂'

	RADIX_儿='$儿'
	RADIX_乚='$乚'
	RADIX_丨='$丨'
	RADIX_丨丨='$丨丨'

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

		RADIX_一口:'q',
		RADIX_一:'a',
		RADIX_口:';',

		RADIX_士冖:'v',
		RADIX_士:'r',
		RADIX_冖:'j',

		RADIX_彳山一:'o',
		RADIX_彳:'.',
		RADIX_山:'d',
		RADIX_山一:'da',

		RADIX_文:'y.',
		RADIX_厂:'z',
		RADIX_文厂:'n',

		RADIX_儿:'s',
		RADIX_乚:'s',
		RADIX_丨:'d',
		RADIX_丨丨:'e',
	}

	def __init__(self, codeList=None, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

		self._codeList=codeList

	def isInstallmentEncoded(self):
		return len(self._codeList)>1

	def getMainCodeList(self):
		if self._codeList != None:
			return sum(self._codeList, [])
		return None

	def getInstallmentCode(self, index):
		return self._codeList[index]

