from gear.CodeInfo import CodeInfo

class BSCodeInfo(CodeInfo):
	def setRadixCodeProperties(self, propDict):
		self._bs_single=propDict.get('獨體編碼')
		str_incode=propDict.get('資訊表示式')
		str_spcode=propDict.get('嘸蝦米補碼')
		if str_incode!=None and str_spcode!=None:
			self.setBSProp(str_incode, str_spcode)

	@property
	def characterCode(self):
		if self._bs_single:
			return self._bs_single
		if self._bs_incode==None or self._bs_spcode==None:
			return None
		elif len(self._bs_incode)<3:
			return self._bs_incode+self._bs_spcode
		else:
			return self._bs_incode

	def setDataEmpty(self):
		self._bs_incode=None
		self._bs_spcode=None

	def setSingleDataEmpty(self):
		self._bs_single=None

	def setBSProp(self, bs_incode, bs_spcode):
		if bs_incode!=None and bs_spcode!=None:
			self._bs_incode=bs_incode
			self._bs_spcode=bs_spcode

	def getBSProp(self):
		return [self._bs_incode, self._bs_spcode]

