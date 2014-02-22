from gear.CodeInfo import CodeInfo

class ARCodeInfo(CodeInfo):
	def setRadixCodeProperties(self, propDict):
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			self.setARProp(str_rtlist)

	@property
	def characterCode(self):
		return self._ar_incode

	def setDataEmpty(self):
		self._ar_incode=None

	def setSingleDataEmpty(self):
		pass

	def setARProp(self, ar_incode):
		if ar_incode!=None:
			self._ar_incode=ar_incode

	def getARProp(self):
		return self._ar_incode

