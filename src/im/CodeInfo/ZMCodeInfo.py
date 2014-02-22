from gear.CodeInfo import CodeInfo

class ZMCodeInfo(CodeInfo):
	def __init__(self):
		CodeInfo.__init__(self)

		self._zm_rtlist=None

		self._zm_extra=None
		self._zm_single=None

	def setRadixCodeProperties(self, propDict):
		extra_code=propDict.get('補充資訊')
		str_rtlist=propDict.get('資訊表示式')

		self._zm_code=''
		self._zm_extra=extra_code
		self._zm_single=propDict.get('獨體編碼')
		self._zm_rtlist=[]
		if str_rtlist!=None:
			rtlist=str_rtlist.split(',')
			self.setZMProp(rtlist)

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

