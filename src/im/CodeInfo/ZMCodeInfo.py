from gear.CodeInfo import CodeInfo

class ZMCodeInfo(CodeInfo):
	RADIX_彳='$彳'
	RADIX_亍='$亍'
	RADIX_行='$行'

	radixToCodeDict={
		RADIX_彳:["oi"],
		RADIX_亍:["bd","i"],
		RADIX_行:["oi"],
	}

	def __init__(self, singleCode, rtList, extraCode, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

		self._zm_code=''
		self._zm_rtlist=rtList

		self._zm_extra=extraCode
		self._zm_single=singleCode

	def getSingletonCode(self):
		return self._zm_single

	def getExtraCode(self):
		return self._zm_extra

	def getZMProp(self):
		return self._zm_rtlist

	def getRtList(self):
		return self._zm_rtlist

