from gear.CodeInfo import CodeInfo

class CJCodeInfo(CodeInfo):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	RADIX_丨='$丨'
	RADIX_乚='$乚'
	RADIX_丨丨='$丨丨'
	RADIX_儿='$儿'

	radixToCodeDict={
		RADIX_丨:['*', ['l']],
		RADIX_乚:['*', ['u']],
		RADIX_丨丨:['-', ['l', 'l']],
		RADIX_儿:['-', ['h', 'u']],
	}

	def __init__(self, singleCode, direction, radixList, cjBody, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)
		self._cj_single=singleCode


		self._cj_rtlist=radixList
		self._cj_direction=direction
		self._cj_body=cjBody

	@staticmethod
	def generateCodeInfo(propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupportingFromProperty(propDict)

		direction='*'
		singleCode=propDict.get('獨體編碼')
		rtlist=[]
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			rtlist=str_rtlist.split(CJCodeInfo.RADIX_SEPERATOR)

		cjBody=CJCodeInfo.computeBodyCode(rtlist, direction)
		codeInfo=CJCodeInfo(singleCode, direction, rtlist, cjBody, isSupportCharacterCode, isSupportRadixCode)

		return codeInfo

	def getSingletonCode(self):
		return self._cj_single

	def getDirection(self):
		return self._cj_direction

	def getRtList(self):
		return self._cj_rtlist

	def getSingle(self):
		return self._cj_single

	def getBodyCode(self):
		return self._cj_body

