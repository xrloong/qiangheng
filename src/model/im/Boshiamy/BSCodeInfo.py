from model.base.CodeInfo import CodeInfo

class BSCodeInfo(CodeInfo):
	RADIX_A='a'
	RADIX_B='b'
	RADIX_C='c'
	RADIX_D='d'
	RADIX_E='e'
	RADIX_F='f'
	RADIX_G='g'
	RADIX_H='h'
	RADIX_I='i'
	RADIX_J='j'
	RADIX_K='k'
	RADIX_L='l'
	RADIX_M='m'
	RADIX_N='n'
	RADIX_O='o'
	RADIX_P='p'
	RADIX_Q='q'
	RADIX_R='r'
	RADIX_S='s'
	RADIX_T='t'
	RADIX_U='u'
	RADIX_V='v'
	RADIX_W='w'
	RADIX_X='x'
	RADIX_Y='y'
	RADIX_Z='z'

	COMPLEMENTARY_A='a'
	COMPLEMENTARY_E='e'
	COMPLEMENTARY_I='i'
	COMPLEMENTARY_J='j'
	COMPLEMENTARY_K='k'
	COMPLEMENTARY_L='l'
	COMPLEMENTARY_N='n'
	COMPLEMENTARY_O='o'
	COMPLEMENTARY_P='p'
	COMPLEMENTARY_X='x'
	COMPLEMENTARY_Y='y'

	radixToCodeDict={
		RADIX_A:'a',
		RADIX_B:'b',
		RADIX_C:'c',
		RADIX_D:'d',
		RADIX_E:'e',
		RADIX_F:'f',
		RADIX_G:'g',
		RADIX_H:'h',
		RADIX_I:'i',
		RADIX_J:'j',
		RADIX_K:'k',
		RADIX_L:'l',
		RADIX_M:'m',
		RADIX_N:'n',
		RADIX_O:'o',
		RADIX_P:'p',
		RADIX_Q:'q',
		RADIX_R:'r',
		RADIX_S:'s',
		RADIX_T:'t',
		RADIX_U:'u',
		RADIX_V:'v',
		RADIX_W:'w',
		RADIX_X:'x',
		RADIX_Y:'y',
		RADIX_Z:'z',
	}

	def __init__(self, codeList, supplementCode, isDigital):
		super().__init__()

		self._codeList=codeList
		self._bs_spcode=supplementCode
		self._is_digital=isDigital

	@staticmethod
	def generateDefaultCodeInfo(codeList, supplementCode):
		codeInfo=BSCodeInfo(codeList, supplementCode, False)
		return codeInfo

	def toCode(self):
		codeList=self.getBSCodeList()
		supplementCode=self.getBSSupplement()
		
		if codeList==None or supplementCode==None:
			return None
		else:
			code="".join(map(lambda x: BSCodeInfo.radixToCodeDict[x], codeList))
			if len(code)<3:
				if self.isDigital():
					# 根據嘸蝦米規則，如果是一到十等數目的字，則不用加補碼
					return code
				else:
					return code+supplementCode
			elif len(code)>4:
				return code[:3]+code[-1:]
			else:
				return code

	def getBSCodeList(self):
		return self.getMainCodeList()

	def getBSSupplement(self):
		return self._bs_spcode

	def isDigital(self):
		return self._is_digital

	def isInstallmentEncoded(self):
		return len(self._codeList)>1

	def getMainCodeList(self):
		if self._codeList != None:
			return sum(self._codeList, [])
		return None

	def getInstallmentCode(self, index):
		return self._codeList[index]

