from .CharInfo import CharInfo

class ZMCharInfo(CharInfo):
	def __init__(self, charname, prop):
		super().__init__(charname, prop)

		self.setFlag=False
		self.noneFlag=False

		self._zm_rtlist=[]
		self._zm_incode=None
		self._zm_tpcode=None
		if len(prop)>=1:
			str_rtlist=prop[0]
			if str_rtlist=='XXXX':
				self.setZMProp([])
			else:
				self.setZMProp(str_rtlist.split(','))

	def setZMProp(self, zm_rtlist):
		self._zm_rtlist=zm_rtlist

		self.setFlag=True

	def getZMProp(self):
		return self._zm_rtlist

	def setByComps(self, complist, direction):
		# 計算鄭碼時，不需要知道此字的組成方向

		if all(complist):
			rtlist=sum(map(lambda c: c.getZMProp(), complist), [])
			if complist and all(rtlist):
				rtlist=rtlist if len(rtlist)<=4 else rtlist[:2]+rtlist[-2:]
				self.setZMProp(rtlist)

	@property
	def zm(self):
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
		elif len(tmp_rtlist)==4:
			if len(tmp_rtlist[0])==1:
				ans=self._zm_rtlist[0][0]+self._zm_rtlist[1][0]+self._zm_rtlist[-2][0]+self._zm_rtlist[-1][0]
			elif len(tmp_rtlist[0])==2:
				ans=self._zm_rtlist[0][0:2]+self._zm_rtlist[-2][0]+self._zm_rtlist[-1][0]
			elif len(tmp_rtlist[0])==3:
				ans=self._zm_rtlist[0][0:3]+self._zm_rtlist[-1][0]
		else:
			ans=''
		return ans

	def getCode(self):
		if self.zm: return self.zm

