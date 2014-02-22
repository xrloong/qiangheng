from gear.CodeInfo import CodeInfo

class ZMCodeInfo(CodeInfo):
	def __init__(self, singleCode, rtList, extraCode, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

		self._zm_code=''
		self._zm_rtlist=rtList

		self._zm_extra=extraCode
		self._zm_single=singleCode

	def setCharacterCode(self, zmCode):
		self._zm_code=zmCode

	def getSingletonCode(self):
		return self._zm_single

	def getCharacterCode(self):
		return self._zm_code

	def getExtraCode(self):
		return self._zm_extra

	def getZMProp(self):
		return self._zm_rtlist

	def getRtList(self):
		return self._zm_rtlist

