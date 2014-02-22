from .CharInfo import CharInfo

class BSCharInfo(CharInfo):
	def __init__(self, propDict={}):
		super().__init__(propDict)

		self.setFlag=False

		self._bs_incode=None
		self._bs_spcode=None

		self.setPropDict(propDict)

	def setPropDict(self, propDict):
		self._bs_single=propDict.get('獨體編碼')
		str_incode=propDict.get('資訊表示式')
		str_spcode=propDict.get('嘸蝦米補碼')
		if str_incode!=None and str_spcode!=None:
			self.setBSProp(str_incode, str_spcode)

	def setBSProp(self, bs_incode, bs_spcode):
		self._bs_incode=bs_incode
		self._bs_spcode=bs_spcode

		self.setFlag=True

	def getBSProp(self):
		return [self._bs_incode, self._bs_spcode]

	def setByComps(self, operator, complist):
		bslist=list(map(lambda c: c.getBSProp()[0], complist))
		if complist and all(bslist):
			cat="".join(bslist)
			bs_incode=(cat[:3]+cat[-1]) if len(cat)>4 else cat
			bs_spcode=complist[-1].getBSProp()[1]
			self.setBSProp(bs_incode, bs_spcode)

	@property
	def bs(self):
		if self._bs_incode==None or self._bs_spcode==None:
			return None
		if self._bs_single:
			return self._bs_single
		elif len(self._bs_incode)<3:
			return self._bs_incode+self._bs_spcode
		else:
			return self._bs_incode

	def getCode(self):
		if self.bs: return self.bs

