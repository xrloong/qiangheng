from .CharInfo import CharInfo

class DYCharInfo(CharInfo):
	def __init__(self, prop):
		super().__init__(prop)

		self.setFlag=False

		self._dy_incode=None
		self._flag_seted=False
		if len(prop)>=1:
			self.setDYProp(prop[0])

	def setDYProp(self, dy_incode):
		if dy_incode=='XXXX':
			self._dy_incode=None
		else:
			self._dy_incode=dy_incode
		self._flag_seted=True

		self.setFlag=True

	def getDYProp(self):
		return self._dy_incode

	def setByComps(self, complist, direction):
		# 計算大易碼時，不需要知道此字的組成方向

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

