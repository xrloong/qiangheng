from gear.CodeInfo import CodeInfo

class ZMCodeInfo(CodeInfo):
	def __init__(self, singleCode, rtList, extraCode, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

		self._zm_code=''
		self._zm_rtlist=rtList

		self._zm_extra=extraCode
		self._zm_single=singleCode

	@property
	def characterCode(self):
		if self._zm_single:
			return self._zm_single

		ans=self._zm_code
		if self._zm_extra:
			ans+=self._zm_extra
		return ans

	def setCharacterCode(self, zmCode):
		self._zm_code=zmCode

	def setZMProp(self, zm_rtlist):
		if zm_rtlist!=None:
			self._zm_rtlist=zm_rtlist

	def getZMProp(self):
		return self._zm_rtlist

	def getRtList(self):
		return self._zm_rtlist

