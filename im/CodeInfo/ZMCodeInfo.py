from .CodeInfo import CodeInfo

class ZMCodeInfo(CodeInfo):
	def setPropDict(self, propDict):
		extra_code=propDict.get('補充資訊')
		str_rtlist=propDict.get('資訊表示式')

		self._zm_extra=extra_code
		self._zm_single=propDict.get('獨體編碼')
		if str_rtlist!=None:
			rtlist=str_rtlist.split(',')
			self.setZMProp(rtlist)

	def setByComps(self, operator, complist):
		if all(complist):
			rtlist=sum(map(lambda c: c.getZMProp(), complist), [])
			if complist and all(rtlist):
				rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
				self.setZMProp(rtlist)

	@property
	def code(self):
		if self._zm_single:
			return self._zm_single

		ans=''
		tmp_rtlist=self._zm_rtlist
		if len(tmp_rtlist)==0:
			return None
		elif len(tmp_rtlist)==1:
			ans=self._zm_rtlist[0]
		elif len(tmp_rtlist)==2:
			if len(tmp_rtlist[0])==1 and len(tmp_rtlist[1])==1:
				ans=''.join(self._zm_rtlist[0:2])
				ans=self._zm_rtlist[0][0]+self._zm_rtlist[-1][0]+'vv'
			else:
				ans=(self._zm_rtlist[0]+self._zm_rtlist[-1])[:4]
		elif len(tmp_rtlist)==3:
			if len(tmp_rtlist[0])==1:
				ans=self._zm_rtlist[0][0]+self._zm_rtlist[1][0]+self._zm_rtlist[-1][0:2]
			elif len(tmp_rtlist[0])==2:
				ans=self._zm_rtlist[0][0:2]+self._zm_rtlist[-2][0]+self._zm_rtlist[-1][0]
			elif len(tmp_rtlist[0])==3:
				ans=self._zm_rtlist[0][0:3]+self._zm_rtlist[-1][0]
		elif len(tmp_rtlist)>=4:
			if len(tmp_rtlist[0])==1:
				ans=self._zm_rtlist[0][0]+self._zm_rtlist[1][0]+self._zm_rtlist[-2][0]+self._zm_rtlist[-1][0]
			elif len(tmp_rtlist[0])==2:
				ans=self._zm_rtlist[0][0:2]+self._zm_rtlist[-2][0]+self._zm_rtlist[-1][0]
			elif len(tmp_rtlist[0])==3:
				ans=self._zm_rtlist[0][0:3]+self._zm_rtlist[-1][0]
		else:
			ans=''
		if self._zm_extra:
			ans+=self._zm_extra
		return ans

	def setDataEmpty(self):
		CodeInfo.setDataEmpty(self)
		self._zm_rtlist=None

	def setSingleDataEmpty(self):
		self._zm_extra=None
		self._zm_single=None

	def setZMProp(self, zm_rtlist):
		if zm_rtlist!=None:
			self.setDataInitialized()
			self._zm_rtlist=zm_rtlist

	def getZMProp(self):
		return self._zm_rtlist

