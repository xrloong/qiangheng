from ..base.CodeInfo import CodeInfo

import sys

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
	}

	def __init__(self, codeList=[]):
		CodeInfo.__init__(self)

		self._codeList=codeList

	@staticmethod
	def generateDefaultCodeInfo(codeList):
		codeInfo=ARCodeInfo(codeList)
		return codeInfo

	def toCode(self):
		mainRadixList=self.getMainCodeList()
		mainCodeList=list(map(lambda x: ARCodeInfo.radixToCodeDict[x], mainRadixList))
		code="".join(mainCodeList)
		return (code[:3]+code[-1] if len(code)>4 else code)


	def isInstallmentEncoded(self):
		return len(self._codeList)>1

	def getMainCodeList(self):
		if self._codeList != None:
			return sum(self._codeList, [])
		return None

	def getInstallmentCode(self, index):
		return self._codeList[index]

