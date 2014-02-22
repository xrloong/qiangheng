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
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			self.setBSProp(str_rtlist)

	def setBSProp(self, bs_x_code):
		bs_list=bs_x_code.split(',')

		if len(bs_list)>=2 and bs_list[0] != 'XXXX' and bs_list[1]!='XXXX':
			self._bs_incode=bs_list[0]
			self._bs_spcode=bs_list[1]
		else:
			self._bs_incode=None
			self._bs_spcode=None

		self.setFlag=True

	def getBSProp(self):
		return [self._bs_incode, self._bs_spcode]

	def setByComps(self, operator, complist):
		bslist=list(map(lambda c: c.getBSProp()[0], complist))
		if complist and all(bslist):
			cat="".join(bslist)
			bs_incode=(cat[:3]+cat[-1]) if len(cat)>4 else cat
			bs_spcode=complist[-1].getBSProp()[1]
			self.setBSProp(','.join([bs_incode, bs_spcode]))

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

