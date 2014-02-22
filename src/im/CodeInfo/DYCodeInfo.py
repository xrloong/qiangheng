from gear.CodeInfo import CodeInfo

class DYCodeInfo(CodeInfo):
	def setRadixCodeProperties(self, propDict):
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			self.setDYProp(str_rtlist)

	@property
	def characterCode(self):
		return self._dy_incode

	def setDataEmpty(self):
		self._dy_incode=None

	def setSingleDataEmpty(self):
		pass

	def setDYProp(self, dy_incode):
		if dy_incode!=None:
			self._dy_incode=dy_incode

	def getDYProp(self):
		return self._dy_incode

