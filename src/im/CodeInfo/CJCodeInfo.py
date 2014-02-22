from gear.CodeInfo import CodeInfo

class CJCodeInfo(CodeInfo):
	def __init__(self, singleCode, direction, radixList, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

		self._cj_radix_list=radixList
		self._cj_rtlist=radixList
		self._cj_direction=direction
#		self._cj_body=None

		self._cj_single=singleCode

#		cjBody=CJCodeInfo.computeBodyCode(rtlist, direction)
#		cjTotal=CJCodeInfoEncoder.computeTotalCode(rtlist, direction).lower()
#		self.setCharacter(cjTotal, cjBody)

	def getSingletonCode(self):
		return self._cj_single

	def getTotalCode(self):
		return self._cj_total

	def setCJProp(self, dir_code, codeList):
		if dir_code!=None and codeList!=None:
			self._cj_radix_list=codeList
			self._cj_direction=dir_code

	def getCJProp(self):
		return [self._cj_direction, self._cj_radix_list]

	def setCharacter(self, cjTotal, cjBody):
		self._cj_body=cjBody
		self._cj_total=cjTotal

	def getRtList(self):
		return self._cj_rtlist

	def getSingle(self):
		return self._cj_single

