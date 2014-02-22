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
	RADIX_EXTEND_9_UP='x:9^:1'	# 即[特微]，由彳、山、一所組成
	RADIX_EXTEND_9_BOTTOM='x:9v:1'	# 即彳，可用來合併字根
	RADIX_EXTEND_3_CENTER='x:3-:1'	# 即山，可用來合併字根
	RADIX_EXTEND_3_CENTER_1_CENTER='x:3-:1-:1'	# 即[山一]，[特微]的右半部

#	RADIX_EXTEND_6_UP='x:6^:1'	# 即亠，可用來合併字根
#	RADIX_EXTEND_9_BOTTOM_2='x:9v:2'	# 即乂
	RADIX_EXTEND_6_UP_9_BOTTOM='x:6^:9v:1'	# 即文
	RADIX_EXTEND_1_BOTTOM='x:1v:1'	# 即厂
	RADIX_EXTEND_6_UP_9_BOTTOM_1_BUTTOM='x:6^:9v:1v'	# 即[文厂]

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

		RADIX_EXTEND_9_UP:'o',
		RADIX_EXTEND_9_BOTTOM:'.',
		RADIX_EXTEND_3_CENTER:'d',
		RADIX_EXTEND_3_CENTER_1_CENTER:'da',

#		RADIX_EXTEND_6_UP:'y',
#		RADIX_EXTEND_9_BOTTOM_2:'.',
		RADIX_EXTEND_6_UP_9_BOTTOM:'y.',
		RADIX_EXTEND_1_BOTTOM:'z',
		RADIX_EXTEND_6_UP_9_BOTTOM_1_BUTTOM:'n',
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

