from gear.CodeInfo import CodeInfo

class BSCodeInfo(CodeInfo):
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
		elif len(self._bs_code_list)<3:
			return "".join(self._bs_code_list)+self._bs_spcode
		elif len(self._bs_code_list)>4:
			return "".join(self._bs_code_list[:3]+self._bs_code_list[-1:])
		else:
			return "".join(self._bs_code_list)

	def setDataEmpty(self):
		self._bs_code_list=None
		self._bs_spcode=None

	def setSingleDataEmpty(self):
		self._bs_single=None

	def setBSProp(self, bs_code_list, bs_spcode):
		if bs_code_list!=None and bs_spcode!=None:
			self._bs_code_list=bs_code_list
			self._bs_spcode=bs_spcode

	def getBSProp(self):
		return [self._bs_code_list, self._bs_spcode]

