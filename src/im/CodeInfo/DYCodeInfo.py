from gear.CodeInfo import CodeInfo

class DYCodeInfo(CodeInfo):
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
	RADIX_0='0'
	RADIX_1='1'
	RADIX_2='2'
	RADIX_3='3'
	RADIX_4='4'
	RADIX_5='5'
	RADIX_6='6'
	RADIX_7='7'
	RADIX_8='8'
	RADIX_9='9'
	RADIX_DOT='.'
	RADIX_COMMA=':'
	RADIX_SEMICOLON=';'
	RADIX_SLASH='/'

	RADIX_EXTEND_E1='e1'	# 即一
	RADIX_EXTEND_H1='h1'	# 即厂
	RADIX_EXTEND_H2='h2'	# 威的前三筆

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
		RADIX_0:'0',
		RADIX_1:'1',
		RADIX_2:'2',
		RADIX_3:'3',
		RADIX_4:'4',
		RADIX_5:'5',
		RADIX_6:'6',
		RADIX_7:'7',
		RADIX_8:'8',
		RADIX_9:'9',
		RADIX_DOT:'.',
		RADIX_COMMA:',',
		RADIX_SEMICOLON:';',
		RADIX_SLASH:'/',

		RADIX_EXTEND_E1:'e',
		RADIX_EXTEND_H1:'h',
		RADIX_EXTEND_H2:'h',
	}

	def __init__(self, codeList, isSupportCharacterCode=True, isSupportRadixCode=True):
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

