
class CharInfo:
	def __init__(self, charname, parseans, prop):
		self.charname=charname
		self.operator=parseans[0]
		self.operandlist=parseans[1]

		self.showFlag=False if len(self.charname)>1 else True
		self.noneFlag=True

	def __str__(self):
		return "{{ {0}|{1},{2} }}".format(self.charname, self.operator, self.operandlist)
		return self.charname

	def __repr__(self):
		return str(self)

	def isToShow(self):
		return self.showFlag

	def isToSetTree(self):
		# 若非空且之前没設過值
		return (not self.isNone) and (not self.isSeted)

	def setByComps(self, complist):
		pass

	@property
	def isNone(self):
		# 是否為空
		return self.noneFlag

	@property
	def isSeted(self):
		# 是否之前設過值，會被覆蓋
		return False

	def getCode(self):
		#多型
		return ""

	def updateIMCode(self, chdesc):
		# 多型
		descList=self.normalizationToLinear(chdesc)
		complist=[x.getChInfo() for x in descList]
		self.setByComps(complist)

	def normalizationToLinear(self, comp):
		"""將樹狀結構轉為線性結構"""
		# 多型
		if len(comp.getCompList())==0:
			return [comp]
		return sum(map(lambda x: self.normalizationToLinear(x), comp.getCompList()), [])

CharInfo.NoneChar=CharInfo('[瑲珩預設空字符]', ['龜', []], [])
CharInfo.NoneChar.noneFlag=True

class CJCharInfo(CharInfo):
	def __init__(self, charname, parseans, prop):
		super().__init__(charname, parseans, prop)
		self._cj_incode=None	# 當獨體使用
		self._cj_rtcode=None	# 當部件使用
		if len(prop)>=2:
			self.setCJProp(prop[0], prop[1])
		self.noneFlag=False

	def setCJProp(self, cj_incode, cj_rtcode):
		if cj_incode=='XXXX':
			self._cj_incode=None
		else:
			self._cj_incode=cj_incode

		if cj_rtcode=='XXXX':
#			self._cj_rtcode=None
			# 目前先假設跟 _cj_incode 一樣
			if cj_incode=='XXXX':
				self._cj_rtcode=None
			else:
				self._cj_rtcode=cj_incode
		else:
			self._cj_rtcode=cj_rtcode

	def getCJProp(self):
		return [self._cj_incode, self._cj_rtcode]

	def setCJByComps(self, prelist, postlist):
		def CJCombideCode(first, second):
			tmpfirst=first if len(first)<=2 else first[0]+first[-1]
			tmpsecond=second if len(second)<=2 else second[0]+second[-1]
			anscode=tmpfirst+tmpsecond
			anscode=anscode if len(anscode)<=3 else anscode[0:2]+anscode[-1]
			return anscode

		def getCJRootCodeAsBody(rtcodelist):
			tmpcode=rtcodelist[0]
			tmpcode=tmpcode if len(tmpcode)<=3 else tmpcode[0:2]+tmpcode[-1]
			for rtcode in rtcodelist[1:]:
				tmpcode=CJCombideCode(tmpcode, rtcode)
			return tmpcode

		cjlist=[list(map(lambda c: c.getCJProp()[1], prelist)),
				list(map(lambda c: c.getCJProp()[1], postlist))]
		if cjlist[0] and cjlist[1] and all(cjlist[0]) and all(cjlist[1]):
			headcode=getCJRootCodeAsBody(cjlist[0])
			headcode=headcode if len(headcode)<=2 else headcode[0]+headcode[-1]
			bodycode=getCJRootCodeAsBody(cjlist[1])
			cjcode=headcode+bodycode
			cjbodycode=CJCombideCode(headcode, bodycode)
			self.setCJProp(cjcode, cjbodycode)

	@property
	def cj(self):
		return self._cj_incode

	@property
	def isSeted(self):
		return bool(self._cj_incode)

	def getCode(self):
		if self.cj: return self.cj

	def updateIMCode(self, chdesc):
		prelist, postlist=chdesc.getCJPrePostList()

		pre_chinfo_list=map(lambda x:x.getChInfo(), prelist)
		post_chinfo_list=map(lambda x:x.getChInfo(), postlist)

		self.setCJByComps(pre_chinfo_list, post_chinfo_list)

	def normalizationToLinear(self, chdesc):
		"""將樹狀結構轉為線性結構"""
		return chdesc.getCompList()

class ARCharInfo(CharInfo):
	def __init__(self, charname, parseans, prop):
		super().__init__(charname, parseans, prop)
		self._ar_incode=None
		if len(prop)>=1:
			self.setARProp(prop[0])
		self.noneFlag=False

	def setARProp(self, ar_incode):
		if ar_incode=='XXXX':
			self._ar_incode=None
		else:
			self._ar_incode=ar_incode

	def getARProp(self):
		return self._ar_incode

	def setByComps(self, complist):
		arlist=list(map(lambda c: c.getARProp(), complist))
		if complist and all(arlist):
			cat="".join(arlist)
			ar=cat[:3]+cat[-1] if len(cat)>4 else cat
			self.setARProp(ar)

	@property
	def ar(self):
		return self._ar_incode

	@property
	def isSeted(self):
		return bool(self._ar_incode)

	def getCode(self):
		if self.ar: return self.ar

class DYCharInfo(CharInfo):
	def __init__(self, charname, parseans, prop):
		super().__init__(charname, parseans, prop)
		self._dy_incode=None
		self._flag_seted=False
		if len(prop)>=1:
			self.setDYProp(prop[0])
		self.noneFlag=False

	def setDYProp(self, dy_incode):
		if dy_incode=='XXXX':
			self._dy_incode=None
		else:
			self._dy_incode=dy_incode
		self._flag_seted=True

	def getDYProp(self):
		return self._dy_incode

	def setByComps(self, complist):
		dylist=list(map(lambda c: c.getDYProp(), complist))
		if complist and all(dylist):
			cat="".join(dylist)
			dy=cat[:3]+cat[-1] if len(cat)>4 else cat
			self.setDYProp(dy)

	@property
	def dy(self):
		return self._dy_incode

	@property
	def isSeted(self):
		return self._flag_seted
		return bool(self._dy_incode)

	def getCode(self):
		if self.dy: return self.dy

class BSCharInfo(CharInfo):
	def __init__(self, charname, parseans, prop):
		super().__init__(charname, parseans, prop)
		self._bs_incode=None
		self._bs_spcode=None
		if len(prop)>=2:
			self.setBSProp(prop[0], prop[1])
		self.noneFlag=False

	def setBSProp(self, bs_incode, bs_spcode):
		if bs_incode=='XXXX' or bs_spcode=='XXXX':
			self._bs_incode=None
			self._bs_spcode=None
		else:
			self._bs_incode=bs_incode
			self._bs_spcode=bs_spcode

	def getBSProp(self):
		return [self._bs_incode, self._bs_spcode]

	def setByComps(self, complist):
		bslist=list(map(lambda c: c.getBSProp()[0], complist))
		if complist and all(bslist):
			cat="".join(bslist)
			bs_incode=(cat[:3]+cat[-1]) if len(cat)>4 else cat
			bs_spcode=complist[-1].getBSProp()[1]
			self.setBSProp(bs_incode, bs_spcode)

	@property
	def bs(self):
		if self._bs_incode==None or self._bs_spcode==None:
			return None
		if len(self._bs_incode)<3:
			return self._bs_incode+self._bs_spcode
		else:
			return self._bs_incode

	@property
	def isSeted(self):
		return bool(self._bs_incode)

	def getCode(self):
		if self.bs: return self.bs

class ZMCharInfo(CharInfo):
	def __init__(self, charname, parseans, prop):
		super().__init__(charname, parseans, prop)
		self._zm_rtlist=[]
		self._zm_incode=None
		self._zm_tpcode=None
		if len(prop)>=1:
			str_rtlist=prop[0]
			if str_rtlist=='XXXX':
				self.setZMProp([])
			else:
				self.setZMProp(str_rtlist.split(','))
		self.noneFlag=False

	def setZMProp(self, zm_rtlist):
		self._zm_rtlist=zm_rtlist

	def getZMProp(self):
		return self._zm_rtlist

	def setByComps(self, complist):
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

	@property
	def isSeted(self):
		return bool(self._zm_rtlist)

	def getCode(self):
		if self.zm: return self.zm

