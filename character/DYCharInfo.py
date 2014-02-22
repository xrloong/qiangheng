from .CharInfo import CharInfo

class DYCharInfo(CharInfo):
	def __init__(self, propDict={}):
		super().__init__(propDict)

		self.setFlag=False

		self._dy_incode=None
		self._flag_seted=False

		self.setPropDict(propDict)

	def setPropDict(self, propDict):
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			self.setDYProp(str_rtlist)

	def setDYProp(self, dy_incode):
		if dy_incode=='XXXX':
			self._dy_incode=None
		else:
			self._dy_incode=dy_incode
		self._flag_seted=True

		self.setFlag=True

	def getDYProp(self):
		return self._dy_incode

	def setByComps(self, operator, complist):
		dylist=list(map(lambda c: c.getDYProp(), complist))
		if complist and all(dylist):
			cat="".join(dylist)
			dy=cat[:3]+cat[-1] if len(cat)>4 else cat
			self.setDYProp(dy)

	@property
	def dy(self):
		return self._dy_incode

	def getCode(self):
		if self.dy: return self.dy

