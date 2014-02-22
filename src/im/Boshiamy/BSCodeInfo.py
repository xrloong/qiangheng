from ..base.CodeInfo import CodeInfo

class BSCodeInfo(CodeInfo):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

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

	RADIX_一='$一'
	RADIX_山='$山'
	RADIX_山一='$山$一'
	RADIX_丿丿='$丿丿'
	RADIX_丿丿_山一='$丿丿$山$一'
	RADIX_丨='$丨'
	RADIX_丿='$丿'
	RADIX_乚='$乚'
	RADIX_丨丨='$丨丨'
	RADIX_丨丿='$丨丿'
	RADIX_丿丨='$丿丨'
	RADIX_儿='$儿'
	RADIX_厂='$厂'
	RADIX_厂一='$厂一'

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

		RADIX_一:'e',
		RADIX_山:'e',
		RADIX_山一:'ee',
		RADIX_丿丿:'m',
		RADIX_丿丿_山一:'m',
		RADIX_丨:'i',
		RADIX_丿:'p',
		RADIX_乚:'l',
		RADIX_丨丨:'r',
		RADIX_丨丿:'r',
		RADIX_丿丨:'r',
		RADIX_儿:'r',
		RADIX_厂:'l',
		RADIX_厂一:'f',
	}

	def __init__(self, singletonCode, codeList, supplementCode):
		CodeInfo.__init__(self)

		self._bs_spcode=supplementCode

		self._bs_singleton=singletonCode
		self._codeList=codeList

	@staticmethod
	def generateDefaultCodeInfo(codeList, supplementCode):
		codeInfo=BSCodeInfo(None, codeList, supplementCode)
		return codeInfo

	def toCode(self):
		singletonCode=self.getSingletonCode()
		codeList=self.getBSCodeList()
		supplementCode=self.getBSSupplement()

		if singletonCode:
			return singletonCode
		if codeList==None or supplementCode==None:
			return None
		else:
			code="".join(map(lambda x: BSCodeInfo.radixToCodeDict[x], codeList))
			if len(code)<3:
				return code+supplementCode
			elif len(code)>4:
				return code[:3]+code[-1:]
			else:
				return code

	def getSingletonCode(self):
		return self._bs_singleton

	def getBSCodeList(self):
		return self.getMainCodeList()

	def getBSSupplement(self):
		return self._bs_spcode

	def isInstallmentEncoded(self):
		return len(self._codeList)>1

	def getMainCodeList(self):
		if self._codeList != None:
			return sum(self._codeList, [])
		return None

	def getInstallmentCode(self, index):
		return self._codeList[index]

