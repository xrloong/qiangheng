from gear.CodeInfo import CodeInfo

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

	RADIX_E1='e1'	# 即一
	RADIX_E2='e2'	# 即山
	RADIX_E2_E1='e2:e1'	# 即[山一]
	RADIX_M1='m1'	# 即彳的前兩筆
	RADIX_M1_E2_E1='m1:e2:e1'	# 即[特微]

#	RADIX_W1='w1'	# 即辶
#	RADIX_W2='w2'	# 即廴

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

		RADIX_E1:'e',
		RADIX_E2:'e',
		RADIX_E2_E1:'ee',
		RADIX_M1:'m',
		RADIX_M1_E2_E1:'m',
	}

	def __init__(self):
		CodeInfo.__init__(self)

		self._bs_code_list=None
		self._bs_spcode=None

		self._bs_single=None

	def setRadixCodeProperties(self, propDict):
		self._bs_single=propDict.get('獨體編碼')
		str_incode=propDict.get('資訊表示式')
		str_spcode=propDict.get('嘸蝦米補碼')
		if str_incode!=None and str_spcode!=None:
			_code_list=str_incode.split(',')
			self.setBSProp(_code_list, str_spcode)

	@property
	def characterCode(self):
		if self._bs_single:
			return self._bs_single
		if self._bs_code_list==None or self._bs_spcode==None:
			return None
		else:
			code="".join(map(lambda x: BSCodeInfo.radixToCodeDict[x], self._bs_code_list))
			if len(code)<3:
				return code+self._bs_spcode
			elif len(code)>4:
				return code[:3]+code[-1:]
			else:
				return code

	def setBSProp(self, bs_code_list, bs_spcode):
		if bs_code_list!=None and bs_spcode!=None:
			self._bs_code_list=bs_code_list
			self._bs_spcode=bs_spcode

	def getBSProp(self):
		return [self._bs_code_list, self._bs_spcode]

