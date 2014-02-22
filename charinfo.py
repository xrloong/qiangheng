
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
		compList=[x.getChInfo() for x in descList]
		self.setByComps(compList)

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

		self._cj_direction=None	# 組件的方向
		self._cj_single=None	# 當此字為獨體時的碼。
		self._cj_body=None	# 當此字為字身時的碼。
		self._cj_radix_list=[]	# 組件
		if len(prop)>=2:
#			self.setCJProp(prop[0], prop[1])
			self.setCJProp(prop[0], prop[2])
		self.noneFlag=False

	def setCJProp(self, cj_single, cj_info_code):
		if len(cj_info_code)>0:
			dir_code=cj_info_code[0]
			if dir_code not in ['|', '-', '+']:
				dir_code='+'

			self._cj_radix_list=cj_info_code[1:].split(',')
		else:
			dir_code='+'
			self._cj_radix_list=[]

		if cj_single=='XXXX':
			self._cj_incode=None
		else:
			self._cj_incode=cj_single

		self._cj_single=cj_single
		self._cj_direction=dir_code
		self._cj_body=self.computeBodyCode(self._cj_radix_list)

	def getCJProp(self):
		return [self._cj_direction, self._cj_radix_list]

	def setByComps(self, complist):
		dir_code=self._cj_direction

		ansRadixList=[]
		for tmpchinfo in complist:
			tmpDirCode, tmpRadixList=tmpchinfo.getCJProp()
			if tmpDirCode=='+':
				ansRadixList.append(tmpchinfo._cj_body)
			elif tmpDirCode==dir_code:
				# 同向
				ansRadixList.extend(tmpRadixList)
			else:
				# 不同向
				ansRadixList.append(tmpchinfo._cj_body)

		self._cj_radix_list=ansRadixList
		self._cj_body=self.computeBodyCode(self._cj_radix_list)

	@property
	def cj(self):
		if self._cj_single:
			return self._cj_single
		else:
			return self.computeTotalCode(self._cj_radix_list).lower()
		return self._cj_incode.lower()

	@property
	def isSeted(self):
		return bool(self._cj_incode)

	def getCode(self):
		if self.cj: return self.cj

	def computeHeadTailCode(self, code, headCount):
		frontCode=code[:headCount]
		rearCode=code[headCount:]

		# 以大寫來表示重要的尾碼
		xTailCode=list(filter(lambda x: x.isupper(), rearCode))
		if len(xTailCode)>0:
			# 重要的尾碼
			tailCode=xTailCode[-1]
		elif len(rearCode)>0:
			tailCode=rearCode[-1]
		else:
			tailCode=''

		return frontCode+tailCode

	def computeHeadCode(self, code):
		headCode=self.computeHeadTailCode(code, 1)
		return headCode

	def computeBodyCode(self, codeList):
		bodyCode=''
		if len(codeList)==0:
			bodyCode=''
		elif len(codeList)==1:
			bodyCode=self.computeHeadTailCode(codeList[0], 2)
		else:
			tmpCodeList=codeList

			tmpHeadCode=self.computeHeadCode(tmpCodeList[0])
			tmpCodeList=tmpCodeList[1:]

			if len(tmpHeadCode)==2:
				if len(tmpCodeList)>0:
					tmpBodyCode=self.computeHeadTailCode(tmpCodeList[-1], 0)
				else:
					tmpBodyCode=''
			elif len(tmpHeadCode)==1:
				tmpHeadCode2=self.computeHeadCode(tmpCodeList[0])
				tmpCodeList=tmpCodeList[1:]

				if len(tmpCodeList)>0:
					tmpBodyCode2=self.computeHeadTailCode(tmpCodeList[-1], 0)
				else:
					tmpBodyCode2=''
				tmpBodyCode=self.computeHeadTailCode(tmpHeadCode2+tmpBodyCode2, 1)
			else:
				# 理論上錯誤
				tmpBodyCode=''
			bodyCode=tmpHeadCode+tmpBodyCode
		return bodyCode

	def computeTotalCode(self, codeList):
		if len(codeList)>0:
			totalCode=self.computeHeadCode(codeList[0])+self.computeBodyCode(codeList[1:])
		else:
			totalCode=''
		return totalCode

	def updateIMCode(self, chdesc):
		# 計算倉頡碼時，需要知道此字部件的組成方向
		self._cj_direction=chdesc.getDir()

		descList=chdesc.getCompList()
		compList=[x.getChInfo() for x in descList]
		self.setByComps(compList)

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

