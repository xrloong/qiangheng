from .CharInfo import CharInfo

class ARCharInfo(CharInfo):
	def __init__(self, prop):
		super().__init__(prop)

		self.setFlag=False

		self._ar_incode=None
		if len(prop)>=1:
			self.setARProp(prop[0])

	def setARProp(self, ar_incode):
		if ar_incode=='XXXX':
			self._ar_incode=None
		else:
			self._ar_incode=ar_incode

		self.setFlag=True

	def getARProp(self):
		return self._ar_incode

	def setByComps(self, operator, complist):
		arlist=list(map(lambda c: c.getARProp(), complist))
		if complist and all(arlist):
			cat="".join(arlist)
			ar=cat[:3]+cat[-1] if len(cat)>4 else cat
			self.setARProp(ar)

	@property
	def ar(self):
		return self._ar_incode

	def getCode(self):
		if self.ar: return self.ar

