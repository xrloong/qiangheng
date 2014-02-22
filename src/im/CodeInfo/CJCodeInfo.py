from gear.CodeInfo import CodeInfo

class CJCodeInfo(CodeInfo):
	def __init__(self, isSupportCharacterCode=True, isSupportRadixCode=True):
		CodeInfo.__init__(self, isSupportCharacterCode, isSupportRadixCode)

		self._cj_radix_list=None
		self._cj_direction=None
		self._cj_body=None

		self._cj_single=None

	def setRadixCodeProperties(self, propDict):
		self._cj_single=propDict.get('獨體編碼')
		self._cj_rtlist=[]
		str_rtlist=propDict.get('資訊表示式')
		if str_rtlist!=None:
			self.setCJProp('*', [str_rtlist])
			self._cj_rtlist=[str_rtlist]

	@property
	def characterCode(self):
		if self._cj_single:
			return self._cj_single
		else:
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

